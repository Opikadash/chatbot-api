# app.py
from flask import Flask, request, jsonify
import pymongo
import bcrypt
import json
from datetime import datetime

app = Flask(__name__)

# MongoDB connection (replace with your URI)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
users_collection = db["users"]
chats_collection = db["chats"]

# Load chatbot rules from JSON file
with open('rules.json', 'r') as f:
    rules = json.load(f)

# Root route to handle requests to "/"
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Chatbot API! Use /signup, /login, or /chat endpoints to interact."}), 200

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Helper function to verify passwords
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# User Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User created successfully"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"username": username})
    if not user or not verify_password(password, user['password']):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "username": username}), 200

# Chatbot Response Logic
def get_chatbot_response(message):
    message = message.lower()
    for rule in rules.get("responses", []):
        for pattern in rule.get("patterns", []):
            if pattern in message:
                return rule.get("response", "Sorry, I don't understand.")
    return "Sorry, I don't understand."

# Send Message
@app.route('/chat/<username>', methods=['POST'])
def send_message(username):
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    response = get_chatbot_response(message)
    chat = {
        "username": username,
        "message": message,
        "response": response,
        "timestamp": datetime.utcnow()
    }
    chats_collection.insert_one(chat)
    return jsonify({"message": message, "response": response}), 200

# Get Chat History
@app.route('/chat/<username>', methods=['GET'])
def get_chat_history(username):
    chats = list(chats_collection.find({"username": username}, {'_id': 0}).sort("timestamp", -1).limit(10))
    return jsonify(chats), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
