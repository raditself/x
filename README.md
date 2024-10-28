# AI-Powered Code Editor

This project is an AI-powered code editor with the following features:
- Chat interface with AI for code assistance
- File management (upload, list, and download)
- GitHub integration for pushing files to repositories

## Setup
1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
2. Set up environment variables:
   - GITHUB_TOKEN: Your GitHub personal access token
   - OLLAMA_API_URL: URL for the Ollama API (default: http://localhost:11434/api/generate)

## Running the application
Run the Flask application:
```
python app.py
```

The application will be available at http://localhost:5000
