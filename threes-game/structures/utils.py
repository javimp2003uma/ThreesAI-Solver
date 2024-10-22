import pygame
from enum import Enum

from algorithms import BreadthFirstSearch, DepthFirstSearch, AStar, AStarMax

class GAME_MODES(Enum):
    USER = 0
    IA = 1

class ALGORITHMS(Enum):
    DEPTH_FIRST_SEARCH = 0
    BREADTH_FIRST_SEARCH = 1
    A_STAR = 2
    A_STAR_MAX = 3

class MOVEMENTS(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

ALGORITHM_CLASSES = {
    ALGORITHMS.DEPTH_FIRST_SEARCH: DepthFirstSearch,
    ALGORITHMS.BREADTH_FIRST_SEARCH: BreadthFirstSearch,
    ALGORITHMS.A_STAR: AStar,
    ALGORITHMS.A_STAR_MAX: AStarMax
}

TRANSLATE_MOVES = {
    pygame.K_LEFT: "LEFT",
    pygame.K_RIGHT: "RIGHT",
    pygame.K_UP: "UP",
    pygame.K_DOWN: "DOWN"
}