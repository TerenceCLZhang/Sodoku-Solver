# Sudoku Solver

This is a Sudoku Solver program implemented using Python and the Pygame library. The program allows you to solve Sudoku puzzles interactively or generate random Sudoku boards to solve.

## Features

- Solve Sudoku puzzles using a backtracking algorithm.
- Generate random Sudoku boards with varying levels of difficulty.
- Interactively select cells, set cell values, and clear cell values.
- Visualize the solving process with a graphical user interface.

## Requirements

- Python 3.x
- Pygame

## Usage

1. Install the required dependencies:
```bash
pip install pygame
```

2. Run the program:
```bash
python main.py
```

3. Use the following controls:

- Spacebar: Solve the Sudoku puzzle using the backtracking algorithm.
- R: Reset the board to the original puzzle.
- G: Generate a new random Sudoku board.
- Number keys (1-9): Set the selected cell to the corresponding value.
- Backspace: Clear the value of the selected cell.
- Left-click: Select a cell.
    - Left-click again to deselect a cell

4. The program will display the Sudoku board and the solving process. Once the puzzle is solved or if there is no solution, a pop-up message will be shown.
