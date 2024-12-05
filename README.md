# AI Chatbot with Flask and GPT-2

## Introduction
This project is a web-based AI chatbot built using Flask and GPT-2, with a simple HTML frontend for user interaction. The chatbot processes user input, generates responses using a pretrained GPT-2 model, and communicates with the backend via AJAX.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Configuration](#configuration)

## Features
- **Real-Time Chat**: Interactive chat interface for users.
- **GPT-2 Responses**: Generates human-like responses using GPT-2.
- **Flask Backend**: Handles API requests and integrates with the chatbot model.
- **AJAX Communication**: Sends and receives messages asynchronously.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/ai-chatbot.git
    cd ai-chatbot
    ```

2. Install dependencies:
    ```bash
    pip install Flask transformers nltk
    ```

3. Download NLTK resources:
    ```python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    ```

4. Run the Flask server:
    ```bash
    python app.py
    ```

5. Open the browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```

## File Structure
- `app.py`: Flask backend handling requests and generating responses.
- `index.html`: Frontend HTML for the chat interface.
- `static/`: Directory for static files (CSS, JS).

## API Endpoints
### `/chat` (POST)
- **Request**: JSON payload with a `message` field.
- **Response**: JSON object containing the bot's response.
- Example:
    ```bash
    curl -X POST http://127.0.0.1:5000/chat -H "Content-Type: application/json" -d '{"message": "Hello"}'
    ```

## Dependencies
- **Flask**: For the web server and handling HTTP requests.
- **transformers**: For GPT-2 model usage.
- **NLTK**: For preprocessing input text.
- **SQLite**: For storing conversation history (in-memory database).

Install dependencies with:
```bash
pip install Flask transformers nltk
```

## Configuration
- **Model**: The GPT-2 model is loaded from Hugging Face.
- **Database**: Uses an in-memory SQLite database.
