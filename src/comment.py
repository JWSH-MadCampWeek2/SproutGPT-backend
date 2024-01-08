

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.schema import BaseOutputParser
import os

class CommaOutputParser(BaseOutputParser):
    def parse(self,text):
        item = text.strip().split(",")
        return list(map(str.strip,item))

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI trained to assist with exercise routines. Provide concise comments on exercises when requested. Do not re-ask questions but use the provided information to give helpful responses."
        ),
        (
            "human",
            "I need feedback on my exercise routine. I'm {age} years old, {gender}, {height} cm tall, weigh {weight} kg, and my goal is {exercise_goal}. I told GPT to pick suitable exercises from {exercise_string}, and it chose {recommend_string}. Can you give me a quick rundown on the exercises? 한글로 써줘. 그리고 써줄때 형식은 운동명 : 설명, 운동명 : 설명, 이런식으로 써줘."
        )
    ]
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

def comment(age, gender, height, weight, exercise_goal, exercise_list, recommend_list):

    chat_ = ChatOpenAI(
    temperature=0.1,
    # model="gpt-4",
)
    try:
        exercise_string = ", ".join(exercise_list)
        recommend_string = ", ".join(recommend_list)

        # Pass the formatted string into the chat prompt template
        prompt = template.format_messages(age=age, gender=gender, height=height, weight=weight, exercise_goal=exercise_goal, exercise_string=exercise_string, recommend_string=recommend_string)
        
        # Invoke the OpenAI Chat model
        chat_response = chat_.invoke(prompt)
        print(chat_response)
        
        return chat_response
    except Exception as e:
        error_message = str(e) or "An error occurred during the AI response generation."
        print(error_message)
        return {"error": error_message}