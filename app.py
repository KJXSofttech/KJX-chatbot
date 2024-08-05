from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from stories import get_chat_response
import json
import os

app = Flask(__name__)
CORS(app)

# Load model data, not needed anymore so just keeping placeholders
try:
    # Replace with actual data if needed
    all_words = []
    tags = []
    professors_data = []
except FileNotFoundError as e:
    print(f"Error loading model: {e}")
    all_words = []
    tags = []
    professors_data = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat_response():
    return get_chat_response()

@app.route("/start_conversation", methods=["POST"])
def start_conversation():
    return get_chat_response()

def save_user_data(data):
    try:
        with open('user_data.json', 'a') as f:
            json.dump(data, f)
            f.write("\n")
    except Exception as e:
        print(f"Error saving user data: {e}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)
