import tkinter as tk
import random as rnd
from algorithms.strategy.more_free_cells_high_value import MoreFreeCellsHighValue
from algorithms.strategy.number_equals import NumberEquals
from algorithms.strategy.dijkstra import Dijkstra
from algorithms.strategy.max_value_and_adjacent import MaxValueAndAdjacent
from algorithms.strategy.max_tiles_combination_potential import MaxTilesCombinationPotential
from algorithms.strategy.max_tile_and_free_cells import MaxTileAndFreeCells 
from algorithms.strategy.max_achievable_minus_current import MaxAchievableMinusCurrentScore
from algorithms.strategy.min_non_free_cells import MinNonFreeCells
from algorithms.strategy.max_move_cells_and_fusion import MaxMoveCellsAndFusion 
from structures.utils import ALGORITHMS, GAME_MODES

class QuestionUI:
    """User interface for selecting game mode and algorithm in the THREES game."""

    def run(self):
        """Initializes and runs the Tkinter window for game settings."""
        ventana = tk.Tk()
        ventana.title("THREES by Los Monotonos")
        ventana.config(width=675, height=600)
        ventana.resizable(False, False)

        # Title and prompts
        tk.Label(text="THREES GAME", font="arial 30 bold", fg="black").place(x=200, y=20)
        tk.Label(text="¿Qué modo de juego desea?", font="arial 15 bold", fg="black").place(x=200, y=100)

        # Game mode selection
        variable = tk.StringVar(ventana, "Elije el quién va a jugar")
        tk.OptionMenu(ventana, variable, "USER", "IA").place(x=200, y=150)

        # Seed input
        tk.Label(text="Introduzca una semilla", font="arial 15 bold", fg="black").place(x=200, y=200)
        inputSeed = tk.Entry(ventana, font="arial 15 bold")
        inputSeed.place(x=200, y=250)
        inputSeed.insert(0, rnd.randint(0, 100000))

        # Algorithm and heuristic variables
        variableAlgorithm = tk.StringVar(ventana, "Elije el algoritmo")
        variable_heuristic = tk.StringVar(ventana, "Elije la heuristica")

        preguntaAlgorithm = None
        inputAlgorithm = None
        pregunta_heuristic = None
        input_heuristic = None

        # Update algorithm menu based on game mode selection
        def update_algorithm_menu(*args):
            nonlocal preguntaAlgorithm, inputAlgorithm

            if variable.get() == "IA":
                if preguntaAlgorithm is None:
                    preguntaAlgorithm = tk.Label(text="¿Qué algoritmo desea utilizar?", font="arial 15 bold", fg="black")
                    preguntaAlgorithm.place(x=200, y=300)

                if inputAlgorithm is None:
                    inputAlgorithm = tk.OptionMenu(ventana, variableAlgorithm, 
                        "Depth First Search", "Breadth First Search", "Greedy Search", "A*", "A* Modified")
                    inputAlgorithm.place(x=200, y=350)
            else:
                if preguntaAlgorithm:
                    preguntaAlgorithm.place_forget()
                    preguntaAlgorithm = None

                if inputAlgorithm:
                    inputAlgorithm.place_forget()
                    inputAlgorithm = None
                # Start game button
                tk.Button(
                    text="Comenzar Juego",
                    command=startGame,
                    bg="#4CAF50",
                    fg="white",
                    font=("Arial", 14, "bold"),
                    padx=20,
                    pady=10
                ).place(x=200, y=500)

            

        # Update heuristic menu based on algorithm selection
        def update_heuristic_menu(*args):
            nonlocal pregunta_heuristic, input_heuristic

            if variableAlgorithm.get() in ["A*", "Greedy Search"]:
                if pregunta_heuristic is None:
                    pregunta_heuristic = tk.Label(text="¿Qué heuristica desea utilizar?", font="arial 15 bold", fg="black")
                    pregunta_heuristic.place(x=200, y=400)

                if input_heuristic is None:
                    input_heuristic = tk.OptionMenu(ventana, variable_heuristic, 
                        "More Free Cells", "Number No Matches", "MaxValueAndAdjacent", "Dijkstra", 
                        "MaxTilesCombinationPotencial", "MaxTilesAndFreeCells", 
                        "MaxAchievableMinusCurrentScore", "MinNonFreeCells" , "MaxMoveCellsAndFusion")
                    input_heuristic.place(x=200, y=450)
            else:
                if pregunta_heuristic:
                    pregunta_heuristic.place_forget()
                    pregunta_heuristic = None

                if input_heuristic:
                    input_heuristic.place_forget()
                    input_heuristic = None
                # Start game button
                tk.Button(
                    text="Comenzar Juego",
                    command=startGame,
                    bg="#4CAF50",
                    fg="white",
                    font=("Arial", 14, "bold"),
                    padx=20,
                    pady=10
                ).place(x=200, y=500)
            
        def show_start_button(*args):
        # Start game button
            tk.Button(
                text="Comenzar Juego",
                command=startGame,
                bg="#4CAF50",
                fg="white",
                font=("Arial", 14, "bold"),
                padx=20,
                pady=10
            ).place(x=200, y=500)
        
        # Trace changes in selection variables
        variable.trace_add('write', update_algorithm_menu)
        variableAlgorithm.trace_add('write', update_heuristic_menu)
        variable_heuristic.trace_add('write', show_start_button)

        def startGame():
            """Starts the game with selected settings."""
            heuristic = None
            seed = inputSeed.get()
            game_mode_aux = variable.get()

            if game_mode_aux == "USER":
                game_mode = GAME_MODES.USER
                algorithm = None
            else:
                game_mode = GAME_MODES.IA
                algorithm_aux = variableAlgorithm.get()
                algorithm = self.get_algorithm(algorithm_aux)
                heuristic = self.get_heuristic(variable_heuristic.get())

            # Save settings and close window
            self.result = (game_mode, seed, algorithm, heuristic)
            ventana.destroy()

        self.result = None

        def on_closing():
            """Handles the window closing event."""
            ventana.destroy()

        ventana.protocol("WM_DELETE_WINDOW", on_closing)
        ventana.mainloop()

        return self.result if self.result else (None, None, None, None)

    def get_algorithm(self, algorithm_name):
        """Maps algorithm names to their respective classes."""
        mapping = {
            "Depth First Search": ALGORITHMS.DEPTH_FIRST_SEARCH,
            "Breadth First Search": ALGORITHMS.BREADTH_FIRST_SEARCH,
            "A*": ALGORITHMS.A_STAR,
            "A* Modified": ALGORITHMS.A_STAR_MODIFIED,
            "Greedy Search": ALGORITHMS.GREEDY_SEARCH
        }
        return mapping.get(algorithm_name)

    def get_heuristic(self, heuristic_name):
        """Maps heuristic names to their respective classes."""
        mapping = {
            "More Free Cells": MoreFreeCellsHighValue(),
            "Number No Matches": NumberEquals(),
            "Dijkstra": Dijkstra(),
            "MaxValueAndAdjacent": MaxValueAndAdjacent(),
            "MaxTilesCombinationPotencial": MaxTilesCombinationPotential(),
            "MaxTilesAndFreeCells": MaxTileAndFreeCells(),
            "MaxAchievableMinusCurrentScore": MaxAchievableMinusCurrentScore(),
            "MinNonFreeCells": MinNonFreeCells(),
            "MaxMoveCellsAndFusion": MaxMoveCellsAndFusion()
        }
        return mapping.get(heuristic_name)
