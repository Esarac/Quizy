import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Quiz:

    def __init__(self, first_player):
        self.players = {first_player}
        self.questions = []
        self.output = "hola"
    
    def __str__(self) -> str:
        return "Este es el quiz"

    def register_player(self, player) -> bool:
        quantity: int = len(self.players)
        self.players.add(player)
        return quantity != len(self.players)


