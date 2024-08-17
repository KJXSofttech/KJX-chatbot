from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from stories import get_chat_response
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
import logging

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.json = CustomJSONProvider(app)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat_response():
    try:
        response = get_chat_response()
        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in chat_response: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."})

@app.route("/start_conversation", methods=["POST"])
def start_conversation():
    try:
        return chat_response()
    except Exception as e:
        logging.error(f"Error in start_conversation: {e}")
        return jsonify({"error": "An internal error occurred. Please try again later."})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
