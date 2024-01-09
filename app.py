
from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from flask_pymongo import PyMongo
from pymongo import MongoClient
from src.recommendation import recommendation
from src.comment import comment
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
collection_Score = db['Score']







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
        user_id = (str)(request.json['user_id'])
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
        targets = goal_info.get('target')
        difficulty_query = {"difficulty": {"$in": [difficulty, [difficulty]]}}
        
        # Prepare the query for targets
        target_query = {"target": {"$in": targets}}
        
        # Combine both queries with an AND condition
        combined_query = {"$and": [difficulty_query, target_query]}
        
        exercise_cursor = collection_Exercise.find(combined_query)
        
        # Create a list of exercise names
        exercise_names = [exercise['name'] for exercise in exercise_cursor]
        
        # Call the recommendation function to get a list of recommended exercise names
        recommended_exercise_names = recommendation(age, gender, height, weight, exercise_goal, exercise_names)
        comment_response = str(comment(age, gender, height, weight, exercise_goal, exercise_names,recommended_exercise_names))
        if isinstance(comment_response, dict) and "error" in comment_response:
            return jsonify(comment_response), 500

        # Fetch full details for the recommended exercises
        recommended_exercises_info = []
        for name in recommended_exercise_names:
            exercise_detail = collection_Exercise.find_one({"name": name}, {'_id': False})
            if exercise_detail:
                recommended_exercises_info.append(exercise_detail)


        print(comment_response)

        # Include comment response in the final JSON response
        return jsonify({'recommended_exercises': recommended_exercises_info, 'comment': comment_response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route("/record", methods=['POST'])
def record_exercise_session():
    try:
        data = request.get_json()
        user_id = data['user_id']
        date = data['date']  # Expecting format "YYYY-MM-DD"
        duration = data['duration']
        exercises = data['exercises']  # Expecting a list

        if not (user_id and date and duration and exercises):
            return jsonify({'error': 'Missing required fields'}), 400

        # Parse the date to extract year, month, and day
        year, month, day = date.split('-')  # "YYYY", "MM", "DD"

        # Find the document for the user and year-month
        user_record = collection_Grass.find_one(
            {"user_id": user_id, f"calendar.{year}-{month}": {"$exists": True}}
        )

        if user_record:
            # Check if the day already exists in exercise_sessions
            day_exists = any(
                session['day'] == day for session in user_record['calendar'][f'{year}-{month}']['exercise_sessions']
            )
            
            if day_exists:
                # Update the existing day's duration and exercises
                collection_Grass.update_one(
                    {"user_id": user_id, f"calendar.{year}-{month}.exercise_sessions.day": day},
                    {"$set": {
                        f"calendar.{year}-{month}.exercise_sessions.$.duration": duration,
                        f"calendar.{year}-{month}.exercise_sessions.$.exercises": exercises
                    }}
                )
            else:
                # Append a new session for the day
                collection_Grass.update_one(
                    {"user_id": user_id},
                    {"$push": {
                        f"calendar.{year}-{month}.exercise_sessions": {"day": day, "duration": duration, "exercises": exercises}
                    }}
                )
            message = "Exercise session updated or added successfully"
        else:
            # If the year-month does not exist, create it and add the session
            collection_Grass.update_one(
                {"user_id": user_id},
                {"$set": {
                    f"calendar.{year}-{month}": {
                        "exercise_sessions": [{"day": day, "duration": duration, "exercises": exercises}]
                    }
                }},
                upsert=True
            )
            message = "New month created and exercise session added successfully"

        return jsonify({'message': message}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    3
@app.route("/score", methods=['POST'])
def calculate_score():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        year_month = data.get('date')  # Expecting format "YYYY-MM"

        if not user_id or not year_month:
            return jsonify({'error': 'User ID and date are required'}), 400

        # Retrieve the exercise sessions for the user and month
        user_record = collection_Grass.find_one(
            {"user_id": user_id, f"calendar.{year_month}.exercise_sessions": {"$exists": True}},
            {f"calendar.{year_month}": 1}
        )

        if not user_record or 'calendar' not in user_record or year_month not in user_record['calendar']:
            return jsonify({'error': 'No exercise sessions found'}), 404

        exercise_sessions = user_record['calendar'][year_month]['exercise_sessions']
        total_duration = sum(int(session['duration']) for session in exercise_sessions)
        score = total_duration * 3  # Base score

        # Check for consecutive days and apply multiplier
        consecutive_days = 1
        for i in range(1, len(exercise_sessions)):
            if int(exercise_sessions[i]['day']) == int(exercise_sessions[i - 1]['day']) + 1:
                consecutive_days += 1
            else:
                score += (consecutive_days - 1) * total_duration * 3
                consecutive_days = 1  # Reset counter for new block
        score += (consecutive_days - 1) * total_duration * 3  # Apply multiplier for the last block if any

        # Update the score in collection_Score
        score_entry = collection_Score.find_one({"user_id": user_id})
        if score_entry:
            # Update the existing score record
            collection_Score.update_one(
                {"_id": score_entry['_id'], "calendar.date": year_month},
                {"$set": {"calendar.$.score": score}},
                upsert=True
            )
        else:
            # Insert a new score record if it doesn't exist
            collection_Score.insert_one(
                {"user_id": user_id, "calendar": [{"date": year_month, "score": score}]}
            )

        return jsonify({'message': 'Score calculated and saved successfully', 'score': score}), 200

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
        year_month = f"{year}-{month}"

        # Fetch the exercise sessions for the given user_id and year_month
        user_record = collection_Grass.find_one(
            {"user_id": user_id, f"calendar.{year_month}": {"$exists": True}},
            {f"calendar.{year_month}.exercise_sessions": 1, "_id": 0}
        )

        # Check if the user_record exists and has the specified year_month
        if user_record and year_month in user_record.get('calendar', {}):
            # Extract the exercise_sessions for the specified year_month
            exercise_sessions = user_record['calendar'][year_month]['exercise_sessions']
        else:
            # Return an empty list if no sessions are found
            exercise_sessions = []

        # Return the exercise sessions as JSON
        return jsonify({'exercise_sessions': exercise_sessions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route("/rank", methods=['POST'])
def get_rankings():
    try:
        data = request.get_json()
        app.logger.info(data)  # Using app.logger instead of print
        year = data.get('year')
        month = data.get('month')
        app.logger.info(f"Year: {year}, Month: {month}")

        # Validate incoming data
        if year is None or month is None:
            return jsonify({'error': 'Year and month are required'}), 400

        # Prepare the date query to match the required format "YYYY-MM"
        date_query = f"{year}-{str(month).zfill(2)}"
        app.logger.info(f"Date Query: {date_query}")

        # Fetch only user score records for the given date from collection_Score
        all_score_records = list(collection_Score.find(
            {"calendar": {"$elemMatch": {"date": date_query}}}
        ))
        app.logger.info(f"All Score Records: {all_score_records}")

        user_scores = []

        # Iterate over the score records to find the score for the given month and year
        for record in all_score_records:
            user_id = record.get('user_id')
            # Extract the score for the specified month and year from the calendar
            for calendar_entry in record.get('calendar', []):
                if calendar_entry.get('date') == date_query:
                    user_scores.append({
                        'user_id': user_id,
                        'score': calendar_entry.get('score', 0)
                    })
                    break  # No need to search further in the calendar

        # Sort the user scores list by score in descending order
        sorted_scores = sorted(user_scores, key=lambda k: k['score'], reverse=True)

        # Return the sorted scores as JSON
        final_results = []

        # For each user score, find the user details from collection_User
        for user_score in sorted_scores:
            user_details = collection_User.find_one({'user_id': user_score['user_id']})
            if user_details:
                # Append the user details to the final results
                final_results.append({
                    'user_id': user_score['user_id'],
                    'score': user_score['score'],
                    'nickname': user_details.get('nickname', 'N/A'),  # Default if no nickname
                    'profile_image': user_details.get('profile_image', 'N/A')  # Default if no image
                })
            else:
                # Append only the score if user details are not found
                final_results.append(user_score)

        # Return the final results as JSON
        return jsonify(final_results), 200

    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__': 
    app.run(debug=True, host = "143.248.219.4", port = 8080)


# local : 143.248.219.4
# ec2 : 13.209.98.220
    


