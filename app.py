
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from flask_pymongo import PyMongo
from pymongo import MongoClient
from src.recommendation import recommendation
load_dotenv() 

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
CLIENT = os.environ.get("CLIENT")


app = Flask(__name__)

client = MongoClient(CLIENT)
db = client['MadCampWeek2']
collection_User = db['User']
collection_Goal = db['Goal']
collection_Exercise = db['Exercise']





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
        token_response = requests.post(token_url, data=payload)
        print(token_response.text) # 이걸로 요청하는듯
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        print(8)
        

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
    user_id = (int)(data.get('user_id'))
    age = data.get('age')
    gender = data.get('gender')
    height = data.get('height')
    weight = data.get('weight')
    # exercise_goal = data.get('exercise_goal')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Build the update document
    update_doc = {
        "$set": {
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            # "exercise_goal": exercise_goal
        }
    }

    # Update the user document in MongoDB
    result = collection_User.update_one({"user_id": user_id}, update_doc)
    
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'message': 'User information updated successfully'}), 200



@app.route("/goal", methods=['POST'])
def update_goal_info():
    try:
        # Extracting data from POST request
        user_id = request.json['user_id']
        exercise_goal = request.json['exercise_goal']
        difficulty = request.json['difficulty']
        target = request.json['target']
        
        # Creating the document to insert into the database
        goal_document = {
            "exercise_goal": exercise_goal,
            "difficulty": difficulty,
            "target": target
        }
        
        # Updating the document in the collection for the given user_id
        # upsert=True will insert a new document if one does not exist
        result = collection_Goal.update_one(
            {"user_id": user_id},
            {"$set": goal_document},
            upsert=True
        )
        
        # Check if a new document was inserted
        if result.upserted_id is not None:
            message = "New user goal created successfully"
        else:
            message = "User goal updated successfully"
        
        # Returning success message
        return jsonify({"message": message}), 200
    except Exception as e:
        # Returning error message
        return jsonify({"error": str(e)}), 500
    

@app.route("/recommend", methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Fetch user's personal information
        user_info = collection_User.find_one({"user_id": user_id})
        if not user_info:
            return jsonify({'error': 'User not found'}), 404
        
        age = user_info.get('age')
        gender = user_info.get('gender')
        height = user_info.get('height')
        weight = user_info.get('weight')
        
        # Fetch user's exercise goal
        goal_info = collection_Goal.find_one({"user_id": user_id})
        if not goal_info:
            return jsonify({'error': 'Goal not found for user'}), 404
        
        exercise_goal = goal_info.get('exercise_goal')
        
        # Adjust the query to include both specific and mixed difficulties
        difficulty = goal_info.get('difficulty')
        target = goal_info.get('target')
        exercise_cursor = collection_Exercise.find({"difficulty": {"$in": [difficulty]}, "target": target})
        
        # Create a list of exercise names
        exercise_list = [exercise['name'] for exercise in exercise_cursor]
        
        # Call the recommendation function
        recommended_exercises = recommendation(age, gender, height, weight, exercise_goal, exercise_list)
        
        # Return the recommended exercises as JSON
        return jsonify({'recommended_exercises': recommended_exercises}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
if __name__ == '__main__':
    app.run(debug=True, host = "143.248.219.4", port = 8080)




    



