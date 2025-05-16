# setup_knowledge_base.py
import pymongo
from sentence_transformers import SentenceTransformer
import numpy as np

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
knowledge_base_collection = db["knowledge_base"]

# Sample knowledge base
knowledge_base = [
    {"question": "What is AI?", "answer": "AI, or artificial intelligence, refers to the development of computer systems that can perform tasks that typically require human intelligence, such as learning, problem-solving, and decision-making."},
    {"question": "What is machine learning?", "answer": "Machine learning is a subset of AI that involves training algorithms to learn patterns from data and make predictions or decisions without being explicitly programmed."},
    {"question": "How does NLP work?", "answer": "NLP, or natural language processing, involves the use of algorithms to analyze, understand, and generate human language. It often uses techniques like tokenization, embeddings, and models like LSTM or transformers."},
    {"question": "What is a neural network?", "answer": "A neural network is a computational model inspired by the human brain, consisting of layers of interconnected nodes (neurons) that process input data to produce outputs, often used in machine learning tasks."},
]

# Load pre-trained sentence transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Compute embeddings for each question
for entry in knowledge_base:
    embedding = model.encode(entry["question"]).tolist()
    entry["embedding"] = embedding

# Insert into MongoDB
knowledge_base_collection.delete_many({})  # Clear existing data
knowledge_base_collection.insert_many(knowledge_base)

print("Knowledge base setup complete. Data inserted into MongoDB.")
