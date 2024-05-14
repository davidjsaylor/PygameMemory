import pygame
import random
import sys
import time
import platform

pygame.init()

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4
SQUARE_SIZE = WIDTH // COLS
TOOLBAR_HEIGHT = 50
MAX_FPS = 60

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 128)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, BROWN, CYAN]

if platform.system() == 'Linux':
    FONT = pygame.font.SysFont("DejaVu Sans", 40)
    SMALL_FONT = pygame.font.SysFont("DejaVu Sans", 30)
else:
    FONT = pygame.font.SysFont("Arial", 40)
    SMALL_FONT = pygame.font.SysFont("Arial", 30)

WIN = pygame.display.set_mode((WIDTH, HEIGHT + TOOLBAR_HEIGHT))
pygame.display.set_caption("Memory Game")

def draw_grid(board, revealed):
    for row in range(ROWS):
        for col in range(COLS):
            color = board[row][col] if revealed[row][col] else GRAY
            pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE + TOOLBAR_HEIGHT, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(WIN, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE + TOOLBAR_HEIGHT, SQUARE_SIZE, SQUARE_SIZE), 2)

def create_board():
    colors = COLORS * 2
    for _ in range(3):
        random.shuffle(colors)
    board = []
    for row in range(ROWS):
        board.append([colors.pop() for _ in range(COLS)])
    return board

def draw_toolbar():
    pygame.draw.rect(WIN, WHITE, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    start_button = FONT.render("Start New Game", True, BLACK)
    WIN.blit(start_button, (WIDTH // 2 - start_button.get_width() // 2, TOOLBAR_HEIGHT // 2 - start_button.get_height() // 2))

def splash_screen():
    WIN.fill(BLACK)
    title = FONT.render("Memory", True, WHITE)
    logo = SMALL_FONT.render("How fast are you?", True, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - title.get_height() // 2 - 50))
    WIN.blit(logo, (WIDTH // 2 - logo.get_width() // 2, HEIGHT // 2 - logo.get_height() // 2 + 50))
    pygame.display.update()

def display_time(elapsed_time):
    time_message = FONT.render(f"Your time: {elapsed_time:.2f} seconds", True, BLACK)
    WIN.blit(time_message, (WIDTH // 2 - time_message.get_width() // 2, HEIGHT // 2 - time_message.get_height() // 2 + TOOLBAR_HEIGHT))

def main():
    clock = pygame.time.Clock()
    board = create_board()
    revealed = [[False] * COLS for _ in range(ROWS)]
    first_selection = None
    matched_pairs = 0
    game_started = False
    game_start_time = 0
    game_completed_time = None

    run = True
    while run:
        clock.tick(MAX_FPS)
        
        WIN.fill(BLACK)
        
        if not game_started:
            splash_screen()
        else:
            draw_grid(board, revealed)
        
        draw_toolbar()
        
        if game_started:
            if game_completed_time is None:
                elapsed_time = time.time() - game_start_time
                timer_display = SMALL_FONT.render(f"Time: {elapsed_time:.2f}", True, BLACK)
            else:
                display_time(game_completed_time)
                elapsed_time = game_completed_time
                timer_display = SMALL_FONT.render(f"Time: {elapsed_time:.2f}", True, BLACK)
            WIN.blit(timer_display, (10, 10))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and TOOLBAR_HEIGHT // 2 - 25 <= y <= TOOLBAR_HEIGHT // 2 + 25:
                    board = create_board()
                    revealed = [[False] * COLS for _ in range(ROWS)]
                    first_selection = None
                    matched_pairs = 0
                    game_started = True
                    game_start_time = time.time()
                    game_completed_time = None
                else:
                    if y > TOOLBAR_HEIGHT and game_started and game_completed_time is None:
                        col, row = x // SQUARE_SIZE, (y - TOOLBAR_HEIGHT) // SQUARE_SIZE
                        if not revealed[row][col]:
                            revealed[row][col] = True
                            if first_selection:
                                draw_grid(board, revealed)
                                pygame.display.update()
                                pygame.time.delay(500)
                                if board[row][col] != board[first_selection[0]][first_selection[1]]:
                                    revealed[row][col] = False
                                    revealed[first_selection[0]][first_selection[1]] = False
                                else:
                                    matched_pairs += 1
                                first_selection = None
                            else:
                                first_selection = (row, col)
        
        if matched_pairs == 8 and game_completed_time is None:
            game_completed_time = time.time() - game_start_time

if __name__ == "__main__":
    main()
