

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


chat = ChatOpenAI(
    temperature=0.1,
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

    print(4)
    print(exercise_list)
    exercise_string = ", ".join(exercise_list)
    recommend_string = ", ".join(recommend_list)


    # Prepare the chat prompt template
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "너는 사용자가 질문하는 내용을 기반으로 운동의 코멘트를 출력하는 머신이야. 유저가 말하는 정보를 기반으로 유저가 말하는대로 {} 안의 내용을 채우고, 각각을 comma separated list로 출력해줘. 재질문은 하지마."
            ),
            ("human","너가 이 운동을 추천해줬어. 사용자가 {age}세이고 성별은 {gender}이고, 키는 {height}cm이고, 몸무게는 {weight}kg이고, 운동 목표는 {exercise_goal}이야. 사용자는 gpt에게 {exercise_string}들 중에 자신에게 맞는 운동을 선정해달라고 했고, 그 결과는 {recommend_string}이야. 일때 아래 [] 안의 내용을 comma separated list로 적어줘. 다시 재질문하지마.1. 워밍업[여기에 사용자의 상황에 맞게 워밍업을 하는 방법을 적어줘.]2. 운동 선정 이유[여기에 gpt가 운동을 사용자에게 추천해준 이유를 운동마다 간단하게 설명해줘]3. 운동 방법[각 운동의 세트수, 반복 횟수, 운동의 무게를 선정하는 기준을 간단하게 제시해줘. 무게를 제시해줄 수 없으면 이에 대해선 언급하지 말아줘. 세트수, 반복 횟수, 운동의 무게 이외엔 언급하지 말아줘.]4. 유의점[각 운동의 유의점을 간단하게 설명해줘.]")
        ]
    )

  
    chain = template |chat | CommaOutputParser()
    comment_message = chain.invoke({"age":age,"gender":gender,"height":height,"weight":weight,"exercise_goal":exercise_goal,"exercise_string":exercise_string, "recommend_string":recommend_string})
    print(5)
    print(list)
    return comment_message