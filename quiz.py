import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Question:
    def __init__(self, player: str, question: str):
        self.player: str = player
        self.question: str = question
        self.answers: dict[str,str] = {}

    def answer_question(self, player: str, answer: str) -> bool:
        added: bool = False
        if not (player in self.answers.keys()):
            self.answers[player] = answer
            added = True
        return added

    @property
    def answer(self) -> str:
        return self.answers[self.player]

class Quiz:

    def __init__(self, first_player: str):
        self.__players: set[str] = {first_player}
        self.__questions: list[Question] = []
        self.__answered_questions: list[Question] = []
        self.__rounds: int = 0
        self.__started: bool = False
    
    def __str__(self) -> str:
        information =f"**Players:** {', '.join(self.__players)}"
        if self.__started:
            information += f"\n**Rounds:** {str(self.__rounds)}"
            information += f"\n**Started**"
        
        return information

    #Methods
    def register_player(self, player: str) -> bool:
        quantity: int = len(self.__players)
        if not self.__started:
            self.__players.add(player)
        return quantity != len(self.__players)

    def init_match(self, rounds: int) -> bool:
        inited: bool = False

        if (not self.__started) and (len(self.__players) > 1) and (rounds >= 1):
            inited = True
            self.__rounds = rounds
            for r in range(self.__rounds):
                self.__questions += [Question(x, "**What kind of music do you enjoy the most?**\n**A.** Rock\n**B.** Electronic\n**C.** Sad music\n**D.** Rap") for x in self.__players]
            self.__started = True
        
        return inited
    
    def answer_question(self, player: str, answer: str) -> bool:
        answered: bool = False
        if self.__started and (len(self.__questions) >= 1):
            if player in self.players:
                answered = self.__questions[0].answer_question(player, answer)
                if (len(self.actual_question().answers) == len(self.players)):
                    self.__answered_questions.append(self.__questions.pop(0))
        return answered

    def actual_question(self) -> Question:
        actual: Question = None
        if self.__started and (len(self.__questions) >= 1):
            actual = self.__questions[0]
        return actual
    
    def scores(self) -> dict[str, int]:
        scores: dict[str, int] = {i:0 for i in self.players}
        for question in self.__answered_questions:
            for player in self.players:
                if player != question.player:
                    if question.answers[player] == question.answer:
                        scores[player] += 1
        return scores
    
    # Properties
    @property
    def players(self) -> set[str]:
        return self.__players
    
    @property
    def questions(self) -> list[Question]:
        return self.__answered_questions + self.__questions

    @property
    def rounds(self) -> int:
        return self.__rounds

    @property
    def started(self) -> bool:
        return self.__started
    
    @property
    def ended(self) -> bool:
        return self.started and (len(self.__questions) == 0)
