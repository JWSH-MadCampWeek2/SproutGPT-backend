# from flask import Flask, render_template, request, jsonify, make_response
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# import requests
# from flask_pymongo import PyMongo
# from pymongo import MongoClient

# load_dotenv() 

# CLIENT_ID = os.environ.get("CLIENT_ID")
# CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
# REDIRECT_URI = os.environ.get("REDIRECT_URI")
# CLIENT = os.environ.get("CLIENT")


# client = MongoClient(CLIENT)
# db = client['MadCampWeek2']
# collection_Goal = db['Goal']


# # data = [

# # {

# # "user_id": "1234567891",
# # "calendar": [
# #     "2024-01" : 
# # ],

# # },



# # ]

# collection_Goal.insert_many(data)

# client.close()