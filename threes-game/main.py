from threes_game import QuestionUI

try:
    seed, game_mode, alg = QuestionUI.run()
except TypeError as e:
    pass