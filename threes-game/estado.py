from enum import Enum
import numpy as np
import random as rnd
import pygame

#from algorithms import DepthFirstSearch, BreadFirstSearch, AStar

BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = (204, 192, 179)
TEXT_COLOR = (119, 110, 101)
GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10

class Estado:
    def __init__(self, seed, size=4):
        rnd.seed(seed)

        posx1 = rnd.randint(0, size-1)
        posy1 = rnd.randint(0, size-1)
        posx2 = rnd.randint(0, size-1)
        posy2 = rnd.randint(0, size-1)

        while posx2 == posy2 and posy2 == posy1:
            posy2 = rnd.randint(0, size-1)
            posx2 = rnd.randint(0, size-1)

        # Cuadrícula inicial (NumPy array)
        grid_array = np.zeros((size, size), dtype=int)
        grid_array[posx1][posy1] = 1
        grid_array[posx2][posy2] = 2

        self.grid = np.array(grid_array)
        self.has_merged = np.zeros_like(self.grid)
    
    # Función para mover la cuadrícula hacia la izquierda
    def move_left(self):
        self.has_merged.fill(0)
        for r in range(GRID_SIZE):
            for c in range(1, GRID_SIZE):  # Comenzar desde la segunda columna
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, -1)  # Mover a la izquierda (-1 en la columna)
        self.add_random_tile()


    # Función para mover la cuadrícula hacia la derecha
    def move_right(self):
        self.has_merged.fill(0)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE - 2, -1, -1):  # Comenzar desde la penúltima columna
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 0, 1)  # Mover a la derecha (+1 en la columna)
        self.add_random_tile()


    # Función para mover la cuadrícula hacia arriba
    def move_up(self):
        self.has_merged.fill(0)
        for r in range(1, GRID_SIZE):  # Comenzar desde la segunda fila
            for c in range(GRID_SIZE):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, -1, 0)  # Mover hacia arriba (-1 en la fila)
        self.add_random_tile()


    # Función para mover la cuadrícula hacia abajo
    def move_down(self):
        self.has_merged.fill(0)
        for r in range(GRID_SIZE - 2, -1, -1):  # Comenzar desde la penúltima fila
            for c in range(GRID_SIZE):
                if self.grid[r][c] != 0:
                    self.shift_tile(r, c, 1, 0)  # Mover hacia abajo (+1 en la fila)
        self.add_random_tile()


    # Función para mover una ficha en la dirección dada (delta_row, delta_col)
    def shift_tile(self, r, c, delta_row, delta_col):
        new_r, new_c = r + delta_row, c + delta_col
        if 0 <= new_r < GRID_SIZE and 0 <= new_c < GRID_SIZE:
            # Si la celda de destino está vacía, mueve la ficha
            if self.grid[new_r][new_c] == 0:
                self.grid[new_r][new_c] = self.grid[r][c]
                self.grid[r][c] = 0
            # Si la celda de destino tiene una ficha, intenta fusionar
            elif self.can_merge(self.grid[r][c], self.grid[new_r][new_c]) and not self.has_merged[new_r][new_c]:
                self.grid[new_r][new_c] = self.grid[r][c] + self.grid[new_r][new_c]
                self.grid[r][c] = 0
                self.has_merged[new_r][new_c] = 1  # Marcar como fusionado

    def completedState(self):
        allZeros = False
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    allZeros = True
        if allZeros:
            for r in range(GRID_SIZE):
                for c in range(GRID_SIZE):
                    # complete the code
                    pass

    # Reglas de fusión (1 + 2, 2 + 1, o n + n si n >= 3)
    def can_merge(self, a, b):
        if (a == 1 and b == 2) or (a == 2 and b == 1):
            return True
        if a >= 3 and a == b:
            return True
        return False
    
    # Agrega una ficha en cualquier celda vacía después de un movimiento válido
    def add_random_tile(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            row, col = rnd.choice(empty_cells)
            self.grid[row][col] = rnd.choice([1, 2, 3])  # Insertar ficha aleatoria

class GAME_MODES(Enum):
    USER = 0
    IA = 1

class ALGORITHMS(Enum):
    DEPTH_FIRST_SEARCH = 0
    BREADTH_FIRST_SEARCH = 1
    A_STAR = 2

class ThreeGame:

    def __init__(self):
        pygame.init()

        self.seed, self.game_mode, self.algorithm = self.askForParameters()
        self.state = Estado(self.seed)

        self.screen = pygame.display.set_mode((GRID_SIZE * (CELL_SIZE + MARGIN), GRID_SIZE * (CELL_SIZE + MARGIN)))
        self.font = pygame.font.Font(None, 55)
        pygame.display.set_caption("Threes Game") 

        
        
            
    
    def askForParameters(self):
        
        screen = pygame.display.set_mode((700,700))
        font = pygame.font.Font(None, 25)
        pygame.display.set_caption("Threes Game") 
        
        seed = 0
        game_mode = GAME_MODES.USER
        algorithm = ALGORITHMS.DEPTH_FIRST_SEARCH  # Default value

        input_box_seed = pygame.Rect(50, 50, 140, 32)
        input_box_algorithm = pygame.Rect(50, 150, 140, 32)
        input_box_mode = pygame.Rect(50, 250, 140, 32)
        
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box_seed.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive

                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            try:
                                seed = int(text)  # Convert to integer when the user presses enter
                                text = ''  # Clear the input box
                            except ValueError:
                                text = 'Invalid input'
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                
                # Selecting game mode
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_mode = GAME_MODES.USER
                    elif event.key == pygame.K_2:
                        game_mode = GAME_MODES.IA

                # Selecting algorithm
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        algorithm = ALGORITHMS.A_STAR
                    elif event.key == pygame.K_b:
                        algorithm = ALGORITHMS.BREADTH_FIRST_SEARCH
                    elif event.key == pygame.K_d:
                        algorithm = ALGORITHMS.DEPTH_FIRST_SEARCH

            screen.fill(BACKGROUND_COLOR)
            
            # Render input box for seed
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box_seed.w = width
            screen.blit(txt_surface, (input_box_seed.x + 5, input_box_seed.y + 5))
            pygame.draw.rect(screen, color, input_box_seed, 2)

            # Instructions for game mode
            mode_text = font.render("Press 1 for User or 2 for IA", True, TEXT_COLOR)
            screen.blit(mode_text, (50, 100))

            # Instructions for algorithm
            algo_text = font.render("Press A for A*, B for BFS, D for DFS", True, TEXT_COLOR)
            screen.blit(algo_text, (50, 200))

            # Draw the selected game mode and algorithm
            selected_mode_text = font.render(f"Mode: {game_mode.name}", True, TEXT_COLOR)
            screen.blit(selected_mode_text, (50, 300))

            selected_algo_text = font.render(f"Algorithm: {algorithm.name}", True, TEXT_COLOR)
            screen.blit(selected_algo_text, (50, 350))

            pygame.display.flip()

        return seed, game_mode, algorithm

    
    def draw_grid(self):
        self.screen.fill(BACKGROUND_COLOR)
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                value = self.state.grid[r][c]
                color = CELL_COLOR if value > 0 else BACKGROUND_COLOR
                pygame.draw.rect(self.screen, color,
                                 (c * (CELL_SIZE + MARGIN), r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE))
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
                        if event.key in MOVES:
                            if self.state.completedState():
                                print("Game Over")
                                running = False
                            MOVES[event.key]()
            elif self.game_mode == GAME_MODES.IA:
                pass

            self.draw_grid()

        pygame.quit()

if __name__ == "__main__":
    
    game = ThreeGame()
    game.run()
