# Chatbot API (rule-based)-brach b1

## Overview
A RESTful API for a rule-based chatbot, built with Flask and MongoDB. Users can sign up, log in, send messages, and retrieve chat history. The chatbot responds based on predefined rules stored in `rules.json`, with conversation data stored in MongoDB. This project showcases backend development, database integration, and introductory NLP skills.

## Features
- User authentication (signup, login) with password hashing (bcrypt).
- Rule-based chatbot with predefined responses (e.g., greetings, FAQs).
- CRUD operations for chat history (create, read).
- MongoDB storage using PyMongo.

## Requirements
- Python 3.x
- MongoDB (local or MongoDB Atlas)
- Flask, PyMongo, bcrypt (listed in `requirements.txt`)

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Opikadash/chatbot-api.git
   cd chatbot-api
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**:
   - Update the MongoDB URI in `app.py` (line 10) with your URI.
   - Ensure MongoDB is running.

5. **Run the Application**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5001`.

## API Endpoints
- **POST /signup**: Create a new user.
  - Request: `{"username": "chatuser", "password": "chatpass"}`
  - Response: `{"message": "User created successfully"}`
- **POST /login**: Authenticate a user.
  - Request: `{"username": "chatuser", "password": "chatpass"}`
  - Response: `{"message": "Login successful", "username": "chatuser"}`
- **POST /chat/<username>**: Send a message and get a response.
  - Request: `{"message": "hello"}`
  - Response: `{"message": "hello", "response": "Hello! How can I assist you today?"}`
- **GET /chat/<username>**: Retrieve recent chat history.
  - Response: List of chats (e.g., `[{"message": "hello", "response": "...", "timestamp": "..."}]`).

## Testing
Test the endpoints using Postman, `curl` (on Unix-like systems), or PowerShell.

### Using `curl` (Unix-like systems or Windows with curl.exe)
- **Signup**:
  ```bash
  curl -X POST http://localhost:5001/signup -H "Content-Type: application/json" -d '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Login**:
  ```bash
  curl -X POST http://localhost:5001/login -H "Content-Type: application/json" -d '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Send Message**:
  ```bash
  curl -X POST http://localhost:5001/chat/chatuser -H "Content-Type: application/json" -d '{"message": "hello"}'
  ```
- **Get Chat History**:
  ```bash
  curl http://localhost:5001/chat/chatuser
  ```

### Using PowerShell (Windows)
- **Signup**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/signup -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Login**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/login -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Send Message**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/chat/chatuser -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "hello"}'
  ```
- **Get Chat History**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/chat/chatuser -Method GET
  ```

### Tested Scenarios
- User signup/login with valid/invalid credentials.
- Chatbot responses for defined rules and unknown inputs.
- Chat history retrieval.


# Chatbot API with LSTM and RAG -branch b2

## Overview
A RESTful API for an advanced chatbot, built with Flask and MongoDB, featuring intent recognition using an LSTM model (TensorFlow/Keras) and dynamic response generation via RAG (Retrieval-Augmented Generation). Users can sign up, log in, send messages, and retrieve chat history. The LSTM model classifies user intents (e.g., greeting, help, question), while the RAG system retrieves relevant answers from a MongoDB knowledge base using sentence embeddings. This project demonstrates backend development, advanced NLP with LSTM, and RAG implementation, making it highly relevant for AI/ML and Backend Intern roles at Pepsales.

## Features
- User authentication (signup, login) with password hashing (bcrypt).
- Intent recognition using an LSTM model (TensorFlow/Keras) for advanced NLP, improving accuracy over traditional rule-based systems.
- Dynamic response generation with RAG, leveraging sentence embeddings (`sentence-transformers`) to retrieve relevant answers from a MongoDB knowledge base.
- CRUD operations for chat history (create, read), stored in MongoDB.
- Backend logic implemented with Flask and PyMongo for seamless API and database integration.

## Requirements
- Python 3.x
- MongoDB (local or MongoDB Atlas)
- Flask, PyMongo, bcrypt, TensorFlow, sentence-transformers (listed in `requirements.txt`)

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Opikadash/chatbot-api.git
   cd chatbot-api
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Download NLTK data:
   ```python
   import nltk
   nltk.download('punkt')
   ```

4. **Train the LSTM Model**:
   ```bash
   python train_lstm_model.py
   ```
   This generates `lstm_intent_model.h5`, `tokenizer.pkl`, `label_encoder.pkl`, and `responses.pkl`.

5. **Set Up Knowledge Base for RAG**:
   ```bash
   python setup_knowledge_base.py
   ```
   This populates the `knowledge_base` collection in MongoDB with question-answer pairs and their embeddings.

6. **Configure MongoDB**:
   - Update the MongoDB URI in `app.py` (line 12) with your URI (e.g., `mongodb://localhost:27017/` for local or your MongoDB Atlas URI).
   - Ensure MongoDB is running.

7. **Run the Application**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5001`.

## API Endpoints
- **POST /signup**: Create a new user.
  - Request: `{"username": "chatuser", "password": "chatpass"}`
  - Response: `{"message": "User created successfully"}`
- **POST /login**: Authenticate a user.
  - Request: `{"username": "chatuser", "password": "chatpass"}`
  - Response: `{"message": "Login successful", "username": "chatuser"}`
- **POST /chat/<username>**: Send a message and get a response.
  - Request: `{"message": "what is ai"}`
  - Response: `{"message": "what is ai", "response": "AI, or artificial intelligence, refers to..."}`
- **GET /chat/<username>**: Retrieve recent chat history.
  - Response: List of chats (e.g., `[{"message": "what is ai", "response": "...", "timestamp": "..."}]`).

## Testing
Test the endpoints using Postman, `curl` (on Unix-like systems), or PowerShell.

### Using `curl` (Unix-like systems or Windows with curl.exe)
- **Signup**:
  ```bash
  curl -X POST http://localhost:5001/signup -H "Content-Type: application/json" -d '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Login**:
  ```bash
  curl -X POST http://localhost:5001/login -H "Content-Type: application/json" -d '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Send Message**:
  ```bash
  curl -X POST http://localhost:5001/chat/chatuser -H "Content-Type: application/json" -d '{"message": "what is ai"}'
  ```
- **Get Chat History**:
  ```bash
  curl http://localhost:5001/chat/chatuser
  ```

### Using PowerShell (Windows)
- **Signup**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/signup -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Login**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/login -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"username": "chatuser", "password": "chatpass"}'
  ```
- **Send Message**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/chat/chatuser -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message": "what is ai"}'
  ```
- **Get Chat History**:
  ```powershell
  Invoke-WebRequest -Uri http://localhost:5001/chat/chatuser -Method GET
  ```

### Tested Scenarios
- User signup/login with valid/invalid credentials.
- Intent recognition with LSTM for greetings, help requests, goodbyes, and questions.
- RAG-based dynamic responses for questions (e.g., "What is AI?"), retrieved from the MongoDB knowledge base.
- Chat history retrieval with MongoDB, ensuring persistence and retrieval of conversations.

## Future Improvements
- Expand the knowledge base with more question-answer pairs to improve RAG coverage.
- Fine-tune a generative model (e.g., GPT) for RAG generation, enabling more natural and context-aware responses.
- Enhance security with JWT authentication for production readiness.
- Use a larger dataset for LSTM training to improve intent recognition accuracy.
18325b).

