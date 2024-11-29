<<<<<<< HEAD
# Multi-Agent PDF Discovery System

This project implements a multi-agent system using AutoGen to collaboratively search and download PDF files related to specific topics.

## System Architecture

The system consists of three main agents:

1. **Research Agent**: Searches for PDF files related to a given topic and compiles a list of URLs.
2. **Download Agent**: Receives URLs from the Research Agent and handles the downloading process.
3. **User Proxy Agent**: Coordinates the interaction between agents and manages the overall workflow.

## Technical Documentation

### System Overview
The Multi-Agent PDF Discovery System is an AI-powered collaborative system designed to automatically search and download research PDFs on specified topics. The system utilizes AutoGen's multi-agent framework to coordinate between specialized agents that handle different aspects of the PDF discovery and download process.

### Architecture

#### Agent Components
1. **User Proxy Agent**
   - Acts as an intermediary between the user and other agents
   - Coordinates the workflow between Research and Download agents
   - Handles user input and system output

2. **Research Agent**
   - Specializes in finding relevant PDF URLs
   - Uses semantic search to identify appropriate academic papers
   - Filters and ranks results based on relevance
   - Returns structured URL data with paper titles

3. **Download Agent**
   - Handles PDF file downloading
   - Implements robust error handling
   - Manages file naming and storage
   - Reports download status and results

### Technical Implementation

#### Core Technologies
- **Python Version**: 3.8+
- **Primary Framework**: AutoGen v0.2.0
- **Key Dependencies**:
  - `pyautogen`: Multi-agent orchestration
  - `requests`: HTTP handling
  - `beautifulsoup4`: Web scraping
  - `python-dotenv`: Environment variable management
  - `hashlib`: Secure filename generation

#### Configuration
```python
# Agent Configuration
assistant_config = {
    "seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120
}

# System Parameters
MAX_CONVERSATIONS = 5
DOWNLOAD_TIMEOUT = 120
```

#### Security Features
1. **API Key Management**
   - OpenAI API keys stored in `.env` file
   - Secure environment variable loading
   - No hardcoded credentials

2. **File Security**
   - URL sanitization
   - Secure filename generation
   - Download validation checks

3. **Error Handling**
   - Network timeout management
   - Invalid URL detection
   - Corrupt file checking
   - Rate limiting compliance

### Workflow Process

1. **Initialization**
   ```python
   # Load environment variables
   load_dotenv()
   
   # Initialize agents
   user_proxy = autogen.UserProxyAgent(...)
   research_agent = autogen.AssistantAgent(...)
   download_agent = autogen.AssistantAgent(...)
   ```

2. **Research Phase**
   - User provides research topic
   - Research Agent searches for relevant PDFs
   - Returns structured list of URLs and titles

3. **Download Phase**
   - Download Agent processes each URL
   - Implements retry logic for failed downloads
   - Validates downloaded files
   - Reports success/failure status

4. **Error Management**
   ```python
   try:
       response = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
       # Download handling
   except requests.exceptions.RequestException as e:
       logging.error(f"Download failed: {str(e)}")
   ```

### System Requirements

#### Hardware Requirements
- CPU: Modern multi-core processor
- RAM: Minimum 4GB
- Storage: Sufficient for PDF storage

#### Software Requirements
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/macOS
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

### Usage Example

```python
# Initialize the system
user_proxy.initiate_chat(
    research_agent,
    message="Find PDFs about artificial intelligence in healthcare"
)
```

### Logging and Monitoring

The system implements comprehensive logging:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Error Codes and Troubleshooting

| Error Code | Description | Resolution |
|------------|-------------|------------|
| E001 | API Key Missing | Check .env file |
| E002 | Download Failed | Check network/retry |
| E003 | Invalid URL | Verify URL format |
| E004 | File Corruption | Retry download |

### Performance Considerations

- Implements rate limiting for API calls
- Chunked downloading for large files
- Efficient memory management
- Parallel download capabilities

### Future Enhancements

1. Advanced PDF content filtering
2. Multiple search engine support
3. Machine learning-based relevance scoring
4. Academic database integration
5. Enhanced metadata extraction

### Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request
4. Follow coding standards

### License

MIT License - See LICENSE file for details

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

3. Run the script:
```bash
python pdf_finder_agents.py
```

## Project Structure

- `pdf_finder_agents.py`: Main script containing the agent implementations
- `requirements.txt`: List of Python dependencies
- `pdf_downloads/`: Directory where downloaded PDFs are stored

## Features

- Collaborative multi-agent system using AutoGen
- Automated PDF discovery based on topics
- Coordinated downloading of found PDFs
- Error handling and download verification
- Clean separation of agent responsibilities

## Note

Make sure you have appropriate permissions and comply with website terms of service when downloading PDFs.
=======
# Multi-Agent-AI-System-for-Collaborative-Task-Completion
>>>>>>> d90b21bcff5d7c59ded9228165c8a9482282022d
