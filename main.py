import tkinter as tk
from tkinter import messagebox
import pygame
import random

FPS = 60
CELL_SIZE = 60
BOARD_SIZE = CELL_SIZE * 9
SCREEN_WIDTH, SCREEN_HEIGHT = BOARD_SIZE, BOARD_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

pygame.display.set_caption("Sudoku Solver")


def draw_board(board, screen, selected_cell, current_cell, solved_cells):
    """
    Draws the sudoku board
    """
    for i in range(9):
        for j in range(9):
            cell_x = j * CELL_SIZE
            cell_y = i * CELL_SIZE

            # Draw cell background
            if (i, j) == selected_cell:
                pygame.draw.rect(
                    screen, GRAY, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
            elif (i, j) == current_cell:
                if is_valid(board, i, j, board[i][j]):
                    pygame.draw.rect(
                        screen, GREEN, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(
                        screen, RED, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
            elif (i, j) in solved_cells:
                pygame.draw.rect(
                    screen, GREEN, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(
                    screen, WHITE, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

            pygame.draw.rect(
                screen, BLACK, (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 1)

            if board[i][j] != 0:
                font = pygame.font.Font(None, 40)
                text = font.render(str(board[i][j]), True, BLACK)
                text_rect = text.get_rect(
                    center=(cell_x + CELL_SIZE // 2, cell_y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

    # Draw dividers
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * 3 * CELL_SIZE),
                         (BOARD_SIZE, i * 3 * CELL_SIZE), 5)
        pygame.draw.line(screen, BLACK, (i * 3 * CELL_SIZE, 0),
                         (i * 3 * CELL_SIZE, BOARD_SIZE), 5)


def draw_window(board, screen, selected_cell, current_cell, solved_cells):
    """
    Draws the pygame window
    """
    screen.fill(WHITE)
    draw_board(board, screen, selected_cell, current_cell, solved_cells)

    pygame.display.update()


def is_valid(board, row, col, num):
    """
    Determines whether a number can be in the given cell
    """
    # Check if the number already exists in the same row
    for i in range(9):
        if board[row][i] == num:
            return False

    # Check if the number already exists in the same column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if the number already exists in the same 3x3 box
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


def backtracking_algorithm(board, screen, selected_cell, current_cell, solved_cells):
    """
    An implementation of the backtracking algorithm for solving a Sodoku board
    """
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, column, num):
                        board[row][column] = num
                        current_cell = (row, column)
                        solved_cells.append((row, column))
                        draw_window(board, screen, selected_cell,
                                    current_cell, solved_cells)
                        pygame.event.pump()  # Process events during the delay
                        # Delay to visualize the solving process
                        pygame.time.delay(100)

                        # Check whether quit button is pressed when the algorithm is running
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                return False

                        if backtracking_algorithm(board, screen, selected_cell, current_cell, solved_cells):
                            return True
                        board[row][column] = 0
                        solved_cells.remove((row, column))
                return False
    draw_window(board, screen, selected_cell, current_cell, solved_cells)
    return True


def backtracking_algorithm_random(board):
    """
    An implementation of the backtracking algorithm to create a random Sudoku board
    """
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                random_numbers = random.sample(
                    range(1, 10), 9)  # Generate random numbers
                for num in random_numbers:
                    if is_valid(board, row, column, num):
                        board[row][column] = num
                        if backtracking_algorithm_random(board):
                            return True
                        board[row][column] = 0
                return False
    return True


def generate_sudoku_board():
    """
    Generates a random Sudoku board
    """
    board = [[0 for _ in range(9)] for _ in range(9)]  # Initialize empty board

    # Fill the diagonal 3x3 squares with random numbers
    for i in range(0, 9, 3):
        square = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(square)
        for j in range(3):
            for k in range(3):
                board[i + j][i + k] = square[j * 3 + k]

    # Create a random Sudoku board using the backtracking algorithm
    backtracking_algorithm_random(board)

    # Remove random numbers to create a puzzle
    empty_cells = random.randint(40, 60)
    for _ in range(empty_cells):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        board[row][col] = 0

    return board


def get_clicked_cell(mouse_pos):
    """
    Gets the row and column index of the cell selected by the mouse
    """
    row = mouse_pos[1] // CELL_SIZE
    col = mouse_pos[0] // CELL_SIZE
    return row, col


def reset_board():
    """
    Returns the original board
    """
    return [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]


def show_error_popup(message):
    """
    Display an error message when board is impossible to solve
    """
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", message)


def main():
    """
    Main function
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    board = reset_board()
    selected_cell = None
    solver_running = False
    solved = False
    current_cell = None
    solved_cells = []

    run = True
    while run:
        clock.tick(FPS)
        pygame.event.pump()  # Process events, including window events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Solve using backtracking
                if event.key == pygame.K_SPACE:
                    if not solver_running:
                        solver_running = True
                        success = backtracking_algorithm(
                            board, screen, selected_cell, current_cell, solved_cells)
                        if not success:
                            show_error_popup(
                                "This sudoku board has no solution.")
                        else:
                            selected_cell = None
                            solved = True
                        solver_running = False

                # Reset board
                if event.key == pygame.K_r:
                    if not solver_running:
                        board = reset_board()
                        solved = False
                        solved_cells = []

                # Generate new board
                if event.key == pygame.K_g:
                    if not solver_running:
                        board = generate_sudoku_board()
                        solved = False
                        solved_cells = []

                # Set selected cell value using number keys
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    if selected_cell and not solver_running:
                        row, col = selected_cell
                        num = int(event.unicode)
                        board[row][col] = num

                # Remove selected cell value
                if event.key == pygame.K_BACKSPACE:
                    if selected_cell and not solver_running:
                        row, col = selected_cell
                        board[row][col] = 0

            # Select specific cell
            if not solved:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not solver_running:
                        mouse_pos = pygame.mouse.get_pos()
                        row, col = get_clicked_cell(mouse_pos)
                        if (row, col) == selected_cell:
                            selected_cell = None
                        else:
                            selected_cell = (row, col)

        draw_window(board, screen, selected_cell, current_cell, solved_cells)

    pygame.quit()


if __name__ == "__main__":
    main()
