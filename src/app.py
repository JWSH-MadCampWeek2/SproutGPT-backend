
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from flask_pymongo import PyMongo
# from controller import Oauth
# from model import UserModel, UserData

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")






app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://sspringson:<password>@madcampweek2.kdhm8ha.mongodb.net/"
mongo = PyMongo(app)


@app.route("/oauth", methods=['POST'])
def oauth_api():
    # Step 1: Receive Authorization Code
    data = request.get_json()
    authorization_code = data.get('authorization_code') #

    if not authorization_code:
        return jsonify({'error': 'Authorization code is required'}), 400

    token_url = 'https://kauth.kakao.com/oauth/token'

    payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'code': authorization_code,
    }
    if CLIENT_SECRET:
        payload['client_secret'] = CLIENT_SECRET

    try:
        token_response = requests.post(token_url, data=payload) # 이걸로 요청하는듯
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return jsonify({'error': 'Access token not found'}), 400

        # Step 3: Fetch User Information
        user_info_url = 'https://kapi.kakao.com/v2/user/me'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        user_response = requests.get(user_info_url, headers=headers)
        user_response.raise_for_status()
        user_info = user_response.json()

        # Step 4: Return User Information
        return jsonify(user_info)
    

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/add', methods=['POST'])
def add_data():
    # Assume JSON data comes with the POST request
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Insert the data into the 'myCollection' collection
        result = mongo.db.myCollection.insert_one(data)
        # Return the ID of the inserted document
        return jsonify({"_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host = "143.248.219.4", port = 8080)

