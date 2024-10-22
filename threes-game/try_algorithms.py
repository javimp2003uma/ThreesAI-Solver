from question_ui import QuestionUI
import random as rd

from algorithms.strategy.more_free_cells_high_value import MoreFreeCellsHighValue
from algorithms.strategy.number_equals import NumberEquals
from algorithms.strategy.dijkstra import Dijkstra
from algorithms.strategy.max_value_and_adjacent import MaxValueAndAdjacent
from algorithms.strategy.max_tiles_combination_potential import MaxTilesCombinationPotential
from algorithms.strategy.max_tile_and_free_cells import MaxTileAndFreeCells 
from algorithms.strategy.max_achievable_minus_current import MaxAchievableMinusCurrentScore
from algorithms.strategy.min_non_free_cells import MinNonFreeCells
from algorithms.strategy.max_move_cells_and_fusion import MaxMoveCellsAndFusion

from threes_game import ThreeGame
from structures.utils import ALGORITHMS, GAME_MODES

seeds = []

for i in range(int(input("Introduce el número de semillas: "))):
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
    
    three_game6 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxValueAndAdjacent(), headless=True)
    points6, time6 = three_game6.run(headless=True)
    
    three_game7 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxTilesCombinationPotential(), headless=True)
    points7, time7 = three_game7.run(headless=True)
    
    three_game8 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxAchievableMinusCurrentScore(), headless=True)
    points8, time8 = three_game8.run(headless=True)
    
    three_game9 = ThreeGame(seed, GAME_MODES.IA, ALGORITHMS.A_STAR, heu=MaxMoveCellsAndFusion(), headless=True)
    points9, time9 = three_game9.run(headless=True)
    

    print("--------------------------------------------------------------------")
    print("Semilla: ", seed, '\n')
    print("MaxTilesAndFreeCells: Puntos: ", points2, ' Tiempo: ', time2, '\n')
    print("MoreFreeCells Puntos: ", points3, ' Tiempo: ', time3, '\n')
    print("Number No Matches: Puntos: ", points4, ' Tiempo: ', time4, '\n')
    print("MAxValueAndAdjacent: Puntos:  ", points6, ' Tiempo: ', time6, '\n')
    print("MaxTilesCombinationPotencial: Puntos: ", points7, ' Tiempo: ', time7, '\n')
    print("MaxAchievableMinusCurrentScore: Puntos: ", points8, ' Tiempo: ', time8, '\n')
    print("MaxMoveCellsAndFusion: Puntos: ", points9, ' Tiempo: ', time9, '\n')
    print("DFS: Puntos: ", points1, ' Tiempo: ', time1, '\n')
    print("--------------------------------------------------------------------")