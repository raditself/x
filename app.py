










from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from github import Github
from github import GithubException
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    app.logger.info('Received chat request')
    data = request.json
    prompt = data.get('prompt', '')
    
    ollama_payload = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=ollama_payload)
        response.raise_for_status()
        ai_response = response.json()['response']
        return jsonify({"response": ai_response})
    except requests.RequestException as e:
        app.logger.error(f'Error in chat request: {str(e)}')
        return jsonify({"error": str(e)}), 500

@app.route('/api/files', methods=['GET', 'POST'])
def files():
    if request.method == 'GET':
        app.logger.info('Listing files')
        files = []
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(file_path),
                    'modified': os.path.getmtime(file_path)
                })
        return jsonify({"files": files})
    elif request.method == 'POST':
        app.logger.info('Uploading file')
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"message": "File uploaded successfully"})
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/api/files/<filename>', methods=['GET'])
def download_file(filename):
    app.logger.info(f'Downloading file: {filename}')
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

@app.route('/api/github', methods=['POST'])
def github():
    app.logger.info('Received GitHub request')
    data = request.json
    repo_name = data.get('repo_name')
    file_name = data.get('file_name')
    commit_message = data.get('commit_message', 'Update from web app')
    
    if not all([repo_name, file_name]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(repo_name)
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        try:
            contents = repo.get_contents(file_name)
            repo.update_file(contents.path, commit_message, content, contents.sha)
        except GithubException:
            repo.create_file(file_name, commit_message, content)
        
        return jsonify({"message": "File successfully pushed to GitHub"})
    except Exception as e:
        app.logger.error(f'Error in GitHub request: {str(e)}')
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.logger.info('Starting Flask application')
    app.run(debug=True)










