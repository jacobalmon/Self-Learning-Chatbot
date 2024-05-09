from flask import Flask, request, jsonify
import sqlite3
import random
import threading
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import GPT2LMHeadModel, GPT2Tokenizer

server = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')

class ChatBot:
    def __init__(self):
        self.lock = threading.Lock()
        self.connect = sqlite3.connect(':memory:', check_same_thread=False) #In Memory SQLite Database.
        self.create_table()
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")
        self.training_data = []

    def create_table(self):
        with self.lock:
            c = self.connect.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS conversations (
                        user_input TEXT,
                        bot_response TEXT
                    )''')
            self.connect.commit()
    
    def add_conversation(self, user_input, bot_response):
        with self.lock:
            c = self.connect.cursor()
            c.execute("INSERT INTO conversations VALUES (?, ?)", (user_input, bot_response))
            self.connect.commit()

    def get_response(self, user_input):
        if not user_input.strip():
            return "I don't understand"

        preproccessed_input = self.preprocess_input(user_input)
        with self.lock:
            c = self.connect.cursor()
            c.execute("SELECT bot_response FROM conversations WHERE user_input=?", (user_input,))
            rows = c.fetchall()
            if rows:
                return random.choice(rows)[0]
            else:
                return self.generate_response(preproccessed_input)
    
    def generate_response(self, user_input):
        inputs = self.tokenizer.encode(user_input, return_tensors="pt", add_special_tokens=True)
        outputs = self.model.generate(inputs, max_length=100, temperature=0.9, num_return_sequences=1, do_sample=True, pad_token_id=self.tokenizer.eos_token_id)
        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        clean_output = ''.join(e for e in decoded_output if e.isalnum() or e.isspace())
        return clean_output
        
    def update_training_data(self, user_input, bot_response):
        self.training_data.append((user_input, bot_response))

    def learn_from_conversation(self, user_input, bot_response):
        preprocessed_input = self.preprocess_input(user_input)
        self.add_conversation(user_input, bot_response)
        self.update_training_data(preprocessed_input, bot_response)

    def preprocess_input(self, user_input):
        tokens = word_tokenize(user_input.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]
        preprocessed_input = ' '.join(filtered_tokens)
        return preprocessed_input

chatbot = ChatBot()

@server.route('/')
def index():
    return open('index.html').read()

@server.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    bot_response = chatbot.get_response(user_input)
    chatbot.learn_from_conversation(user_input, bot_response)
    return jsonify({'message': bot_response})

if __name__ == '__main__':
    server.run(debug=True)