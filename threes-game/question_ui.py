import tkinter as tk

from algorithms.strategy.more_free_cells_high_value import MoreFreeCellsHighValue
from algorithms.strategy.number_equals import NumberEquals
from algorithms.strategy.dijkstra import Dijkstra
from algorithms.strategy.max_value_and_adjacent import MaxValueAndAdjacent
from algorithms.strategy.max_tiles_combination_potential import MaxTilesCombinationPotential
from algorithms.strategy.max_tile_and_free_cells import MaxTileAndFreeCells 
from algorithms.strategy.max_achievable_minus_current import MaxAchievableMinusCurrentScore
from algorithms.strategy.heuristic_maximize_score import HeuristicMaximizeScore
from algorithms.strategy.min_non_free_cells import MinNonFreeCells
from structures.utils import ALGORITHMS, GAME_MODES

class QuestionUI:
    def run(self):
        ventana = tk.Tk()
        ventana.title("THREES by Los Monotonos")
        ventana.config(width=675, height=600)
        ventana.resizable(False, False)

        titulo_programa = tk.Label(text="THREES GAME", font="arial 30 bold", fg="black")
        titulo_programa.place(x=200, y=20)

        preguntaUser = tk.Label(text="¿Qué modo de juego desea?", font="arial 15 bold", fg="black")
        preguntaUser.place(x=200, y=100)

        variable = tk.StringVar(ventana)
        variable.set("Elije el quién va a jugar")

        inputUser = tk.OptionMenu(ventana, variable, "USER", "IA")
        inputUser.place(x=200, y=150)

        preguntaSeed = tk.Label(text="Introduzca una semilla", font="arial 15 bold", fg="black")
        preguntaSeed.place(x=200, y=200)

        inputSeed = tk.Entry(ventana, font="arial 15 bold")
        inputSeed.place(x=200, y=250)

        variableAlgorithm = tk.StringVar(ventana)
        variableAlgorithm.set("Elije el algoritmo")

        variable_heuristic = tk.StringVar(ventana)
        variable_heuristic.set("Elije la heuristica")

        preguntaAlgorithm = None
        inputAlgorithm = None

        pregunta_heuristic = None
        input_heuristic = None

        def update_algorithm_menu(*args):
            nonlocal preguntaAlgorithm, inputAlgorithm

            if variable.get() == "IA":
                if preguntaAlgorithm is None:
                    preguntaAlgorithm = tk.Label(text="¿Qué algoritmo desea utilizar?", font="arial 15 bold", fg="black")
                    preguntaAlgorithm.place(x=200, y=300)

                if inputAlgorithm is None:
                    inputAlgorithm = tk.OptionMenu(ventana, variableAlgorithm, "Depth First Search", "Breadth First Search", "Greedy Search", "A*")
                    inputAlgorithm.place(x=200, y=350)
            else:
                if preguntaAlgorithm is not None:
                    preguntaAlgorithm.place_forget()
                    preguntaAlgorithm = None

                if inputAlgorithm is not None:
                    inputAlgorithm.place_forget()
                    inputAlgorithm = None

        def update_heuristic_menu(*args):
            nonlocal pregunta_heuristic, input_heuristic

            if variableAlgorithm.get() in ["A*", "Greedy Search"]:
                if pregunta_heuristic is None:
                    pregunta_heuristic = tk.Label(text="¿Qué heuristica desea utilizar?", font="arial 15 bold", fg="black")
                    pregunta_heuristic.place(x=200, y=400)

                if input_heuristic is None:
                    input_heuristic = tk.OptionMenu(ventana, variable_heuristic, "More Free Cells", "Number No Matches", "MaxValueAndAdjacent", "Dijkstra", "MaxTilesCombinationPotencial", "MaxTilesAndFreeCells", "MaxAchievableMinusCurrentScore", "MinNonFreeCells", "maximizescore")
                    input_heuristic.place(x=200, y=450)
            else:
                if pregunta_heuristic is not None:
                    pregunta_heuristic.place_forget()
                    pregunta_heuristic = None

                if input_heuristic is not None:
                    input_heuristic.place_forget()
                    input_heuristic = None

        variable.trace('w', update_algorithm_menu)
        variableAlgorithm.trace('w', update_heuristic_menu)

        def startGame():
            heuristic = None
            seed = inputSeed.get()
            game_mode_aux = variable.get()

            if game_mode_aux == "USER":
                game_mode = GAME_MODES.USER
                algorithm = None
            else:
                game_mode = GAME_MODES.IA
                algorithm_aux = variableAlgorithm.get()
                if algorithm_aux == "Depth First Search":
                    algorithm = ALGORITHMS.DEPTH_FIRST_SEARCH
                elif algorithm_aux == "Breadth First Search":
                    algorithm = ALGORITHMS.BREADTH_FIRST_SEARCH
                else:
                    if algorithm_aux == "A*":
                        algorithm = ALGORITHMS.A_STAR
                    elif algorithm_aux == "Greedy Search":
                        algorithm = ALGORITHMS.GREEDY_SEARCH
                    heuristic_aux = variable_heuristic.get()
                    if heuristic_aux == "More Free Cells":
                        heuristic = MoreFreeCellsHighValue()
                    elif heuristic_aux == "Number No Matches":
                        heuristic = NumberEquals()
                    elif heuristic_aux == "Dijkstra":
                        heuristic = Dijkstra()
                    elif heuristic_aux == "MaxValueAndAdjacent":
                        heuristic = MaxValueAndAdjacent()
                    elif heuristic_aux == "MaxTilesCombinationPotencial":
                        heuristic = MaxTilesCombinationPotential()
                    elif heuristic_aux == "MaxTilesAndFreeCells":
                        heuristic = MaxTileAndFreeCells()
                    elif heuristic_aux == "MaxAchievableMinusCurrentScore":
                        heuristic = MaxAchievableMinusCurrentScore()
                    elif heuristic_aux == "maximizescore":
                        heuristic = HeuristicMaximizeScore()
                    elif heuristic_aux == "MinNonFreeCells":
                        heuristic = MinNonFreeCells()

            # Guardar los valores y cerrar la ventana
            self.result = (game_mode, seed, algorithm, heuristic)
            ventana.destroy()

        boton = tk.Button(
            text="Comenzar Juego",
            command=startGame,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=10
        )
        boton.place(x=200, y=500)

        self.result = None
        ventana.mainloop()

        return self.result
