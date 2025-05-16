# Chatbot API

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
