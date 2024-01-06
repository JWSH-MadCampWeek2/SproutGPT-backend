from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os
# db 생성
load_dotenv()
user_id = os.getenv("USER_ID")
user_pwd = os.getenv("USER_PWD")
mongo = PyMongo()

app = Flask(__name__)
app.config['MONGO_URI'] = f'mongodb+srv://sspringson:{user_pwd}@madcampweek2.kdhm8ha.mongodb.net/testdb?retryWrites=true&w=majority'

mongo.init_app(app)

testdb = mongo.db.testdb


@app.route('/')
def main():
    # context = testdb.find()
    context = list(testdb.find())
    return render_template('index.html',context=context)



if __name__ == '__main__':
    app.run(debug=True)
