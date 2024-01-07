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
collection_Exercise = db['Exercise']


data = {
    "Exercises": [
      {
        "name": "벤치 프레스",
        "description": "바벨을 사용하여 가슴을 주로 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "가슴",
        "link": "https://example.com/bench-press"
      },
      {
        "name": "컨센트레이션 컬",
        "description": "한 손에 덤벨을 들고, 팔꿈치를 다리에 기대어 이두근에 집중적으로 자극을 주는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://example.com/concentration-curl"
      },
      {
        "name": "데드리프트",
        "description": "바벨을 들어 올려 전신 근력을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://example.com/deadlift"
      },
      {
        "name": "스쿼트",
        "description": "바벨을 어깨 뒤에 두고 앉았다 일어서는 운동",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://example.com/squat"
      },
      {
        "name": "풀업",
        "description": "철봉을 잡고 몸을 위로 끌어올리는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://example.com/pull-up"
      },
      {
        "name": "밀리터리 프레스",
        "description": "바벨을 머리 위로 들어올리는 어깨 운동",
        "difficulty": ["intermediate"],
        "target": "어깨",
        "link": "https://example.com/military-press"
      },
      {
        "name": "덤벨 컬",
        "description": "덤벨을 사용하여 이두근을 단련하는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://example.com/dumbbell-curl"
      },
      {
        "name": "트라이셉스 익스텐션",
        "description": "덤벨 또는 바벨을 사용하여 삼두근을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://example.com/triceps-extension"
      },
      {
        "name": "크런치",
        "description": "복근 운동의 기본이 되는 바닥 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "복근",
        "link": "https://example.com/crunch"
      },
      {
        "name": "플랭크",
        "description": "몸을 곧게 펴고 버티는 운동으로 코어 근육 강화에 좋음",
        "difficulty": ["intermediate","beginner"],
        "target": "복근",
        "link": "https://example.com/plank"
      },
      {
        "name": "레그 레이즈",
        "description": "바닥에 누워 다리를 들어 올리는 운동으로 하복부 강화에 좋음",
        "difficulty": ["intermediate","beginner"],
        "target": "하복부",
        "link": "https://example.com/leg-raise"
      },
      {
        "name": "라트 풀다운",
        "description": "케이블 머신을 사용하여 등 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "등",
        "link": "https://example.com/lat-pulldown"
      },
      {
        "name": "시티드 로우",
        "description": "케이블 머신을 사용하여 등 중앙 부위를 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://example.com/seated-row"
      },
      {
        "name": "덤벨 래터럴 레이즈",
        "description": "덤벨을 들고 팔을 옆으로 들어 올리며 어깨를 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "어깨",
        "link": "https://example.com/dumbbell-lateral-raise"
      },
      {
        "name": "프론트 레이즈",
        "description": "덤벨이나 바벨을 사용하여 어깨 전면을 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "어깨",
        "link": "https://example.com/front-raise"
      },
      {
        "name": "레그 컬",
        "description": "기계를 사용하여 허벅지 뒤쪽 근육을 강화하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://example.com/leg-curl"
      },
      {
        "name": "레그 익스텐션",
        "description": "기계를 사용하여 허벅지 앞쪽 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://example.com/leg-extension"
      },
      {
        "name": "카프 레이즈",
        "description": "발뒤꿈치를 들어올려 종아리 근육을 강화하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://example.com/calf-raise"
      },
      {
        "name": "버피",
        "description": "점프, 스쿼트, 플랭크, 푸시업을 결합한 전신 운동",
        "difficulty": ["intermediate"],
        "target": "전신",
        "link": "https://example.com/burpee"
      },
      {
        "name": "덤벨 플라이",
        "description": "덤벨을 사용하여 가슴의 옆부분을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://example.com/dumbbell-fly"
      },
      {
        "name": "바벨 로우",
        "description": "바벨을 들어 등 근육을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://example.com/barbell-row"
      },
      {
        "name": "시티드 레그 프레스",
        "description": "기계를 사용하여 앉은 자세에서 다리를 앞으로 밀어내는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://example.com/seated-leg-press"
      },
      {
        "name": "힙 스러스트",
        "description": "바벨과 벤치를 사용하여 엉덩이와 허벅지 뒷부분을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://example.com/hip-thrust"
      },
      {
        "name": "펙 덱 플라이",
        "description": "기계를 사용하여 가슴 근육을 중앙으로 모으는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://example.com/pec-deck-fly"
      },
      {
        "name": "인클라인 덤벨 프레스",
        "description": "기울어진 벤치에서 덤벨을 사용하여 상부 가슴 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://example.com/incline-dumbbell-press"
      },
      {
        "name": "케이블 크로스오버",
        "description": "케이블 머신을 사용하여 가슴 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://example.com/cable-crossover"
      },
      {
        "name": "바벨 컬",
        "description": "바벨을 사용하여 이두근을 단련하는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://example.com/barbell-curl"
      },
      {
        "name": "해머 컬",
        "description": "덤벨을 사용하여 이두근과 전완근을 동시에 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://example.com/hammer-curl"
      },
      {
        "name": "덤벨 숄더 프레스",
        "description": "덤벨을 사용하여 어깨 근육을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "어깨",
        "link": "https://example.com/dumbbell-shoulder-press"
      },
      {
        "name": "스미스 머신 스쿼트",
        "description": "스미스 머신을 사용하여 안정적으로 스쿼트 운동을 하는 방법",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://example.com/smith-machine-squat"
      },
      {
        "name": "레그 프레스",
        "description": "다리를 이용해 무게를 밀어내는 하체 근력 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://example.com/leg-press"
      },
      {
        "name": "케이블 킥백",
        "description": "케이블을 이용해 삼두근을 집중적으로 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://example.com/cable-kickback"
      },
      {
        "name": "덤벨 스쿼트",
        "description": "덤벨을 이용하여 전통적인 스쿼트 운동을 강화하는 방법",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://example.com/dumbbell-squat"
      },
      {
        "name": "벤트오버 바벨 로우",
        "description": "상체를 숙이고 바벨을 들어올려 등 근육을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://example.com/bent-over-barbell-row"
      },
      {
        "name": "케이블 바이셉스 컬",
        "description": "케이블 머신을 사용하여 이두근을 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://example.com/cable-biceps-curl"
      },
      {
        "name": "트라이셉스 딥스",
        "description": "자신의 체중을 이용해 삼두근을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://example.com/triceps-dips"
      },
      {
        "name": "행잉 레그 레이즈",
        "description": "철봉에 매달린 상태에서 다리를 들어올려 복근을 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "복근",
        "link": "https://example.com/hanging-leg-raise"
      },
      {
        "name": "덤벨 런지",
        "description": "덤벨을 들고 런지 자세를 취하면서 하체 근육을 강화하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://example.com/dumbbell-lunge"
      },
      {
        "name": "케이블 크로스 풀다운",
        "description": "케이블 머신을 사용하여 등 근육을 효과적으로 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://example.com/cable-cross-pulldown"
      },
      {
        "name": "워킹 런지",
        "description": "걸으며 런지 자세를 취하는 기본적인 하체 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://example.com/walking-lunge"
      },
      {
        "name": "스텝 업",
        "description": "벤치나 계단을 이용하여 하체 근육을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://example.com/step-up"
      },
      {
        "name": "바이시클 크런치",
        "description": "바닥에 누워 자전거 페달을 밟는 듯한 동작으로 복근을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "복근",
        "link": "https://example.com/bicycle-crunch"
      },
      {
        "name": "푸시업",
        "description": "가슴, 어깨, 삼두근을 강화하는 기본적인 상체 운동",
        "difficulty": ["beginner"],
        "target": "가슴",
        "link": "https://example.com/push-up"
      },
      {
        "name": "덤벨 사이드 레이즈",
        "description": "덤벨을 들고 팔을 옆으로 들어 올려 어깨 근육을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "어깨",
        "link": "https://example.com/dumbbell-side-raise"
      },
      {
        "name": "월 시트",
        "description": "벽에 등을 대고 앉은 자세를 유지하며 하체 근육을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://example.com/wall-sit"
      },
      {
        "name": "체어 딥스",
        "description": "의자를 사용하여 삼두근을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://example.com/chair-dips"
      },
      {
        "name": "마운틴 클라이머",
        "description": "플랭크 자세에서 다리를 번갈아 가며 끌어올리는 유산소와 코어 운동",
        "difficulty": ["beginner"],
        "target": "코어",
        "link": "https://example.com/mountain-climber"
      },
      {
        "name": "글루트 브릿지",
        "description": "바닥에 누워 엉덩이를 들어올리는 운동으로 하체와 코어 근육 강화",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://example.com/glute-bridge"
      },
      {
        "name": "덤벨 데드리프트",
        "description": "덤벨을 사용하여 등과 하체 근육을 동시에 단련하는 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://example.com/dumbbell-deadlift"
      }
    ]
}

collection_Exercise.insert_one(data)

client.close()