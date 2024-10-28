
from flask import Flask, request, jsonify, render_template, g
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
import requests
from dotenv import load_dotenv
import logging
import openai
from docker_sandbox import DockerSandbox

# Set up logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
limiter = Limiter(app, key_func=get_remote_address)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://admin:password@db/ai_assistant')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        g.current_user = user
        return username

@app.route('/')
def index():
    app.logger.info('Rendering index page')
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/chat', methods=['POST'])
@auth.login_required
@limiter.limit("10/minute")
def chat():
    app.logger.info('Received chat request')
    data = request.json
    prompt = data.get('prompt', '')
    
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_response = response.choices[0].message.content.strip()
        return jsonify({"response": ai_response})
    except Exception as e:
        app.logger.error(f'Error in chat request: {str(e)}')
        return jsonify({"error": str(e)}), 500

@app.route('/api/execute', methods=['POST'])
@auth.login_required
@limiter.limit("5/minute")
def execute_code():
    app.logger.info('Received code execution request')
    data = request.json
    code = data.get('code', '')
    
    try:
        sandbox = DockerSandbox()
        output = sandbox.execute_code(code)
        return jsonify({"output": output})
    except Exception as e:
        app.logger.error(f'Error in code execution: {str(e)}')
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
