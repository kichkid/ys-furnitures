from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

WHATSAPP_NUMBER = "2347026972403"

@app.route("/get_whatsapp", methods=["GET"])
def get_whatsapp():
    return jsonify({"whatsapp": WHATSAPP_NUMBER})

if __name__ == "__main__":
    app.run(debug=True)

# app.py
# Flask app to serve WhatsApp number securely
# To run the app, use the command: python app.py
# To access the WhatsApp number, visit: http://localhost:5000/get-whatsapp
