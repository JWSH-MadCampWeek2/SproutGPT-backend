from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)



class User(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    exercise_goal = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % self.email
    
    def add_or_update_user(email, gender, age, height, weight, exercise_goal):
        user = User.query.get(email)
        if user is None:
            user = User(email=email, gender=gender, age=age, height=height, weight=weight, exercise_goal=exercise_goal)
            db.session.add(user)
        else:
            user.gender = gender
            user.age = age
            user.height = height
            user.weight = weight
            user.exercise_goal = exercise_goal
        db.session.commit()
    


