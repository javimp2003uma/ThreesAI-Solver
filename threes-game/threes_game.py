from enum import Enum
import pygame

from state import State
from algorithms import BreadthFirstSearch, DepthFirstSearch, AStar
from structures.node import TRANSLATE_MOVES
from algorithms.strategy.more_free_cells_high_value import MoreFreeCellsHighValue
from algorithms.strategy.number_equals import NumberEquals
from algorithms.strategy.max_tile_and_free_cells import MaxTileAndFreeCells
from algorithms.strategy.max_value_and_adjacent import MaxValueAndAdjacent

import tkinter as tk
import time

BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR_ONES = (241, 103, 128)
CELL_COLOR_TWOS = (114, 202, 242)
CELL_COLOR_NUMBER = (255, 255, 255)
CELL_COLOR_DEFAULT = (219, 247, 255)
TEXT_COLOR_DARK = (76, 76, 76)
TEXT_COLOR_LIGHT = (255, 255, 255)
CELL_SIZE = 100
MARGIN = 10
NEXT_NUM_SPACE = 150

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
    
    def __init__(self, seed, game_mode, alg, heu, size=4):
        pygame.init()

        self.seed = seed
        self.game_mode = game_mode
        
        self.size = size
        self.algorithm = alg

        self.state = State(self.seed)

        self.heuristic = heu

        self.screen = pygame.display.set_mode((self.size * (CELL_SIZE + MARGIN) + NEXT_NUM_SPACE, self.size * (CELL_SIZE + MARGIN)))
        self.font = pygame.font.Font(None, 55)
        pygame.display.set_caption("Threes Game") 

        self.draw_grid()

    def draw_grid(self):
        self.screen.fill(BACKGROUND_COLOR)
        for r in range(self.size):
            for c in range(self.size):
                value = self.state.grid[r][c]
                color = (
                            CELL_COLOR_ONES if value == 1 else
                            CELL_COLOR_TWOS if value == 2 else
                            tuple(max(0, int(c * max(0.1, 1 - value / 100))) for c in CELL_COLOR_NUMBER)
                            if value > 2 else CELL_COLOR_DEFAULT
                        )
                pygame.draw.rect(self.screen, color, (c * (CELL_SIZE + MARGIN), r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE))
                
                if value != 0:
                    text_surface = self.font.render(str(value), True, TEXT_COLOR_LIGHT if value <= 2 or value > 40 else TEXT_COLOR_DARK)
                    text_rect = text_surface.get_rect(center=(c * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                                                              r * (CELL_SIZE + MARGIN) + CELL_SIZE // 2))
                    self.screen.blit(text_surface, text_rect)
        
        label_font = pygame.font.Font(None, 25)
        next_num_font = pygame.font.Font(None, 35)

        label_surf = label_font.render("Próximo número", True, CELL_COLOR_ONES)
        label_rect = label_surf.get_rect(center=(self.size * (CELL_SIZE + MARGIN) + (NEXT_NUM_SPACE - MARGIN) // 2, self.size * (CELL_SIZE + MARGIN) // 2 - 10))

        next_num_surf = next_num_font.render(f"{self.state.next_number}", True, CELL_COLOR_ONES)
        next_num_rect = next_num_surf.get_rect(center=(self.size * (CELL_SIZE + MARGIN) + (NEXT_NUM_SPACE - MARGIN) // 2, self.size * (CELL_SIZE + MARGIN) // 2 + 10))

        pygame.draw.rect(
            self.screen, 
            CELL_COLOR_DEFAULT, 
            (self.size * (CELL_SIZE + MARGIN) - 2, 
             self.size * (CELL_SIZE + MARGIN) // 2 - 25,
            NEXT_NUM_SPACE - MARGIN + 5,
             50)
        )


        self.screen.blits([
            (label_surf, label_rect),
            (next_num_surf, next_num_rect)
        ])
        

        pygame.display.flip()
    
    
    def show_points_window(self):
        # Borrar el contenido de la pantalla
        self.screen.fill(BACKGROUND_COLOR)  # Limpia el fondo de la pantalla

        # Crear una nueva fuente para el mensaje de error
        font = pygame.font.Font(None, 34)  # Ajusta el tamaño según sea necesario

        # Renderizar las líneas de texto
        puntosTotales = round(self.state.total_points(),2)
        line1 = font.render("Juego Terminado", True, TEXT_COLOR_DARK)
        line2 = font.render(f"Has logrado un total de {puntosTotales} puntos", True, TEXT_COLOR_DARK)

        # Obtener el rectángulo para centrar el texto
        rect1 = line1.get_rect(center=((self.size * (CELL_SIZE + MARGIN) + NEXT_NUM_SPACE) // 2, 
                                        (self.size * (CELL_SIZE + MARGIN)) // 2 - 20))  # Ajusta la posición vertical
        rect2 = line2.get_rect(center=((self.size * (CELL_SIZE + MARGIN) + NEXT_NUM_SPACE) // 2, 
                                        (self.size * (CELL_SIZE + MARGIN)) // 2 + 20))  # Ajusta la posición vertical

        # Bucle para esperar hasta que se cierre la ventana
        waiting = True
        blink_timer = 0  # Temporizador para el parpadeo
        show_text = True  # Variable para mostrar/ocultar el texto

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False

            # Actualizar el temporizador y alternar la visibilidad del texto
            blink_timer += 1
            if blink_timer % 5 == 0:  # Cambia la velocidad del parpadeo aquí
                show_text = not show_text

            # Borrar el fondo
            self.screen.fill(BACKGROUND_COLOR)

            # Dibujar el texto en la pantalla si show_text es True
            if show_text:
                self.screen.blit(line1, rect1)
                self.screen.blit(line2, rect2)

            pygame.display.flip()  # Actualiza la pantalla para mostrar el mensaje
            pygame.time.delay(100)

        pygame.quit()  # Cierra la ventana de Pygame    
        QuestionUI.run() #Vuelve a la ventana de preguntas

    def run(self):
        print(f"Running the game with parameters: {self.seed}, {self.game_mode}, {self.algorithm}")
        
        MOVES = {
            pygame.K_LEFT: "LEFT",
            pygame.K_RIGHT: "RIGHT",
            pygame.K_UP: "UP",
            pygame.K_DOWN: "DOWN"
        }

        running = True
        if self.game_mode == GAME_MODES.USER:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key in MOVES.keys():
                            move_dir = MOVES[event.key]
                            self.state.move(move_dir)
                            
                            if self.state.completed_state():
                                self.show_points_window()
                                running = False

                self.draw_grid()
        elif self.game_mode == GAME_MODES.IA:
            algorithm_class = ALGORITHM_CLASSES[self.algorithm](self.state, self.heuristic)
            print(f"Secuencia de movimientos hasta el camino óptimo:\n {[TRANSLATE_MOVES[move] for move in algorithm_class.moves_list]}")
            # hablar con el profe lo de arriba porque vaya mierdon lo del random

            while running:
                
                for moves in algorithm_class.moves_list:
                    time.sleep(0.25) # Frecuencia de la IA
                    move = TRANSLATE_MOVES[moves]
                    self.state.move(move)      
                    if self.state.completed_state():
                        self.show_points_window()
                        running = False

                    self.draw_grid()
                #next_move = algorithm_class.get_next_move()
                #print(f"({algorithm_class.it}/{len(algorithm_class.moves_list)}) IA Mueve: {TRANSLATE_MOVES[next_move]}")

                #move_func = MOVES[next_move]
                #move_func()

                #if self.state.completed_state():
                #    self.mostrarErrorVentana()
                #    running = False

                # next_state, next_move = algorithm_class.get_next_state()
                # if next_state is not None:
                #     self.state = next_state
                #     print(f"({algorithm_class.it}/{len(algorithm_class.moves_list)}) IA Mueve: {TRANSLATE_MOVES[next_move]}")
                #     self.draw_grid()
                # else: # Juego terminado
                #     self.show_points_window()
                #     running = False

if __name__ == "__main__":
    
    game = ThreeGame()
    game.run()

class QuestionUI:
    def run():
        ventana = tk.Tk()
        ventana.title("THREES by Los Monotonos")
        ventana.config(width=675, height=600)
        ventana.resizable(False, False)

        titulo_programa = tk.Label(text="THREES GAME", font="arial 30 bold", fg="black")
        titulo_programa.place(x=200, y=20)

        preguntaUser = tk.Label(text="¿Qué modo de juego desea?", font="arial 15 bold", fg="black")
        preguntaUser.place(x=200, y=100)

        variable = tk.StringVar(ventana)
        variable.set("Elije el quién va a jugar")  # Etiqueta inicial

        inputUser = tk.OptionMenu(ventana, variable, "USER", "IA")
        inputUser.place(x=200, y=150)

        preguntaSeed = tk.Label(text="Introduzca una semilla", font="arial 15 bold", fg="black")
        preguntaSeed.place(x=200, y=200)

        inputSeed = tk.Entry(ventana, font="arial 15 bold")
        inputSeed.place(x=200, y=250)

        # Inicializamos variableAlgorithm aquí para que sea accesible desde cualquier función
        variableAlgorithm = tk.StringVar(ventana)
        variableAlgorithm.set("Elije el algoritmo")

        variable_heuristic = tk.StringVar(ventana)
        variable_heuristic.set("Elije la heuristica")

        # Lugar donde agregaremos dinámicamente el menú de algoritmos
        preguntaAlgorithm = None
        inputAlgorithm = None

        # Lugar donde agregaremos dinámicamente el menú de Heuristicas
        pregunta_heuristic = None
        input_heuristic = None

        def update_algorithm_menu(*args):
            nonlocal preguntaAlgorithm, inputAlgorithm

            # Si el usuario elige "IA", mostramos el menú de algoritmos
            if variable.get() == "IA":
                if preguntaAlgorithm is None:
                    preguntaAlgorithm = tk.Label(text="¿Qué algoritmo desea utilizar?", font="arial 15 bold", fg="black")
                    preguntaAlgorithm.place(x=200, y=300)

                if inputAlgorithm is None:
                    inputAlgorithm = tk.OptionMenu(ventana, variableAlgorithm, "Depth First Search", "Breadth First Search", "A*")
                    inputAlgorithm.place(x=200, y=350)
            else:
                # Si se elige "USER", eliminamos el menú de algoritmos (si está visible)
                if preguntaAlgorithm is not None:
                    preguntaAlgorithm.place_forget()
                    preguntaAlgorithm = None

                if inputAlgorithm is not None:
                    inputAlgorithm.place_forget()
                    inputAlgorithm = None

        def update_heuristic_menu(*args):
            nonlocal pregunta_heuristic, input_heuristic

            # Si el usuario elige "IA", mostramos el menú de algoritmos
            if variableAlgorithm.get() == "A*":
                if pregunta_heuristic is None:
                    pregunta_heuristic = tk.Label(text="¿Qué heuristica desea utilizar?", font="arial 15 bold", fg="black")
                    pregunta_heuristic.place(x=200, y=400)

                if input_heuristic is None:
                    input_heuristic = tk.OptionMenu(ventana, variable_heuristic, "More Free Cells", "Number No Matches", "MaxValueAndAdjacent", "test")
                    input_heuristic.place(x=200, y=450)
            else:
                # Si se elige "USER", eliminamos el menú de algoritmos (si está visible)
                if pregunta_heuristic is not None:
                    pregunta_heuristic.place_forget()
                    pregunta_heuristic = None

                if input_heuristic is not None:
                    input_heuristic.place_forget()
                    input_heuristic = None

        # Actualizar el menú de algoritmos cuando cambie la selección del modo de juego
        variable.trace('w', update_algorithm_menu)
        variableAlgorithm.trace('w', update_heuristic_menu)

        def startGame():
            global heuristic
            heuristic = None
            seed = inputSeed.get()
            game_mode_aux = variable.get()

            # Obtener el modo de juego
            if game_mode_aux == "USER":
                game_mode = GAME_MODES.USER
                algorithm = None
            else:
                game_mode = GAME_MODES.IA
                algorithm_aux = variableAlgorithm.get()  # Ahora variableAlgorithm está definido globalmente
                if algorithm_aux == "Depth First Search":
                    algorithm = ALGORITHMS.DEPTH_FIRST_SEARCH
                    heuristic = None
                elif algorithm_aux == "Breadth First Search":
                    algorithm = ALGORITHMS.BREADTH_FIRST_SEARCH
                    heuristic = None
                else:
                    algorithm = ALGORITHMS.A_STAR
                    heuristic_aux = variable_heuristic.get()
                    if heuristic_aux == "More Free Cells":
                        heuristic = MoreFreeCellsHighValue()
                    elif heuristic_aux == "Number No Matches":
                        heuristic = NumberEquals()
                    elif heuristic_aux == "test":
                        heuristic = MaxTileAndFreeCells()
                    elif heuristic_aux == "MaxValueAndAdjacent":
                        heuristic = MaxValueAndAdjacent()


            
            print(f"Los parametros de juegos seleccionados son: {game_mode}, {seed}, {algorithm}")

            ventana.destroy()

            ThreeGame(seed=seed, game_mode=game_mode, alg=algorithm, heu=heuristic).run()

        boton = tk.Button(
            text="Comenzar Juego",
            command=startGame,
            bg="#4CAF50",  # Background color
            fg="white",  # Text color
            font=("Arial", 14, "bold"),  # Font
            padx=20,  # Padding X
            pady=10  # Padding Y
        )
        boton.place(x=200, y=500)

        ventana.mainloop()