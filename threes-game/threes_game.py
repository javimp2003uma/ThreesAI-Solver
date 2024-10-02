from enum import Enum
import pygame

from state import State
from algorithms import DepthFirstSearch, BreadthFirstSearch, AStar

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
    
    def __init__(self, size=4):
        pygame.init()

        self.size = size
        self.seed, self.game_mode, self.algorithm = self.askForParameters()

        self.state = State(self.seed)

        self.screen = pygame.display.set_mode((self.size * (CELL_SIZE + MARGIN), self.size * (CELL_SIZE + MARGIN)))
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
