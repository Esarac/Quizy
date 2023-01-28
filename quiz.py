import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Quiz:

    def __init__(self, first_player: str):
        self.players: dict = {first_player: 0}
        self.questions: list = []
        self.rounds: int = 0

        self.__started: bool = False
    
    def __str__(self) -> str:
        information =f"**Players:** {', '.join(self.players)}"
        if self.__started:
            information += f"\n**Rounds:** {str(self.rounds)}"
            information += f"\n**Started**"
        
        return information

    def register_player(self, player: str) -> bool:
        if not self.__started:
            quantity: int = len(self.players)
            self.players[player] = 0
        return quantity != len(self.players)

    def init_match(self, rounds: int) -> bool:
        inited: bool = False

        if (not self.__started) and (len(self.players) > 1):
            inited = True
            self.rounds = 3
            for r in range(self.rounds):
                self.questions += [(x, "**What kind of music do you enjoy the most?**\n**A.** Rock\n**B.** Electronic\n**C.** Sad music\n**D.** Rap") for x in self.players]
            self.__started = True
        
        return inited
    
    def pop_question(self) -> tuple:
        if self.__started and (len(self.questions) > 0):
            return self.questions.pop(0)
    
    def answer_question(self, player: str, answer: str) -> bool: #No implemented
        return True
    
    def started(self):
        return self.__started
