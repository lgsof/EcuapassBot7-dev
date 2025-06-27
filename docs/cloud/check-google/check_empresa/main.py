"""
Script using google cloud to check  if an 'empresa' is allowed for using EcuapassBot
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock valid users
VALID_USERS = {"BYZA", "ALDIA", "SANCHEZPOLO"}

@app.route('/check_empresa', methods=['POST'])
def check_empresa():
	data    = request.json
	empresa = data.get ('empresa')
	
	if empresa in VALID_USERS:
		return jsonify({"status": "success", "message": "Empresa is valid"}), 200
	else:
		return jsonify({"status": "failure", "message": "Invalid empresa"}), 403

