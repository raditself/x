
import os
import logging
import time
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ctransformers import AutoModelForCausalLM

app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MODEL_URL = "https://huggingface.co/Crataco/stablelm-2-1_6b-chat-imatrix-GGUF/resolve/main/stablelm-2-1_6b-chat.Q4_K_M.imx.gguf?download=true"
MODEL_PATH = "stablelm-2-1_6b-chat.Q4_K_M.imx.gguf"

model = None
model_loading_start_time = None

def download_model():
    if not os.path.exists(MODEL_PATH):
        logger.info("Downloading model...")
        start_time = time.time()
        response = requests.get(MODEL_URL, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        downloaded_size = 0
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    elapsed_time = time.time() - start_time
                    progress = (downloaded_size / total_size) * 100
                    download_speed = downloaded_size / (1024 * 1024 * elapsed_time)
                    logger.info(f"Downloading... {progress:.2f}% | {downloaded_size/(1024*1024):.2f} MB / {total_size/(1024*1024):.2f} MB | Speed: {download_speed:.2f} MB/s")
        logger.info(f"Model downloaded successfully. Total time: {time.time() - start_time:.2f} seconds")
    else:
        logger.info("Model already exists.")

@app.route('/')
def index():
    logger.debug("Serving index.html")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global model, model_loading_start_time
    logger.debug("Received chat request")
    
    if model is None:
        if not os.path.exists(MODEL_PATH):
            download_model()
        logger.info("Loading model...")
        model_loading_start_time = time.time()
        model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, model_type="stablelm")
        loading_time = time.time() - model_loading_start_time
        logger.info(f"Model loaded successfully. Loading time: {loading_time:.2f} seconds")
    
    data = request.json
    user_input = data['message']
    logger.debug(f"User input: {user_input}")
    
    response = model(f"Human: {user_input}\nAssistant:", max_new_tokens=100)
    logger.debug(f"Model response: {response}")
    
    return jsonify({"response": response})

@app.route('/model_status', methods=['GET'])
def model_status():
    logger.debug("Checking model status")
    if model is None:
        if os.path.exists(MODEL_PATH):
            return jsonify({"status": "Model file exists, not loaded"})
        else:
            return jsonify({"status": "Model not downloaded"})
    else:
        return jsonify({"status": "Model loaded", "loading_time": f"{time.time() - model_loading_start_time:.2f} seconds"})

if __name__ == '__main__':
    logger.info("Starting Flask app")
    app.run(host='0.0.0.0', port=5000, debug=True)
