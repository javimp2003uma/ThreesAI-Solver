from enum import Enum
import pygame

from state import State
from algorithms import BreadthFirstSearch, DepthFirstSearch, AStar
from structures.node import TRANSLATE_MOVES

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

        self.state = State(self.seed)

        self.screen = pygame.display.set_mode((self.size * (CELL_SIZE + MARGIN), self.size * (CELL_SIZE + MARGIN)))
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

        pygame.display.flip()
    
    
    def mostrarErrorVentana(self):
        # Borrar el contenido de la pantalla
        self.screen.fill(BACKGROUND_COLOR)  # Limpia el fondo de la pantalla

        # Crear una nueva fuente para el mensaje de error
        font = pygame.font.Font(None, 34)  # Ajusta el tamaño según sea necesario

        # Renderizar las líneas de texto
        puntosTotales = round(self.state.total_points(),2)
        line1 = font.render("Juego Terminado", True, TEXT_COLOR_DARK)
        line2 = font.render(f"Has logrado un total de {puntosTotales} puntos", True, TEXT_COLOR_DARK)

        # Obtener el rectángulo para centrar el texto
        rect1 = line1.get_rect(center=(self.size * (CELL_SIZE + MARGIN) // 2, 
                                        self.size * (CELL_SIZE + MARGIN) // 2 - 20))  # Ajusta la posición vertical
        rect2 = line2.get_rect(center=(self.size * (CELL_SIZE + MARGIN) // 2, 
                                        self.size * (CELL_SIZE + MARGIN) // 2 + 20))  # Ajusta la posición vertical

        # Bucle para esperar hasta que se cierre la ventana
        waiting = True
        blink_timer = 0  # Temporizador para el parpadeo
        show_text = True  # Variable para mostrar/ocultar el texto

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

    def run(self):
        print(f"Running the game with parameters: {self.seed}, {self.game_mode}, {self.algorithm}")
        
        MOVES = {
            pygame.K_LEFT: self.state.move_left,
            pygame.K_RIGHT: self.state.move_right,
            pygame.K_UP: self.state.move_up,
            pygame.K_DOWN: self.state.move_down
        }

        running = True
        if self.game_mode == GAME_MODES.USER:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key in MOVES.keys():
                            move_func = MOVES[event.key]
                            move_func()
                            
                            if self.state.completed_state():
                                self.mostrarErrorVentana()
                                running = False

                self.draw_grid()
        elif self.game_mode == GAME_MODES.IA:
            algorithm_class = ALGORITHM_CLASSES[self.algorithm](self.state)
            # print(f"Secuencia de movimientos hasta el camino óptimo:\n {[TRANSLATE_MOVES[move] for move in algorithm_class.moves_list]}")
            # hablar con el profe lo de arriba porque vaya mierdon lo del random

            while running:
                time.sleep(0.25) # Frecuencia de la IA

                #next_move = algorithm_class.get_next_move()
                #print(f"({algorithm_class.it}/{len(algorithm_class.moves_list)}) IA Mueve: {TRANSLATE_MOVES[next_move]}")

                #move_func = MOVES[next_move]
                #move_func()

                #if self.state.completed_state():
                #    self.mostrarErrorVentana()
                #    running = False

                next_state, next_move = algorithm_class.get_next_state()
                if next_state is not None:
                    self.state = next_state
                    print(f"({algorithm_class.it}/{len(algorithm_class.moves_list)}) IA Mueve: {TRANSLATE_MOVES[next_move]}")
                    self.draw_grid()
                else: # Juego terminado
                    self.mostrarErrorVentana()
                    running = False

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

        # Lugar donde agregaremos dinámicamente el menú de algoritmos
        preguntaAlgorithm = None
        inputAlgorithm = None

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

        # Actualizar el menú de algoritmos cuando cambie la selección del modo de juego
        variable.trace('w', update_algorithm_menu)

        def startGame():
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
                elif algorithm_aux == "Breadth First Search":
                    algorithm = ALGORITHMS.BREADTH_FIRST_SEARCH
                else:
                    algorithm = ALGORITHMS.A_STAR
            
            print(f"Los parametros de juegos seleccionados son: {game_mode}, {seed}, {algorithm}")

            ventana.destroy()

            ThreeGame(seed=seed, game_mode=game_mode, alg=algorithm).run()

        boton = tk.Button(
            text="Comenzar Juego",
            command=startGame,
            bg="#4CAF50",  # Background color
            fg="white",  # Text color
            font=("Arial", 14, "bold"),  # Font
            padx=20,  # Padding X
            pady=10  # Padding Y
        )
        boton.place(x=200, y=400)

        ventana.mainloop()