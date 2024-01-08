
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
collection_Grass = db['Grass']
collection_Rank = db['Rank']





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
        # print(token_response.text) # 이걸로 요청하는듯
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

        user_id_str = str(user_info.get('id'))

        existing_user = collection_User.find_one({"user_id": user_id_str})
        if existing_user:
            # Fetch the user's goal data from collection_Goal
            user_goals = collection_Goal.find_one({"user_id": user_id_str})
            if user_goals:
                # Remove the '_id' field from the user_goals if it exists
                user_goals.pop('_id', None)

            # Extract nickname and profile_image from existing_user
            nickname = existing_user.get('nickname')
            profile_image = existing_user.get('profile_image')

            # Construct the user_data response
            user_data = {
                "exist": "yes",
                "goals": user_goals,
                "nickname": nickname,
                "profile_image": profile_image,
                "user_id": user_id_str
            }

            # 결합된 데이터를 JSON 형태로 반환합니다.
            return jsonify(user_data), 200
        else :
    
            user_nickname = user_info['kakao_account']['profile']['nickname']
            user_profile_image = user_info['kakao_account']['profile']['profile_image_url']

            # Prepare the document to insert into MongoDB
            new_user_document = {
                "user_id": user_id_str,
                "nickname": user_nickname,
                "profile_image": user_profile_image
            }
            
            # Step 4: Insert User Information into MongoDB
            collection_User.insert_one(new_user_document)
            new_user_document.pop('_id', None)
            # Step 4: Return User Information
            return jsonify(new_user_document) , 200
    

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/info", methods=['POST'])
def update_user_info():
    data = request.get_json()
    user_id = (data.get('user_id'))
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
        user_id = (data.get('user_id'))
        
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
        exercise_names = [exercise['name'] for exercise in exercise_cursor]
        
        # Call the recommendation function to get a list of recommended exercise names
        recommended_exercise_names = recommendation(age, gender, height, weight, exercise_goal, exercise_names)
        
        # Fetch full details for the recommended exercises
        recommended_exercises_info = []
        for name in recommended_exercise_names:
            exercise_details = collection_Exercise.find_one({"name": name})
            if exercise_details:
                # Omit the MongoDB '_id' from the JSON response
                exercise_details.pop('_id', None)
                recommended_exercises_info.append(exercise_details)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/record", methods=['POST'])
def record_exercise_session():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        exercise_date = data.get('date')  # Format: "YYYY-MM-DD"
        duration = data.get('duration')
        exercises = data.get('exercises')  # Assuming this is a list

        if not user_id or not exercise_date or duration is None:
            return jsonify({'error': 'Missing required fields'}), 400

        # Parse the date to extract year and month
        year_month = exercise_date[:7]  # "YYYY-MM"

        # Find the user's record
        user_record = collection_Grass.find_one({"user_id": user_id})

        if not user_record:
            # Create a new record for a new user
            new_record = {
                "user_id": user_id,
                "exercise_sessions": {
                    year_month: {
                        "exercise_sessions": [
                            {"date": exercise_date, "duration": duration}
                        ],
                        "score": duration  # Initial score is the duration
                    }
                }
            }
            collection_Grass.insert_one(new_record)
        else:
            # Update the existing record
            monthly_record = user_record.get("exercise_sessions", {}).get(year_month)

            if monthly_record:
                # Update the existing monthly record
                monthly_record["exercise_sessions"].append({"date": exercise_date, "duration": duration})
                monthly_record["score"] += duration  # Update the score
            else:
                # Create a new monthly record
                user_record["exercise_sessions"][year_month] = {
                    "exercise_sessions": [{"date": exercise_date, "duration": duration}],
                    "score": duration
                }

            # Update the user's record in the database
            collection_Grass.update_one({"user_id": user_id}, {"$set": user_record})

        return jsonify({'message': 'Exercise session recorded successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/grass", methods=['POST'])
def get_exercise_sessions():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        year = data.get('year')
        month = data.get('month')

        # Validate incoming data
        if not user_id or year is None or month is None:
            return jsonify({'error': 'User ID, year, and month are required'}), 400

        # Prepare the query to match the date format
        date_query = f"{year:04d}-{month:02d}"

        # Fetch the exercise sessions for the given user_id and date range
        user_record = collection_Grass.find_one({"user_id": user_id})
        
        if not user_record:
            return jsonify({'error': 'No record found for the given user_id'}), 404

        # Filter sessions that match the given year and month
        matched_sessions = [
            session for session in user_record.get('exercise_sessions', [])
            if session['date'].startswith(date_query)
        ]

        # Return the matched exercise sessions as JSON
        return jsonify(matched_sessions), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    




if __name__ == '__main__': 
    app.run(debug=True, host = "143.248.219.4", port = 8080)




    



