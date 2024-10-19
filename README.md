# Ollama Chatbot

This is a simple chatbot using Ollama and Streamlit.

## Prerequisites

- [Ollama](https://ollama.ai/download) installed and running on your system
- Python 3.7+

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/raditself/x.git
   cd x
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Pull the Llama2 model using Ollama:
   ```
   ollama pull llama2
   ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run chatbot.py
   ```

2. Open your web browser and go to the URL displayed in the terminal (usually http://localhost:8501)

3. Start chatting with the bot!

## Note

Make sure Ollama is running in the background before starting the Streamlit app.