# import tkinter as tk
# import os
# import importlib
# from structures.utils import ALGORITHMS, GAME_MODES

# class QuestionUI:
#     def run(self):
#         ventana = tk.Tk()
#         ventana.title("THREES by Los Monotonos")
#         ventana.config(width=675, height=600)
#         ventana.resizable(False, False)

#         titulo_programa = tk.Label(text="THREES GAME", font="arial 30 bold", fg="black")
#         titulo_programa.place(x=200, y=20)

#         preguntaUser = tk.Label(text="¿Qué modo de juego desea?", font="arial 15 bold", fg="black")
#         preguntaUser.place(x=200, y=100)

#         variable = tk.StringVar(ventana)
#         variable.set("Elije el quién va a jugar")

#         inputUser = tk.OptionMenu(ventana, variable, "USER", "IA")
#         inputUser.place(x=200, y=150)

#         preguntaSeed = tk.Label(text="Introduzca una semilla", font="arial 15 bold", fg="black")
#         preguntaSeed.place(x=200, y=200)

#         inputSeed = tk.Entry(ventana, font="arial 15 bold")
#         inputSeed.place(x=200, y=250)

#         variableAlgorithm = tk.StringVar(ventana)
#         variableAlgorithm.set("Elije el algoritmo")

#         variable_heuristic = tk.StringVar(ventana)
#         variable_heuristic.set("Elije la heuristica")

#         preguntaAlgorithm = None
#         inputAlgorithm = None

