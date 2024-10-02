import pygame
import random

# Configuración de Pygame
pygame.init()

# Dimensiones de la ventana
WIDTH = 400
HEIGHT = 400
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLOR = (204, 192, 179)
TEXT_COLOR = (119, 110, 101)

# Fuentes
font = pygame.font.Font(None, 55)

# Función para crear una nueva cuadrícula
def new_grid():
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(grid)
    add_new_tile(grid)
    return grid

# Función para agregar un nuevo tile
def add_new_tile(grid):
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        grid[r][c] = 2 if random.random() < 0.9 else 3

# Función para dibujar la cuadrícula
def draw_grid(surface, grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            pygame.draw.rect(surface, CELL_COLOR if grid[r][c] > 0 else BACKGROUND_COLOR,
                             (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
            if grid[r][c] != 0:
                text_surface = font.render(str(grid[r][c]), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=(c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2))
                surface.blit(text_surface, text_rect)

# Función para mover los tiles
def compress(grid):
    new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        pos = 0
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                new_grid[r][pos] = grid[r][c]
                pos += 1
    return new_grid

def merge(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE - 1):
            if grid[r][c] == grid[r][c + 1] and grid[r][c] != 0:
                grid[r][c] *= 2
                grid[r][c + 1] = 0
    return grid

def move_left(grid):
    new_grid = compress(grid)
    new_grid = merge(new_grid)
    new_grid = compress(new_grid)
    return new_grid

# Función principal del juego
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Threes")
    clock = pygame.time.Clock()

    grid = new_grid()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    grid = move_left(grid)
                    add_new_tile(grid)

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
