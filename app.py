
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from flask_pymongo import PyMongo
from pymongo import MongoClient

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
CLIENT = os.environ.get("CLIENT")




app = Flask(__name__)

client = MongoClient("CLIENT")
db = client['MadCampWeek2']
collection_User = db['User']





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

        existing_user = collection_User.find_one({"user_id": user_info.get('id')})
        if existing_user:
            return jsonify({'message': 'User already exists'}), 200

        user_id = user_info.get('id')
        user_nickname = user_info['kakao_account']['profile']['nickname']
        user_profile_image = user_info['kakao_account']['profile']['profile_image_url']

        # Prepare the document to insert into MongoDB
        user_document = {
            "user_id": user_id,
            "nickname": user_nickname,
            "profile_image": user_profile_image
        }

        # Step 4: Insert User Information into MongoDB
        result = collection_User.insert_one(user_document)
        # Step 4: Return User Information
        return jsonify(user_info)
    

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/info", methods=['POST'])
def update_user_info():
    data = request.get_json()

    user_id = data.get('user_id')
    age = data.get('age')
    gender = data.get('gender')
    height = data.get('height')
    weight = data.get('weight')
    exercise_goal = data.get('exercise_goal')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Build the update document
    update_doc = {
        "$set": {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "exercise_goal": exercise_goal
        }
    }

    # Update the user document in MongoDB
    result = collection_User.update_one({"user_id": user_id}, update_doc)
    
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User information updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True, host = "143.248.219.4", port = 8080)



