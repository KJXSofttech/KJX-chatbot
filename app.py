from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat_response():
    from stories import get_chat_response
    return get_chat_response()

@app.route("/start_conversation", methods=["POST"])
def start_conversation():
    return chat_response()  # Use the same function for both routes

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
