import pygame
import time

from state import State
from structures.utils import GAME_MODES, TRANSLATE_MOVES, ALGORITHM_CLASSES

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

class ThreeGame:
    
    def __init__(self, seed, game_mode, alg, heu, size=4, headless=False):
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

        if not headless:self.draw_grid()

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

    def run(self, headless=False):
        points = 0
        if not headless: print(f"Running the game with parameters: {self.seed}, {self.game_mode}, {self.algorithm}")
        
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
                                points = self.show_points_window()
                                running = False

                self.draw_grid() 
        elif self.game_mode == GAME_MODES.IA:
            start_time = time.time()
            algorithm_class = ALGORITHM_CLASSES[self.algorithm](self.state, self.heuristic, headless= headless)
            if not headless: print(f"Secuencia de movimientos hasta el camino óptimo:\n {[TRANSLATE_MOVES[move] for move in algorithm_class.moves_list]}")

            while running:
                next_move = algorithm_class.get_next_move()
                if next_move is not None:
                    translated_move = TRANSLATE_MOVES[next_move]
                    if not headless: print(f"({algorithm_class.it}/{len(algorithm_class.moves_list)}) IA Mueve: {TRANSLATE_MOVES[next_move]}")

                    self.state.move(translated_move)
                    if self.state.completed_state():
                        if headless:
                            end_time = time.time()
                            points = self.state.total_points()
                            pygame.quit()
                            return points, end_time - start_time
                        else:
                            points = self.show_points_window()                        
                            running = False

                    if not headless : self.draw_grid() 
                    else: None
                else:
                    running = False
                    print("Ha habido algún error, no hay mas movimientos pero no se ha llegado al estado final")

                time.sleep(0.25) # 4 movs / s