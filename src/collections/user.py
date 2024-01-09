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
collection_User = db['User']


data =  [
      {
        "name": "벤치 프레스",
        "description": "바벨을 사용하여 가슴을 주로 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "가슴",
        "link": "https://youtu.be/tRdBuUgOb5w?si=IYWNoMkRAwudf--E"
      },
    ]

collection_User.insert_many(data)

client.close()