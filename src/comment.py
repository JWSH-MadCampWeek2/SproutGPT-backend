

from dotenv import load_dotenv
from flask import app
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
            "You are an AI designed to provide personalized fitness advice. When recommending exercises, directly reference the user's age, gender, height, weight, and fitness goals to explain why you've chosen specific routines. Also, clearly articulate how to determine the appropriate number of sets, reps, and weight for each exercise in a way that’s easy for beginners to understand in korean and in under 150 characters"
        ),
        (
            "human",
            "I'm {age} years old, a {gender} who is {height} cm tall and weighs {weight} kg, aiming to {exercise_goal}. Based on this, why did you recommend {recommend_string} from the list {exercise_string}? Please explain clearly, considering my personal information, how to decide on the number of sets, repetitions, and the weight to use for each exercise."
        )
    ]
)
# template = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "hi",
#         ),
#         (
#             "human",
#             "hi"
#         )
#     ]
# )


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

        return chat_response
    except Exception as e:
        error_message = str(e) or "An error occurred during the AI response generation."
        app.logger.error(error_message)
        return {"error": error_message}
    
    #     if 'choices' in chat_response and chat_response['choices']:
    #         response_text = chat_response['choices'][0].get('message', {}).get('content', '')
    #         app.logger.info(f"Chat Response: {response_text}")
    #         return response_text  # Returns the actual string response
    #     else:
    #         error_message = "No response found in chat_response."
    #         app.logger.error(error_message)
    #         return {"error": error_message}
    # except Exception as e:
    #     error_message = str(e) or "An error occurred during the AI response generation."
    #     app.logger.error(error_message)
    #     return {"error": error_message}