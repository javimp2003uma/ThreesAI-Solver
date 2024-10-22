import pygame
from enum import Enum

from algorithms import BreadthFirstSearch, DepthFirstSearch, GreedySearch, AStar, AStarModified

class GAME_MODES(Enum):
    USER = 0
    IA = 1

class ALGORITHMS(Enum):
    DEPTH_FIRST_SEARCH = 0
    BREADTH_FIRST_SEARCH = 1
    GREEDY_SEARCH = 2
    A_STAR = 3
    A_STAR_MODIFIED = 4

class MOVEMENTS(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

ALGORITHM_CLASSES = {
    ALGORITHMS.DEPTH_FIRST_SEARCH: DepthFirstSearch,
    ALGORITHMS.BREADTH_FIRST_SEARCH: BreadthFirstSearch,
    ALGORITHMS.GREEDY_SEARCH: GreedySearch,
    ALGORITHMS.A_STAR: AStar,
    ALGORITHMS.A_STAR_MODIFIED: AStarModified
}

TRANSLATE_MOVES = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN"
}