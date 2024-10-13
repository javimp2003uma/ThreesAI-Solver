from question_ui import QuestionUI
import random as rd

from algorithms.strategy.more_free_cells_high_value import MoreFreeCellsHighValue
from algorithms.strategy.number_equals import NumberEquals
from algorithms.strategy.dijkstra import Dijkstra
from algorithms.strategy.max_value_and_adjacent import MaxValueAndAdjacent
from algorithms.strategy.max_tiles_combination_potential import MaxTilesCombinationPotential
from algorithms.strategy.max_tile_and_free_cells import MaxTileAndFreeCells 

from threes_game import ThreeGame
from structures.utils import ALGORITHMS, GAME_MODES

seeds = []

for i in range(input("Introduce el número de semillas: ")):
    seeds.append(rd.randint(0, 100000))

for seed in seeds:
    three_game1 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.DEPTH_FIRST_SEARCH, heu=None, headless=True)
    points1, time1 = three_game1.run(headless=True)
    three_game2 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxTileAndFreeCells(), headless=True)
    points2, time2 = three_game2.run(headless=True)
    three_game3 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MoreFreeCellsHighValue(), headless=True)
    points3, time3 = three_game3.run(headless=True)
    three_game4 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=NumberEquals(), headless=True)
    points4, time4 = three_game4.run(headless=True)
    three_game5 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=Dijkstra(), headless=True)
    points5, time5 = three_game5.run(headless=True)
    three_game6 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxValueAndAdjacent(), headless=True)
    points6, time6 = three_game6.run(headless=True)
    three_game7 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxTilesCombinationPotential(), headless=True)
    points7, time7 = three_game7.run(headless=True)


    print("Semilla: ", seed, '\n')
    print("MaxTilesAndFreeCells: Puntos: ", points2, ' Tiempo: ', time2, '\n')
    print("MoreFreeCells ", points3, ' Tiempo: ', time3, '\n')
    print("Number No Matches ", points4, ' Tiempo: ', time4, '\n')
    print("Dijkstra ", points5, ' Tiempo: ', time5, '\n')
    print("MAxValueAndAdjacent ", points6, ' Tiempo: ', time6, '\n')
    print("MaxTilesCombinationPotencial", points7, ' Tiempo: ', time7, '\n')
    print("DFS", points1, ' Tiempo: ', time1, '\n')