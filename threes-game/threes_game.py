import pygame
import time
from state import State
from structures.utils import GAME_MODES, TRANSLATE_MOVES, ALGORITHM_CLASSES

# Colors for the game interface
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR_ONES = (241, 103, 128)
CELL_COLOR_TWOS = (114, 202, 242)
CELL_COLOR_NUMBER = (255, 255, 255)
CELL_COLOR_DEFAULT = (219, 247, 255)
TEXT_COLOR_DARK = (76, 76, 76)
TEXT_COLOR_LIGHT = (255, 255, 255)

# Cell sizes and margins
CELL_SIZE = 100
MARGIN = 10
NEXT_NUM_SPACE = 150

class ThreeGame:
    """
    Class representing the Threes game.

    This class manages the game initialization, drawing the interface,
    and game logic.
    """

    def __init__(self, seed, game_mode, alg, heu, size=4, headless=False):
        """
        Initialize the Threes game.

        Args:
            seed: Seed for the state generator.
            game_mode: Game mode (user or AI).
            alg: Algorithm to use for AI.
            heu: Heuristic to use for AI.
            size: Size of the board (default 4).
            headless: Indicates whether to run without a graphical interface.
        """
        pygame.init()
        self.seed = seed
        self.game_mode = game_mode
        self.size = size
        self.algorithm = alg
        self.state = State(self.seed)
        self.heuristic = heu
        self.screen = pygame.display.set_mode(
            (self.size * (CELL_SIZE + MARGIN) + NEXT_NUM_SPACE, self.size * (CELL_SIZE + MARGIN))
        )
        self.font = pygame.font.Font(None, 55)
        pygame.display.set_caption("Threes Game")

        if not headless:
            self.draw_grid()

    def draw_grid(self):
        """
        Draw the game grid on the screen.

        This method renders the cells and their respective values on the board.
        """
        self.screen.fill(BACKGROUND_COLOR)
        for r in range(self.size):
            for c in range(self.size):
                value = self.state.grid[r][c]
                # Determine the color of the cell based on its value
                color = self.get_cell_color(value)
                pygame.draw.rect(self.screen, color,
                                 (c * (CELL_SIZE + MARGIN), r * (CELL_SIZE + MARGIN), CELL_SIZE, CELL_SIZE))
                if value != 0:
                    self.draw_cell_value(value, c, r)

        self.draw_next_number_info()
        pygame.display.flip()

    def get_cell_color(self, value):
        """
        Get the color for a cell based on its value.

        Args:
            value: The value of the cell.

        Returns:
            Color tuple for the cell.
        """
        if value == 1:
            return CELL_COLOR_ONES
        elif value == 2:
            return CELL_COLOR_TWOS
        elif value > 2:
            return tuple(max(0, int(c * max(0.1, 1 - value / 100))) for c in CELL_COLOR_NUMBER)
        return CELL_COLOR_DEFAULT

    def draw_cell_value(self, value, col, row):
        """
        Draw the value of a cell on the screen.

        Args:
            value: The value to display in the cell.
            col: The column index of the cell.
            row: The row index of the cell.
        """
        text_surface = self.font.render(str(value), True,
                                         TEXT_COLOR_LIGHT if value <= 2 or value > 40 else TEXT_COLOR_DARK)
        text_rect = text_surface.get_rect(
            center=(col * (CELL_SIZE + MARGIN) + CELL_SIZE // 2,
                    row * (CELL_SIZE + MARGIN) + CELL_SIZE // 2)
        )
        self.screen.blit(text_surface, text_rect)

    def draw_next_number_info(self):
        """
        Draw the next number information and the seed on the screen.
        """
        label_font = pygame.font.Font(None, 25)
        next_num_font = pygame.font.Font(None, 35)

        # Draw the seed label and value
        seed_label_surf = label_font.render("Seed", True, CELL_COLOR_ONES)
        seed_label_rect = seed_label_surf.get_rect(
            center=(self.size * (CELL_SIZE + MARGIN) + (NEXT_NUM_SPACE - MARGIN) // 2,
                    self.size * (CELL_SIZE + MARGIN) // 2 - 40)
        )
        seed_value_surf = label_font.render(f"{self.seed}", True, CELL_COLOR_ONES)
        seed_value_rect = seed_value_surf.get_rect(
            center=(self.size * (CELL_SIZE + MARGIN) + (NEXT_NUM_SPACE - MARGIN) // 2,
                    self.size * (CELL_SIZE + MARGIN) // 2 - 20)
        )

        # Draw the "Next Number" label and value
        label_surf = label_font.render("Next Number", True, CELL_COLOR_ONES)
        label_rect = label_surf.get_rect(
            center=(self.size * (CELL_SIZE + MARGIN) + (NEXT_NUM_SPACE - MARGIN) // 2,
                    self.size * (CELL_SIZE + MARGIN) // 2 + 10)
        )
        next_num_surf = next_num_font.render(f"{self.state.next_number}", True, CELL_COLOR_ONES)
        next_num_rect = next_num_surf.get_rect(
            center=(self.size * (CELL_SIZE + MARGIN) + (NEXT_NUM_SPACE - MARGIN) // 2,
                    self.size * (CELL_SIZE + MARGIN) // 2 + 30)
        )

        # Draw background rectangle for text
        pygame.draw.rect(
            self.screen,
            CELL_COLOR_DEFAULT,
            (self.size * (CELL_SIZE + MARGIN) - 2,
            self.size * (CELL_SIZE + MARGIN) // 2 - 55,
            NEXT_NUM_SPACE - MARGIN + 5, 110)
        )

        # Blit the seed, "Next Number" label, and next number value
        self.screen.blits([
            (seed_label_surf, seed_label_rect),
            (seed_value_surf, seed_value_rect),
            (label_surf, label_rect),
            (next_num_surf, next_num_rect)
        ])


    def show_points_window(self):
        """
        Display a window with the final points when the game ends.

        This method renders the end-game message with a translucent overlay
        and waits for the user to press a key to close the game.
        """
        # Create a translucent surface
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # (R, G, B, A), where A is the alpha (transparency)

        font = pygame.font.Font(None, 34)
        total_points = round(self.state.total_points(), 2)

        line1 = font.render("Game Over", True, TEXT_COLOR_LIGHT)
        line2 = font.render(f"You scored a total of {total_points} points", True, TEXT_COLOR_LIGHT)

        rect1 = line1.get_rect(center=((self.size * (CELL_SIZE + MARGIN) + NEXT_NUM_SPACE) // 2,
                                        (self.size * (CELL_SIZE + MARGIN)) // 2 - 20))
        rect2 = line2.get_rect(center=((self.size * (CELL_SIZE + MARGIN) + NEXT_NUM_SPACE) // 2,
                                        (self.size * (CELL_SIZE + MARGIN)) // 2 + 20))

        waiting, blink_timer, show_text = True, 0, True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False

            blink_timer += 1
            if blink_timer % 5 == 0:
                show_text = not show_text

            self.draw_grid()  # Redraw the grid behind the overlay
            self.screen.blit(overlay, (0, 0))  # Apply the translucent overlay

            if show_text:
                self.screen.blit(line1, rect1)
                self.screen.blit(line2, rect2)

            pygame.display.flip()
            pygame.time.delay(100)

        pygame.quit()

    def run(self, headless=False):
        """
        Execute the main game loop.

        This method manages the game logic and user or AI inputs.

        Args:
            headless: Indicates whether to run without a graphical interface.
        """
        start_time = time.time()
        if not headless:
            print(f"Running the game with parameters: {self.seed}, {self.game_mode}, {self.algorithm}")

        MOVES = {pygame.K_LEFT: "LEFT",
                 pygame.K_RIGHT: "RIGHT",
                 pygame.K_UP: "UP",
                 pygame.K_DOWN: "DOWN"}

        running = True
        points = 0

        if self.game_mode == GAME_MODES.USER:
            self.run_user_mode(MOVES, running)
        elif self.game_mode == GAME_MODES.IA:
            points = self.run_ai_mode(running, headless)

        end_time = time.time()

        return points, end_time - start_time

    def run_user_mode(self, MOVES, running):
        """
        Handle the user mode gameplay loop.

        Args:
            MOVES: Dictionary mapping keys to move directions.
            running: Boolean indicating whether the game is still running.
        """
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key in MOVES.keys():
                    move_dir = MOVES[event.key]
                    self.state.move(move_dir)

                    if self.state.completed_state():
                        self.show_points_window()
                        running = False

            self.draw_grid()

    def run_ai_mode(self, running, headless):
        """
        Handle the AI mode gameplay loop.

        Args:
            running: Boolean indicating whether the game is still running.
            headless: Indicates whether to run without a graphical interface.

        Returns:
            Total points scored.
        """
        algorithm_class = ALGORITHM_CLASSES[self.algorithm](self.state, self.heuristic, headless=headless)

        if not headless:
            print(f"Sequence of moves to the optimal path:\n {[TRANSLATE_MOVES[move] for move in algorithm_class.moves_list]}")

        while running:
            next_move = algorithm_class.get_next_move()
            if next_move is not None:
                translated_move = TRANSLATE_MOVES[next_move]
                if not headless:
                    print(f"({algorithm_class.it}/{len(algorithm_class.moves_list)}) AI Moves: {TRANSLATE_MOVES[next_move]}")

                self.state.move(translated_move)
                if self.state.completed_state():
                    if headless:
                        points = self.state.total_points()
                        return points
                    self.show_points_window()
                    running = False
            self.draw_grid()

            time.sleep(0.25)

        return 0
