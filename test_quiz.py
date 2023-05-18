from quiz import Quiz

def test_init_match():
    quiz = Quiz("Esteban")
    assert not quiz.init_match(2)
    assert not quiz.started

    quiz.register_player("Johan")
    assert not quiz.init_match(0)
    assert not quiz.started

    assert quiz.init_match(2)
    assert quiz.started
    assert len(quiz.questions) == 4

    assert not quiz.init_match(2)
    assert quiz.started

def test_register_player():
    quiz = Quiz("Esteban")
    assert len(quiz.players) == 1

    assert quiz.register_player("Johan")
    assert len(quiz.players) == 2

    assert not quiz.register_player("Johan")
    assert len(quiz.players) == 2

    quiz.init_match(2)

    assert not quiz.register_player("Mateo")
    assert len(quiz.players) == 2

def test_answer_question():
    quiz = Quiz("Esteban")
    quiz.register_player("Johan")
    quiz.register_player("Mateo")

    quiz.init_match(1)

    actual_question = quiz.actual_question()
    assert quiz.answer_question("Esteban","A")
    assert quiz.answer_question("Johan","B")
    assert not quiz.answer_question("Samuel","C")
    assert not quiz.answer_question("Johan","D")
    assert actual_question == quiz.actual_question()
    assert quiz.answer_question("Mateo","A")
    assert actual_question != quiz.actual_question()

    actual_question = quiz.actual_question()
    assert quiz.answer_question("Esteban","D")
    assert quiz.answer_question("Johan","C")
    assert not quiz.answer_question("Samuel","C")
    assert not quiz.answer_question("Johan","D")
    assert actual_question == quiz.actual_question()
    assert quiz.answer_question("Mateo","C")
    assert actual_question != quiz.actual_question()

    actual_question = quiz.actual_question()
    assert quiz.answer_question("Esteban","B")
    assert quiz.answer_question("Johan","A")
    assert not quiz.answer_question("Samuel","C")
    assert not quiz.answer_question("Johan","D")
    assert actual_question == quiz.actual_question()
    assert quiz.answer_question("Mateo","D")
    assert actual_question != quiz.actual_question()

    actual_question = quiz.actual_question()
    assert not actual_question
    assert not quiz.answer_question("Esteban","A")
    assert quiz.ended

    given_answers = quiz.questions[0].answers
    assert len(given_answers) == 3
    assert given_answers["Esteban"] == "A"
    assert given_answers["Johan"] == "B"
    assert given_answers["Mateo"] == "A"

    given_answers = quiz.questions[1].answers
    assert len(given_answers) == 3
    assert given_answers["Esteban"] == "D"
    assert given_answers["Johan"] == "C"
    assert given_answers["Mateo"] == "C"

    given_answers = quiz.questions[2].answers
    assert len(given_answers) == 3
    assert given_answers["Esteban"] == "B"
    assert given_answers["Johan"] == "A"
    assert given_answers["Mateo"] == "D"

def test_scores():
    def answer_factory(quiz: Quiz):
        actual_player = quiz.actual_question().player
        if actual_player == "Esteban":
            quiz.answer_question("Esteban","A")
            quiz.answer_question("Johan","A")
            quiz.answer_question("Mateo","B")
        elif actual_player == "Johan":
            quiz.answer_question("Esteban","B")
            quiz.answer_question("Johan","A")
            quiz.answer_question("Mateo","C")
        elif actual_player == "Mateo":
            quiz.answer_question("Esteban","D")
            quiz.answer_question("Johan","D")
            quiz.answer_question("Mateo","D")

    quiz = Quiz("Esteban")
    quiz.register_player("Johan")
    quiz.register_player("Mateo")

    assert quiz.question_index() == -1
    assert quiz.question_relative_index() == -1
    assert quiz.round_index() == -1

    quiz.init_match(2)

    assert quiz.question_index() == 0
    assert quiz.question_relative_index() == 0
    assert quiz.round_index() == 0

    answer_factory(quiz)

    assert quiz.question_index() == 1
    assert quiz.question_relative_index() == 1
    assert quiz.round_index() == 0

    answer_factory(quiz)

    assert quiz.question_index() == 2
    assert quiz.question_relative_index() == 2
    assert quiz.round_index() == 0

    answer_factory(quiz)

    scores = quiz.scores()
    assert scores["Esteban"] == 1
    assert scores["Johan"] == 2
    assert scores["Mateo"] == 0

    assert quiz.question_index() == 3
    assert quiz.question_relative_index() == 0
    assert quiz.round_index() == 1

    answer_factory(quiz)

    assert quiz.question_index() == 4
    assert quiz.question_relative_index() == 1
    assert quiz.round_index() == 1

    answer_factory(quiz)

    assert quiz.question_index() == 5
    assert quiz.question_relative_index() == 2
    assert quiz.round_index() == 1

    answer_factory(quiz)

    scores = quiz.scores()
    assert scores["Esteban"] == 2
    assert scores["Johan"] == 4
    assert scores["Mateo"] == 0

    assert quiz.question_index() == -1
    assert quiz.question_relative_index() == -1
    assert quiz.round_index() == -1