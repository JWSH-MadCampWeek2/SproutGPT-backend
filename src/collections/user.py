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


data = [

{

"user_id": "1234567891",

"nickname": "이상혁",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "28",

"gender": "남자",

"height": "173",

"weight": "65",


},
{

"user_id": "1234567892",

"nickname": "최우제",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "21",

"gender": "남자",

"height": "178",

"weight": "73",


},
{

"user_id": "1234567893",

"nickname": "문현준",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "23",

"gender": "남자",

"height": "180",

"weight": "78",


},
{

"user_id": "1234567894",

"nickname": "이민형",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "23",

"gender": "남자",

"height": "182",

"weight": "85",


},
{

"user_id": "1234567895",

"nickname": "류민석",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "23",

"gender": "남자",

"height": "168",

"weight": "60",


},
{

"user_id": "1234567896",

"nickname": "하니",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "20",

"gender": "여자",

"height": "162",

"weight": "48",


},
{

"user_id": "1234567897",

"nickname": "민지",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "20",

"gender": "여자",

"height": "169",

"weight": "52",


},
{

"user_id": "1234567898",

"nickname": "해린",

"profile_image": "http://k.kakaocdn.net/dn/1G9kp/btsAot8liOn/8CWudi3uy07rvFNUkk3ER0/img_640x640.jpg",

"age": "28",

"gender": "여자",

"height": "165",

"weight": "49",


},

]

collection_User.insert_many(data)

client.close()