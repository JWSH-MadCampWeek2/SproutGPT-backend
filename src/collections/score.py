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
collection_Score = db['Score']


data = [
{
"user_id": "1234567891",
"calendar": [
    {"date" : "2024-01" ,
     "score" : 5000,},
],
},
{
"user_id": "1234567892",
"calendar": [
    {"date" : "2024-01" ,
     "score" : 330,},
],
},{
"user_id": "1234567893",
"calendar": [
    {"date" : "2024-01" ,
     "score" : 351,},
],
},{
"user_id": "1234567894",
"calendar": [
    {"date" : "2024-01" ,
     "score" : 342,},
],
},{
"user_id": "1234567895",
"calendar": [
    {"date" : "2024-01",
     "score" : 331,},
],
},{
"user_id": "1234567896",
"calendar": [
    {"date" : "2024-01",
     "score" : 315,},
],
},{
"user_id": "1234567897",
"calendar": [
    {"date" : "2024-01",
     "score" : 317,},
],
},{
"user_id": "1234567898",
"calendar": [
    {"date" : "2024-01",
     "score" : 373,},
],
},




]

collection_Score.insert_many(data)

client.close()