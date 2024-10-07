from threes_game import QuestionUI

try:
    seed, game_mode, alg, heuristic = QuestionUI.run()
except TypeError as e:
    pass