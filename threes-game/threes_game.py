from enum import Enum
import pygame

from state import State
from algorithms import DepthFirstSearch, BreadthFirstSearch, AStar

import tkinter as tk
from tkinter import font
from PIL import ImageFont, ImageDraw, Image, ImageTk

BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = (204, 192, 179)
TEXT_COLOR = (119, 110, 101)
CELL_SIZE = 100
MARGIN = 10

class GAME_MODES(Enum):
    USER = 0
    IA = 1

class ALGORITHMS(Enum):
    DEPTH_FIRST_SEARCH = 0
    BREADTH_FIRST_SEARCH = 1
    A_STAR = 2

ALGORITHM_CLASSES = {
    ALGORITHMS.DEPTH_FIRST_SEARCH: DepthFirstSearch,
    ALGORITHMS.BREADTH_FIRST_SEARCH: BreadthFirstSearch,
    ALGORITHMS.A_STAR: AStar
}

class ThreeGame:
    
    def __init__(self, seed, game_mode, alg, size=4):
        pygame.init()

        self.seed = seed
        self.game_mode = game_mode

        self.size = size
        self.algorithm = alg
        #self.seed, self.game_mode, self.algorithm = self.askForParameters()

        self.state = State(self.seed)

        self.screen = pygame.display.set_mode((self.size * (CELL_SIZE + MARGIN), self.size * (CELL_SIZE + MARGIN)))
        self.font = pygame.font.Font(None, 55)
        pygame.display.set_caption("Threes Game") 


    
    def draw_grid(self):
        self.screen.fill(BACKGROUND_COLOR)
        for r in range(self.size):
            for c in range(self.size):
                value = self.state.grid[r][c]
                color = CELL_COLOR if value > 0 else BACKGROUND_COLOR
                pygame.draw.rect(self.screen, color, (c * (CELL_SIZE + MARGIN), r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE))
                
                if value != 0:
                    text_surface = self.font.render(str(value), True, TEXT_COLOR)
                    text_rect = text_surface.get_rect(center=(c * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                                                              r * (CELL_SIZE + MARGIN) + CELL_SIZE // 2))
                    self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        
    def run(self):
        MOVES = {
            pygame.K_LEFT: self.state.move_left,
            pygame.K_RIGHT: self.state.move_right,
            pygame.K_UP: self.state.move_up,
            pygame.K_DOWN: self.state.move_down
        }

        running = True
        while running:
            if self.game_mode == GAME_MODES.USER:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        move_func = MOVES[event.key]
                        if move_func is not None:
                            move_func()

                            if self.state.completedState():
                                print("Game Over")
                                running = False

            elif self.game_mode == GAME_MODES.IA:
                pass

            self.draw_grid()

        pygame.quit()

if __name__ == "__main__":
    
    game = ThreeGame()
    game.run()

class QuestionUI:
    def run():
        ventana = tk.Tk()
        ventana.title("THREES by Los Monotonos")
        ventana.config(width=675, height= 600)
        ventana.resizable(False, False)

    
        titulo_programa = tk.Label(text="THREES GAME", font= "arial 30 bold", fg= "black")
        titulo_programa.place(x= 200, y= 20)

        preguntaUser = tk.Label(text="¿Qué modo de juego desea?", font= "arial 15 bold", fg= "black")
        preguntaUser.place(x= 200, y= 100)

        variable = tk.StringVar(ventana)
        variable.set("Elije el quién va a jugar")  # Etiqueta inicial

        inputUser = tk.OptionMenu(ventana, variable, "USER", "IA")
        inputUser.place(x= 200, y= 150)

        preguntaUser = tk.Label(text="Introduzca una semilla", font= "arial 15 bold", fg= "black")
        preguntaUser.place(x= 200, y= 200)

        inputSeed = tk.Entry(ventana, font= "arial 15 bold")
        inputSeed.place(x= 200, y= 250)
        
        preguntaUser = tk.Label(text="¿Qué algoritmo desea utilizar?", font= "arial 15 bold", fg= "black")
        preguntaUser.place(x= 200, y= 300)

        variableAlgorithm = tk.StringVar(ventana)
        variableAlgorithm.set("Elije el algoritmo")

        inputAlgorithm = tk.OptionMenu(ventana, variableAlgorithm, "Depth First Search", "Breadth First Search", "A*")
        inputAlgorithm.place(x= 200, y= 350)

        seed = None
        game_mode = None
        algorithm = None

        def startGame():
            seed = inputSeed.get()
            game_mode_aux = variable.get()
            if game_mode_aux == "USER":
                game_mode = GAME_MODES.USER
            else:
                game_mode = GAME_MODES.IA

            algorithm_aux = variableAlgorithm.get()
            if algorithm_aux == "Depth First Search":
                algorithm = ALGORITHMS.DEPTH_FIRST_SEARCH
            elif algorithm_aux == "Breadth First Search":
                algorithm = ALGORITHMS.BREADTH_FIRST_SEARCH
            else:
                algorithm = ALGORITHMS.A_STAR

            ventana.destroy()

            ThreeGame(seed=seed, game_mode=game_mode, alg=algorithm).run()
        
        boton = tk.Button(
            text="Comenzar Juego",
            command= startGame,
            bg="#4CAF50",  # Background color
            fg="white",    # Text color
            font=("Arial", 14, "bold"),  # Font
            padx=20,  # Padding X
            pady=10   # Padding Y
        )
        boton.place(x= 200, y= 400)
        
        ventana.mainloop()
    


