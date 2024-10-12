from question_ui import QuestionUI
from threes_game import ThreeGame

while True:
    try:
        question_ui = QuestionUI()
        game_mode, seed, algorithm, heuristic = question_ui.run()

        three_game = ThreeGame(seed, game_mode, algorithm, heuristic)
        three_game.run()
    except TypeError as e:
        pass