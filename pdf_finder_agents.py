import autogen
import os
from dotenv import load_dotenv
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import hashlib
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logging.error("OPENAI_API_KEY not found in environment variables")
    sys.exit(1)

# Configure API key
config_list = [
    {
        'model': 'gpt-4',
        'api_key': api_key,
    }
]

# Create agent configurations
assistant_config = {
    "seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

def sanitize_filename(url: str) -> str:
    """Create a safe filename from URL."""
    try:
        # Get the last part of the URL
        filename = url.split('/')[-1]
        # Remove query parameters if any
        filename = filename.split('?')[0]
        # If filename is empty or doesn't end with .pdf, create a hash-based name
        if not filename or not filename.lower().endswith('.pdf'):
            filename = hashlib.md5(url.encode()).hexdigest()[:10] + '.pdf'
        # Replace unsafe characters
        filename = ''.join(c for c in filename if c.isalnum() or c in '.-_')
        return filename
    except Exception as e:
        logging.error(f"Error sanitizing filename for URL {url}: {str(e)}")
        return hashlib.md5(url.encode()).hexdigest()[:10] + '.pdf'

def download_pdf(url: str, save_dir: str) -> Dict[str, str]:
    """Download a PDF file from the given URL."""
    result = {"status": "failed", "message": "", "path": ""}
    try:
        logging.info(f"Attempting to download PDF from: {url}")
        
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # First check if the URL is accessible
        response = requests.head(url, headers=headers, timeout=10)
        if response.status_code != 200:
            result["message"] = f"URL not accessible: HTTP {response.status_code}"
            logging.warning(result["message"])
            return result
            
        # Download the file
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            content_disp = response.headers.get('content-disposition', '').lower()
            
            # Check if it's a PDF either by content-type or URL
            if 'pdf' in content_type or 'pdf' in content_disp or url.lower().endswith('.pdf'):
                filename = sanitize_filename(url)
                save_path = os.path.join(save_dir, filename)
                
                file_size = 0
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file_size += len(chunk)
                            f.write(chunk)
                
                # Verify the file was actually downloaded
                if file_size > 0:
                    result["status"] = "success"
                    result["message"] = f"Successfully downloaded to {filename} ({file_size} bytes)"
                    result["path"] = save_path
                    logging.info(result["message"])
                else:
                    result["message"] = "Downloaded file is empty"
                    logging.warning(result["message"])
                    if os.path.exists(save_path):
                        os.remove(save_path)
            else:
                result["message"] = f"URL does not point to a PDF file (content-type: {content_type})"
                logging.warning(result["message"])
        else:
            result["message"] = f"Failed to download: HTTP {response.status_code}"
            logging.warning(result["message"])
            
    except requests.exceptions.RequestException as e:
        result["message"] = f"Network error: {str(e)}"
        logging.error(result["message"])
    except Exception as e:
        result["message"] = f"Error downloading: {str(e)}"
        logging.error(result["message"])
    
    return result

# Create the research agent that searches for PDFs
research_agent = autogen.AssistantAgent(
    name="research_agent",
    system_message="""Research Agent: Your role is to search for PDF files related to a given topic.
    You will receive a topic and should return a list of PDF URLs related to that topic.
    Focus on academic and reliable sources. After finding URLs, pass them to the download agent.
    Format your response as a numbered list with title and URL on separate lines.
    
    Important: Only include URLs that are likely to be directly downloadable PDF files.""",
    llm_config=assistant_config,
)

# Create the download agent that handles file downloading
download_agent = autogen.AssistantAgent(
    name="download_agent",
    system_message="""Download Agent: Your role is to download PDF files from provided URLs.
    When you receive URLs from the Research Agent:
    1. For each URL, you MUST execute this exact function call:
       download_pdf(url, "pdf_downloads")
    2. Report the actual result returned by the function
    
    Important: 
    - You MUST actually execute the download_pdf function call for each URL
    - Do NOT just describe what you would do
    - Do NOT say "Status: Success" unless you actually called the function
    - Report the exact result returned by the function
    
    Example response format:
    URL: [url]
    Result: [actual result from download_pdf function call]
    
    Final Summary: X downloads attempted""",
    llm_config=assistant_config,
    function_map={"download_pdf": download_pdf}
)

# Create the user proxy agent
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    system_message="User Proxy: Coordinate between the Research and Download agents.",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,  # Limit the conversation to prevent infinite loops
    code_execution_config={
        "work_dir": "pdf_downloads",
        "use_docker": False  # Disable Docker
    }
)

def initialize_workspace():
    """Create the downloads directory if it doesn't exist."""
    downloads_dir = "pdf_downloads"
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
        logging.info(f"Created downloads directory: {downloads_dir}")
    return downloads_dir

def start_task(topic: str):
    """Start the collaborative task with the given topic."""
    try:
        downloads_dir = initialize_workspace()
        logging.info(f"Starting PDF search and download task for topic: {topic}")
        
        # Create a group chat
        groupchat = autogen.GroupChat(
            agents=[user_proxy, research_agent, download_agent],
            messages=[],
            max_round=5  # Limit the number of conversation rounds
        )
        
        manager = autogen.GroupChatManager(groupchat=groupchat)
        
        # Start the conversation
        user_proxy.initiate_chat(
            manager,
            message=f"Please find and download PDF files related to the topic: {topic}. Research Agent should find the URLs, and Download Agent should handle the downloads to the directory: {downloads_dir}"
        )
        
        logging.info("Task completed")
        
    except Exception as e:
        logging.error(f"Error during task execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Example usage
        topic = "artificial intelligence in healthcare"
        start_task(topic)
    except KeyboardInterrupt:
        logging.info("\nTask interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
