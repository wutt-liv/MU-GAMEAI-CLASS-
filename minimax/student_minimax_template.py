"""
Student Minimax Template
This file provides a template for students to implement their own minimax algorithm.
"""

import pygame
import sys
from tictactoe import TicTacToe

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
BOARD_SIZE = 3
CELL_SIZE = 150
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE * CELL_SIZE) // 2
BOARD_OFFSET_Y = 100

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe - Implement Your Minimax")
clock = pygame.time.Clock()

# Load fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

def draw_board():
    """Draw the tic-tac-toe board"""
    screen.fill(WHITE)
    
    # Draw title
    title_text = font_large.render("Tic-Tac-Toe", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 40))
    screen.blit(title_text, title_rect)
    
    # Draw grid lines
    for i in range(1, BOARD_SIZE):
        # Vertical lines
        pygame.draw.line(screen, BLACK,
                        (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y),
                        (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE), 3)
        # Horizontal lines
        pygame.draw.line(screen, BLACK,
                        (BOARD_OFFSET_X, BOARD_OFFSET_Y + i * CELL_SIZE),
                        (BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET_Y + i * CELL_SIZE), 3)
    
    # Draw board border
    pygame.draw.rect(screen, BLACK,
                    (BOARD_OFFSET_X, BOARD_OFFSET_Y,
                     BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE), 3)

def draw_marks(board):
    """Draw X's and O's on the board"""
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                # Draw X
                center_x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                size = CELL_SIZE // 3
                pygame.draw.line(screen, RED,
                               (center_x - size, center_y - size),
                               (center_x + size, center_y + size), 5)
                pygame.draw.line(screen, RED,
                               (center_x + size, center_y - size),
                               (center_x - size, center_y + size), 5)
            elif board[row][col] == 'O':
                # Draw O
                center_x = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                radius = CELL_SIZE // 3
                pygame.draw.circle(screen, BLUE, (center_x, center_y), radius, 5)

def draw_status(game):
    """Draw game status and instructions"""
    # Status text
    if game.winner:
        if game.winner == 'X':
            status_text = "You Win!"
            color = RED
        elif game.winner == 'Draw':
            status_text = "It's a Draw!"
            color = DARK_GRAY
        else:
            status_text = "AI Wins!"
            color = BLUE
    elif game.is_board_full():
        status_text = "It's a Draw!"
        color = DARK_GRAY
    else:
        if game.current_player == 'X':
            status_text = "Your Turn (X)"
            color = RED
        else:
            status_text = "AI is Thinking..."
            color = BLUE

    text = font_medium.render(status_text, True, color)
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 600))
    screen.blit(text, text_rect)

    # Instructions
    if game.winner or game.is_board_full():
        inst_text = font_small.render("Press SPACE to play again or ESC to quit", True, DARK_GRAY)
        inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, 650))
        screen.blit(inst_text, inst_rect)
    else:
        inst_text = font_small.render("Click on an empty cell to make your move", True, DARK_GRAY)
        inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, 650))
        screen.blit(inst_text, inst_rect)

def get_board_position(mouse_pos):
    """Convert mouse position to board coordinates"""
    x, y = mouse_pos
    col = (x - BOARD_OFFSET_X) // CELL_SIZE
    row = (y - BOARD_OFFSET_Y) // CELL_SIZE

    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
        return row, col
    return None, None

# ==================== STUDENT IMPLEMENTATION AREA ====================
def evaluate_board(board):
    for row in board:
        if row[0] == row[1] == row[2] == 'O':
            return 10 # AI win!
        elif row[0] == row[1] == row[2] == 'X':
            return -10 # Human win!
        
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == 'O':
            return 10
        elif board[0][col] == board[1][col] == board[2][col] == 'X':
            return -10
        
    if board[0][0] == board[1][1] == board[2][2] == 'O':
        return 10
    elif board[0][0] == board[1][1] == board[2][2] == 'X':
        return -10
    
    if board[0][2] == board[1][1] == board[2][0] == 'O':
        return 10
    elif board[0][2] == board[1][1] == board[2][0] == 'X':
        return -10
    
    if all(' ' not in row for row in board):
        return 0
    
    return None #May something wrong?

def get_empty_cells(board):
    empty = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                empty.append((row, col))
    return empty
    

def minimax(board, depth, is_maximizing):
    # check if the game is over
    result = evaluate_board(board)
    if result is not None:
        return result
    
    if is_maximizing:
        best_score = float('-inf')

        #try every possible paths
        for row, col in get_empty_cells(board):
            board[row][col] = 'O'
            score = minimax(board, depth+1, False)
            board[row][col] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')

        #try every possible paths
        for row, col in get_empty_cells(board):
            board[row][col] = 'X'
            score = minimax(board, depth+1, True)
            board[row][col] = ' '
            best_score = min(score, best_score)
        return best_score

def get_best_move(game):
    best_score = float('-inf')
    best_move = None

    for row, col in game.get_empty_cells():
        game.board[row][col] = 'O'
        score = minimax(game.board, 0, False)
        game.board[row][col] = ' '
        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move

# ==================== END STUDENT IMPLEMENTATION AREA ====================

def main():
    """Main game loop"""
    game = TicTacToe()
    running = True
    ai_thinking = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and (game.winner or game.is_board_full()):
                    # Reset game
                    game = TicTacToe()
                    ai_thinking = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not ai_thinking:
                if event.button == 1:  # Left click
                    if game.current_player == 'X' and not game.winner:
                        row, col = get_board_position(event.pos)
                        if row is not None and game.board[row][col] == ' ':
                            # Player move
                            game.make_move(row, col)
                            ai_thinking = True

        # AI move
        if ai_thinking and game.current_player == 'O' and not game.winner:
            # Add a small delay to show AI is "thinking"
            pygame.time.wait(500)

            # Get best move using student's minimax
            best_move = get_best_move(game)
            if best_move:
                game.make_move(best_move[0], best_move[1])

            ai_thinking = False

        # Draw everything
        draw_board()
        draw_marks(game.board)
        draw_status(game)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()