#         pregunta_heuristic = None
#         input_heuristic = None

#         # Cargar algoritmos automáticamente
#         strategy_dir = 'algorithms/strategy'  # Cambia esto a tu ruta
#         strategy = {}
#         algorithms_dir = 'algorithms'  # Cambia esto a tu ruta
#         algorithms = {}

#         for filename in os.listdir(algorithms_dir):
#             if filename.endswith('.py') and filename != '__init__.py' and filename != 'heuristic.py':
#                 module_name = filename[:-3]
#                 module = importlib.import_module(f"algorithms.{module_name}")
#                 algorithms[module_name] = module

#         for filename in os.listdir(strategy_dir):
#             if filename.endswith('.py') and filename != '__init__.py' and filename != 'search_algorithm.py':
#                 module_name = filename[:-3]  # Eliminar .py
#                 module = importlib.import_module(f"algorithms.strategy.{module_name}")
#                 strategy[module_name] = module

#         def update_algorithm_menu(*args):
#             nonlocal preguntaAlgorithm, inputAlgorithm

#             if variable.get() == "IA":
#                 if preguntaAlgorithm is None:
#                     preguntaAlgorithm = tk.Label(text="¿Qué algoritmo desea utilizar?", font="arial 15 bold", fg="black")
#                     preguntaAlgorithm.place(x=200, y=300)

#                 if inputAlgorithm is None:
#                     inputAlgorithm = tk.OptionMenu(ventana, variableAlgorithm, *algorithms.keys())
#                     inputAlgorithm.place(x=200, y=350)
#             else:
#                 if preguntaAlgorithm is not None:
#                     preguntaAlgorithm.place_forget()
#                     preguntaAlgorithm = None

#                 if inputAlgorithm is not None:
#                     inputAlgorithm.place_forget()
#                     inputAlgorithm = None

#         def update_heuristic_menu(*args):
#             nonlocal pregunta_heuristic, input_heuristic

#             if variableAlgorithm.get() == "a_star":
#                 if pregunta_heuristic is None:
#                     pregunta_heuristic = tk.Label(text="¿Qué heuristica desea utilizar?", font="arial 15 bold", fg="black")
#                     pregunta_heuristic.place(x=200, y=400)

#                 if input_heuristic is None:
#                     heuristic_options = list(strategy.keys())  # Opciones basadas en los algoritmos cargados
#                     input_heuristic = tk.OptionMenu(ventana, variable_heuristic, *heuristic_options)
#                     input_heuristic.place(x=200, y=450)
#             else:
#                 if pregunta_heuristic is not None:
#                     pregunta_heuristic.place_forget()
#                     pregunta_heuristic = None

#                 if input_heuristic is not None:
#                     input_heuristic.place_forget()
#                     input_heuristic = None

#         variable.trace('w', update_algorithm_menu)
#         variableAlgorithm.trace('w', update_heuristic_menu)

#         def startGame():
#             heuristic = None
#             seed = inputSeed.get()
#             game_mode_aux = variable.get()

#             if game_mode_aux == "USER":
#                 game_mode = GAME_MODES.USER
#                 algorithm = None
#             else:
#                 game_mode = GAME_MODES.IA
#                 algorithm_aux = variableAlgorithm.get()
#                 algorithm = algorithms.get(algorithm_aux)#Esto no funciona

#                 if algorithm is not None and algorithm_aux == "a_star":
#                     heuristic_aux = variable_heuristic.get()
#                     heuristic = strategy.get(heuristic_aux) #Esto no funciona

#             # Guardar los valores y cerrar la ventana
#             self.result = (game_mode, seed, algorithm, heuristic)
#             ventana.destroy()

#         boton = tk.Button(
#             text="Comenzar Juego",
#             command=startGame,
#             bg="#4CAF50",
#             fg="white",
#             font=("Arial", 14, "bold"),
#             padx=20,
#             pady=10
#         )
#         boton.place(x=200, y=500)

#         self.result = None
#         ventana.mainloop()

#         return self.result
