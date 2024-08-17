from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from stories import get_chat_response
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

app = Flask(__name__)
app.json = CustomJSONProvider(app)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat_response():
    response = get_chat_response()
    return jsonify(response)

@app.route("/start_conversation", methods=["POST"])
def start_conversation():
    return chat_response()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)