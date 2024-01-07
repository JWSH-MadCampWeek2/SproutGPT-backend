

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



chat = ChatOpenAI(
    temperature=0.1
)
template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 fittness center에서만 할 수 있는 근력운동 추천 목록을 작성해주는 머신이야. 운동 부위는 {부위}운동이야.너는 나이,성별,키,몸무게,운동목표를 질문받은다음 추천하는 운동을 우선순위대로 5개 생각할거야. 나이는 {age}세고 성별은 {gender}고 키는 {height}cm이고 몸무게는 {weight}kg이고 운동목표는 {exercise_goal}이야. 이를  comma separated list로 출력할거야. ."
        ),
        # ("human","{question}"),
    ]
)

prompt = template.format_messages(age="70",gender="woman",height="170cm",weight="60",exercise_goal="몸매 유지",부위 = "복근")

print(chat.predict_messages(prompt))