# AI Chatbot

This is an AI chatbot using the StableLM model.

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/raditself/x.git
   cd x
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Chatbot

1. Start the Flask server:
   ```
   python chatbot.py
   ```

2. The server will start on http://localhost:5000

3. You can interact with the chatbot by sending POST requests to http://localhost:5000/chat with a JSON payload:
   ```
   {"message": "Your message here"}
   ```

4. To check the model status, send a GET request to http://localhost:5000/model_status

## Features

- Automatic model downloading
- Real-time progress tracking for model download
- Model loading time tracking
- Logging of chat interactions and model responses

