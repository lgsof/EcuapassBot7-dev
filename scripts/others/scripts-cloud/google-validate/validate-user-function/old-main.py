
from flask import Flask, request, jsonify

app = Flask (__name__)

# Mock valid users
VALID_USERS = {"BYZA", "REDFRONTE"}

@app.route ('/validate_user', methods=['POST'])
def validate_user():
    data = request.json
    username = data.get ('username')
    
    if username in VALID_USERS:
        return jsonify ({"status": "success", "message": "User is valid"}), 200
    else:
        return jsonify ({"status": "failure", "message": "Invalid user"}), 403

# This is the expected entry point for Cloud Functions
def function (request):
    return app (request)
