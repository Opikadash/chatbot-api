# train_lstm_model.py
import nltk
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from sklearn.preprocessing import LabelEncoder
import pickle

# Download required NLTK data
nltk.download('punkt')

# Sample training data: messages and their corresponding intents
data = [
    ("hello", "greeting"),
    ("hi there", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("help me", "help"),
    ("i need assistance", "help"),
    ("support", "help"),
    ("can you assist", "help"),
    ("bye", "goodbye"),
    ("goodbye", "goodbye"),
    ("see you", "goodbye"),
    ("exit", "goodbye"),
    ("what is ai", "question"),
    ("tell me about machine learning", "question"),
    ("how does nlp work", "question"),
]

# Intent-to-response mapping (fallback responses)
responses = {
    "greeting": "Hello! How can I assist you today?",
    "help": "I'm here to help! Please tell me your issue.",
    "goodbye": "Goodbye! Have a great day!",
    "question": "Let me find an answer for you...",
    "unknown": "Sorry, I don't understand."
}

# Prepare data
texts = [text for text, _ in data]
labels = [intent for _, intent in data]

# Tokenize texts
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

# Pad sequences to ensure uniform length
max_len = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# Encode labels
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Build LSTM model
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 50

model = Sequential([
    Embedding(vocab_size, embedding_dim, input_length=max_len),
    LSTM(64, return_sequences=False),
    Dense(32, activation='relu'),
    Dense(len(label_encoder.classes_), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train the model
model.fit(padded_sequences, encoded_labels, epochs=50, verbose=1)

# Save the model, tokenizer, label encoder, and responses
model.save("lstm_intent_model.h5")
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)
with open("responses.pkl", "wb") as f:
    pickle.dump(responses, f)

print("LSTM model training complete. Files saved: lstm_intent_model.h5, tokenizer.pkl, label_encoder.pkl, responses.pkl")
