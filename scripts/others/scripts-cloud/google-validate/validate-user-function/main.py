from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock valid users
VALID_USERS = {"user1", "user2", "user3"}

@app.route('/validate_user', methods=['POST'])
def validate_user():
    try:
        data = request.json
        if not data or 'username' not in data:
            return jsonify({"status": "failure", "message": "Missing username"}), 400

        username = data.get('username')
        if username in VALID_USERS:
            return jsonify({"status": "success", "message": "User is valid"}), 200
        else:
            return jsonify({"status": "failure", "message": "Invalid user"}), 403
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "failure", "message": "Internal Server Error"}), 500

# Entry point for Google Cloud Functions
def function(request):
    """Google Cloud Function entry point."""
    with app.request_context(request.environ):
        # Route root requests ("/") to "/validate_user" in Flask
        if request.path == '/':
            request.environ['PATH_INFO'] = '/validate_user'
        response = app.full_dispatch_request()
        return response.get_data(), response.status_code, dict(response.headers)

