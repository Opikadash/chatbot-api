# app.py
from flask import Flask, request, jsonify
import pymongo
import bcrypt
import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sentence_transformers import SentenceTransformer, util
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
users_collection = db["users"]
chats_collection = db["chats"]
knowledge_base_collection = db["knowledge_base"]

# Load the LSTM model, tokenizer, label encoder, and responses
model = load_model("lstm_intent_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)
with open("responses.pkl", "rb") as f:
    responses = pickle.load(f)

# Load sentence transformer for RAG
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Root route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Chatbot API! Use /signup, /login, or /chat endpoints to interact."}), 200

# Helper function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Helper function to verify passwords
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Preprocessing for LSTM
def preprocess_text_lstm(text):
    sequence = tokenizer.texts_to_sequences([text.lower()])
    max_len = model.input_shape[1]  # Get max_len from model input shape
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
    return padded_sequence

# RAG: Retrieve relevant response from knowledge base
def retrieve_response(message):
    # Compute embedding for user message
    message_embedding = sentence_model.encode(message)

    # Retrieve all knowledge base entries
    knowledge_entries = list(knowledge_base_collection.find())
    if not knowledge_entries:
        return None

    # Compute similarity scores
    best_score = -1
    best_answer = None
    for entry in knowledge_entries:
        kb_embedding = np.array(entry["embedding"])
        score = util.cos_sim(message_embedding, kb_embedding).item()
        if score > best_score and score > 0.5:  # Threshold for relevance
            best_score = score
            best_answer = entry["answer"]

    return best_answer

# Chatbot response logic with LSTM and RAG
def get_chatbot_response(message):
    # Predict intent using LSTM
    processed_message = preprocess_text_lstm(message)
    intent_probs = model.predict(processed_message, verbose=0)
    intent_idx = np.argmax(intent_probs, axis=1)[0]
    intent = label_encoder.inverse_transform([intent_idx])[0]

    # If intent is "question", use RAG
    if intent == "question":
        rag_response = retrieve_response(message)
        if rag_response:
            return rag_response
        return responses.get(intent, responses["unknown"])
    
    # Otherwise, use predefined response
    return responses.get(intent, responses["unknown"])

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
