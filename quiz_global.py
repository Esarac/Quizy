import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Quiz:

    def __init__(self, topic):
        gpt_prompt = "Create a multiple choices (A,B,C,D) quiz of 5 questions, about {topic}. Show the answers at the end of each question.".format(topic = topic)

        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=gpt_prompt,
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        self.questions = []
        self.output = response['choices'][0]['text']