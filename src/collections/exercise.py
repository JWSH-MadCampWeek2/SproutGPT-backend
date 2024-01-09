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


data =  [
      {
        "name": "벤치 프레스",
        "description": "바벨을 사용하여 가슴을 주로 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "가슴",
        "link": "https://youtu.be/tRdBuUgOb5w?si=IYWNoMkRAwudf--E"
      },
      {
        "name": "컨센트레이션 컬",
        "description": "한 손에 덤벨을 들고, 팔꿈치를 다리에 기대어 이두근에 집중적으로 자극을 주는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://youtu.be/gFGV6OeRckU?si=iv2KXM46ATvVIOQ-"
      },
      {
        "name": "데드리프트",
        "description": "바벨을 들어 올려 전신 근력을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://youtube.com/shorts/Q7FL43F0hQM?si=exA6uVIrfuK4qvyf"
      },
      {
        "name": "스쿼트",
        "description": "바벨을 어깨 뒤에 두고 앉았다 일어서는 운동",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://youtu.be/50f62PSGY7k?si=8JpI5vrv1cxiInw6"
      },
      {
        "name": "풀업",
        "description": "철봉을 잡고 몸을 위로 끌어올리는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://youtu.be/nWhS28U6bCY?si=YdMaZFFum6CfkE9l"
      },
      {
        "name": "밀리터리 프레스",
        "description": "바벨을 머리 위로 들어올리는 어깨 운동",
        "difficulty": ["intermediate"],
        "target": "어깨",
        "link": "https://youtu.be/8DByXGrk4Ps?si=-x7Yxt5ZbQtHdOvD"
      },
      {
        "name": "덤벨 컬",
        "description": "덤벨을 사용하여 이두근을 단련하는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://youtu.be/WYW98dryPLM?si=RuDx4U7AABb-10O5"
      },
      {
        "name": "라잉 트라이셉스 익스텐션",
        "description": "덤벨 또는 바벨을 사용하여 삼두근을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://youtu.be/hbDE-gbAHCY?si=4oVqjqBYEdDp9jZO"
      },
      {
        "name": "크런치",
        "description": "복근 운동의 기본이 되는 바닥 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "복근",
        "link": "https://youtu.be/KqnFav4Edvw?si=x7cCIafJ17is_HZG"
      },
      {
        "name": "플랭크",
        "description": "몸을 곧게 펴고 버티는 운동으로 코어 근육 강화에 좋음",
        "difficulty": ["intermediate","beginner"],
        "target": "복근",
        "link": "https://youtu.be/Zq8nRY9P_cM?si=mqJAoI4oOuRFLIYW"
      },
      {
        "name": "레그 레이즈",
        "description": "바닥에 누워 다리를 들어 올리는 운동으로 하복부 강화에 좋음",
        "difficulty": ["intermediate","beginner"],
        "target": "하복부",
        "link": "https://youtu.be/tObWHCnLkKg?si=KA0oUUdTKcmbq7wA"
      },
      {
        "name": "랫 풀다운",
        "description": "케이블 머신을 사용하여 등 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "등",
        "link": "https://youtu.be/MpVD4WMoewM?si=rOgnIGUP21sR92L6"
      },
      {
        "name": "케이블 시티드 로우",
        "description": "케이블 머신을 사용하여 등 중앙 부위를 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://youtu.be/Tp9VFoSuK_0?si=ivMZ767EWXvYVSjy"
      },
      {
        "name": "사이드 래터럴 레이즈",
        "description": "덤벨을 들고 팔을 옆으로 들어 올리며 어깨를 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "어깨",
        "link": "https://youtu.be/YdhHnZxcpgY?si=ymlPOO6cvByEnnPw"
      },
      {
        "name": "프론트 레이즈",
        "description": "덤벨이나 바벨을 사용하여 어깨 전면을 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "어깨",
        "link": "https://youtu.be/m0ddyws4VL4?si=E_9UzgmxaQVBJbl1"
      },
      {
        "name": "레그 컬",
        "description": "기계를 사용하여 허벅지 뒤쪽 근육을 강화하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://youtu.be/6I0NiRc6yww?si=KFlFBVIYhbxkxbKu"
      },
      {
        "name": "레그 익스텐션",
        "description": "기계를 사용하여 허벅지 앞쪽 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://youtu.be/6P62nYjEMR8?si=5T3MqeZp3Rsb25xI"
      },
      {
        "name": "카프 레이즈",
        "description": "발뒤꿈치를 들어올려 종아리 근육을 강화하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://youtu.be/YmmFMZF8A48?si=cIYToWZjeUPBXiLg"
      },
      {
        "name": "버피",
        "description": "점프, 스쿼트, 플랭크, 푸시업을 결합한 전신 운동",
        "difficulty": ["intermediate"],
        "target": "전신",
        "link": "https://youtu.be/hVPgQT7cZdY?si=TJeLH5Bw6ILO9xmX"
      },
      {
        "name": "덤벨 플라이",
        "description": "덤벨을 사용하여 가슴의 옆부분을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://youtu.be/HcDzxNNrSBo?si=KiwyvOro98WmNusn"
      },
      {
        "name": "바벨 로우",
        "description": "바벨을 들어 등 근육을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://youtu.be/4bx17wuyJ2o?si=ljfPmbNrPBsPjOv6"
      },
      {
        "name": "시티드 레그 프레스",
        "description": "기계를 사용하여 앉은 자세에서 다리를 앞으로 밀어내는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://youtube.com/shorts/6k7fBUE3rec?si=BuWJAqP6IwSZX209"
      },
      {
        "name": "힙 스러스트",
        "description": "바벨과 벤치를 사용하여 엉덩이와 허벅지 뒷부분을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://youtu.be/ZJMOZIE2FYo?si=Ds2OpWeYTiZf9rRW"
      },
      {
        "name": "펙 덱 플라이",
        "description": "기계를 사용하여 가슴 근육을 중앙으로 모으는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://youtu.be/Og9pgOtL-04?si=FK1ym4_cIwdo9t31"
      },
      {
        "name": "인클라인 덤벨 프레스",
        "description": "기울어진 벤치에서 덤벨을 사용하여 상부 가슴 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://youtu.be/FuButPvWEaY?si=nON-nqEcCqUS_8zH"
      },
      {
        "name": "케이블 크로스오버",
        "description": "케이블 머신을 사용하여 가슴 근육을 단련하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "가슴",
        "link": "https://youtu.be/_FUhaghu_ds?si=LZtuh8vNqdMuuGkC"
      },
      {
        "name": "바벨 컬",
        "description": "바벨을 사용하여 이두근을 단련하는 운동",
        "difficulty": ["beginner"],
        "target": "팔",
        "link": "https://youtu.be/mKZ1sxVLrVA?si=XU-06p9qilEReptl"
      },
      {
        "name": "해머 컬",
        "description": "덤벨을 사용하여 이두근과 전완근을 동시에 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://youtube.com/shorts/sLXKGCyPeTY?si=cTDsM4qpcOGFlA2b"
      },
      {
        "name": "덤벨 숄더 프레스",
        "description": "덤벨을 사용하여 어깨 근육을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "어깨",
        "link": "https://youtu.be/Ia9DYFMkMmU?si=9ZIYXIN2q22QwveX"
      },
      {
        "name": "스미스 머신 스쿼트",
        "description": "스미스 머신을 사용하여 안정적으로 스쿼트 운동을 하는 방법",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://youtu.be/xAzWNBmDS-I?si=lYb30w02NN0rHcXO"
      },
      {
        "name": "레그 프레스",
        "description": "다리를 이용해 무게를 밀어내는 하체 근력 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://youtu.be/hYwJrXpzEfs?si=qdxYSI3x7K2Sj76M"
      },
      {
        "name": "스플릿 스쿼트",
        "description": "덤벨을 이용하여 스쿼트 운동을 강화하는 방법",
        "difficulty": ["intermediate"],
        "target": "하체",
        "link": "https://youtube.com/shorts/0OOfgow1q68?si=rlaxoEjwvdHzIJDG"
      },
      {
        "name": "케이블 컬",
        "description": "케이블 머신을 사용하여 이두근을 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://youtu.be/5bPGsV7aTKU?si=VenjCJIurX1QTTQb"
      },
      {
        "name": "트라이셉스 딥스",
        "description": "자신의 체중을 이용해 삼두근과 가슴을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "팔",
        "link": "https://youtube.com/shorts/3jMstQ5bIm0?si=PMOZebAAmpbEavvB"
      },
      {
        "name": "행잉 레그 레이즈",
        "description": "철봉에 매달린 상태에서 다리를 들어올려 복근을 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "복근",
        "link": "https://youtu.be/8qt6isvWSt4?si=cjoItOIYKgDbMzkR"
      },
      {
        "name": "런지",
        "description": "런지 자세를 취하면서 하체 근육을 강화하는 운동",
        "difficulty": ["intermediate","beginner"],
        "target": "하체",
        "link": "https://youtu.be/7erin-2cpRo?si=0x3t2VRXrEWHm51m"
      },
      {
        "name": "암 풀다운",
        "description": "케이블 머신을 사용하여 등 근육을 효과적으로 단련하는 운동",
        "difficulty": ["intermediate"],
        "target": "등",
        "link": "https://youtu.be/C1_Yx8qPXRE?si=Guv2s4Iv7ohncEND"
      },
      {
        "name": "워킹 런지",
        "description": "걸으며 런지 자세를 취하는 기본적인 하체 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://youtu.be/RKzuCDSnFMU?si=GKDR_jNsiK23jv5x"
      },
      {
        "name": "스텝 업",
        "description": "벤치나 계단을 이용하여 하체 근육을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://youtube.com/shorts/zEDecNH4u7k?si=FjF9BlP5Su90hcz6"
      },
      {
        "name": "바이시클 크런치",
        "description": "바닥에 누워 자전거 페달을 밟는 듯한 동작으로 복근을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "복근",
        "link": "https://youtu.be/anoM9iutAuY?si=AnKR9oHACFDlf3uo"
      },
      {
        "name": "푸쉬업",
        "description": "가슴, 어깨, 삼두근을 강화하는 기본적인 상체 운동",
        "difficulty": ["beginner"],
        "target": "가슴",
        "link": "https://youtu.be/-_DUjHxgmWk?si=XtOVzZBOJe0IE3zD"
      },
      {
        "name": "벽 스쿼트",
        "description": "벽에 등을 대고 앉은 자세를 유지하며 하체 근육을 강화하는 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://youtube.com/shorts/GoC2Y5PDZE8?si=yLx2c6NCU8ef4KHa"
      },
      {
        "name": "딥스",
        "description": "평행봉등을  사용하여 삼두근과 가슴을 강화하는 운동",
        "difficulty": ["intermediate"],
        "target": "가슴",
        "link": "https://youtu.be/pQSfXvaQGas?si=FIccDI42SzSPovsV"
      },
      {
        "name": "마운틴 클라이머",
        "description": "플랭크 자세에서 다리를 번갈아 가며 끌어올리는 유산소와 복근 운동",
        "difficulty": ["beginner"],
        "target": "복근",
        "link": "https://youtu.be/FscNBbxpu58?si=w0dBORlxYoDJ0iAp"
      },
      {
        "name": "글루트 브릿지",
        "description": "바닥에 누워 엉덩이를 들어올리는 운동으로 하체와 코어 근육 강화",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://youtu.be/6EGYtkbj_34?si=lBQgTc-Wq9OH6I2l"
      },
      {
        "name": "덤벨 데드리프트",
        "description": "덤벨을 사용하여 등과 하체 근육을 동시에 단련하는 운동",
        "difficulty": ["beginner"],
        "target": "하체",
        "link": "https://youtube.com/shorts/49jK8jelP2c?si=UZj8oYN4JT1nq_rv"
      },
    ]

collection_Exercise.insert_many(data)

client.close()