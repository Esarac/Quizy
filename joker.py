import os
import openai
from dotenv import load_dotenv
import random

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

TOPICS = ["minecraft", "valorant", "overwatch", "minions", "among us", "shrek"]

def tell_joke() -> str:
    topic_number = random.randint(0, len(TOPICS)-1)
    gpt_prompt = f"""Tell a joke about dogs:
What breed of dog goes after anything that is red? A Bulldog.
Tell a joke about batman:
What would Batman do if he wasn't rich? He would be Robin.
Tell a joke about {TOPICS[topic_number]}:
"""

    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=gpt_prompt,
        temperature=0.5,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return str(response['choices'][0]['text'].split("\n")[0])