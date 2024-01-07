

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser
import os

class CommaOutputParser(BaseOutputParser):

    def parse(self,text):
        item = text.strip().split(",")
        return list(map(str.strip,item))

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

# age = 20
# gender = "man"
# height = 173
# weight = 73
# exercise_goal = "체중 감량"


# excercise_list = [
#     "덤벨 컬",
#     "크런치",
#     "플랭크",
#     "카프 레이즈",
#     "바벨 컬",
#     "바이시클 크런치",
#     "푸시업",
#     "덤벨 사이드 레이즈",
#     "월 시트",
#     "체어 딥스"
# ]

# exercise_string = ", ".join(excercise_list)

chat = ChatOpenAI(
    temperature=0.1,
    model="gpt-4-0613",
)
# template = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "너는 운동 추천 머신이야. 너가 해야할 것은 사용자의 나이, 성별, 키, 몸무게, 운동 목표를 기반으로 사용자가 보내준 하고싶은 운동 목록중에 사용자에게 잘 맞는 운동을 4개 선별해서 출력해줄거야. 다음 양식을 꼭 지켜서 출력해줘. [첫번 째 운동,두번 째 운동,세번 째 운동,네번 째 운동]"
#         ),
#         ("human","나는 {age}세의 {gender}야. 내 키는 {height}cm이고, 몸무게는 {weight}이야. 내가 운동으로 얻고싶은 목표는  {exercise_goal}이야. 내가 하고싶은 운동은  {exercise_list} 이것들이야. 이 운동들 중에 나에게 맞는 운동을 4개 추천해줘."),
#     ]
# )

# prompt = template.format_messages(age=age,gender=gender,height=height,weight=weight,exercise_goal=exercise_goal,exercise_list=exercise_string)

def recommendation(age, gender, height, weight, exercise_goal, exercise_list):
    exercise_string = ", ".join(exercise_list)

    # Prepare the chat prompt template
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an exercise recommendation machine. Based on the user's age, gender, height, weight, and exercise goal, select 4 suitable exercises from the list provided by the user. Output the exercises in the following format: [First Exercise, Second Exercise, Third Exercise, Fourth Exercise]."
            ),
            ("human", f"I am a {age} year old {gender}. My height is {height} cm, and my weight is {weight} kg. My exercise goal is {exercise_goal}. The exercises I am interested in are {exercise_string}. Please recommend four exercises that suit me.")
        ]
    )

    # Format the chat prompt
    prompt = template.format_messages()
    response = chat.predict_messages(prompt)

    # Parse the response to get the list of exercises
    parser = CommaOutputParser()
    recommended_exercises = parser.parse(response)
    return recommended_exercises