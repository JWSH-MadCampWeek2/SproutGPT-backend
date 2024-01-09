from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
from flask_pymongo import PyMongo
from pymongo import MongoClient

load_dotenv() 

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
CLIENT = os.environ.get("CLIENT")


client = MongoClient(CLIENT)
db = client['MadCampWeek2']
collection_Goal = db['Goal']


data = [

{

"user_id": "1234567892",

"difficulty" : "beginner",

"exercise_goal" : "현재 상태 유지",

"target" : ["가슴","등"],

},
{

"user_id": "1234567893",

"difficulty" : "intermediate",

"exercise_goal" : "근육 증가",

"target" : ["등","가슴","팔","하체"],

},{

"user_id": "1234567894",

"difficulty" : "beginner",

"exercise_goal" : "체지방 감소",

"target" : ["복근",],

},{

"user_id": "1234567895",

"difficulty" : "beginner",

"exercise_goal" : "현재 상태 유지",

"target" : ["팔",],

},{

"user_id": "1234567896",

"difficulty" : "beginner",

"exercise_goal" : "체중 감소",

"target" : ["복근",],

},{

"user_id": "1234567897",

"difficulty" : "intermediate",

"exercise_goal" : "근육 증가",

"target" : ["등","가슴","복근"],

},{

"user_id": "1234567898",

"difficulty" : "beginner",

"exercise_goal" : "현재 상태 유지",

"target" : ["등","복근"],

},


]

collection_Goal.insert_many(data)

client.close()