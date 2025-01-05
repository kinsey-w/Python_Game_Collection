import tkinter as tk
from tkinter import messagebox
import random

# Initialize the main window
window = tk.Tk()
window.title("Tic-Tac-Toe")

# Global variables
board = [' ' for _ in range(9)]  # Board state
current_player = 'X'  # Human player is 'X', AI is 'O'
buttons = []  # To store the buttons

# Check for a win
def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if all(board[pos] == player for pos in condition):
            return True
    return False

# Check for a tie
def check_tie(board):
    return ' ' not in board

# Handle AI move
def ai_move():
    global board
    # AI logic: Win, block, or random
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_win(board, 'O'):
                update_board()
                return
            board[i] = ' '  # Undo move

    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_win(board, 'X'):
                board[i] = 'O'
                update_board()
                return
            board[i] = ' '  # Undo move

    # Random move
    available_moves = [i for i, cell in enumerate(board) if cell == ' ']
    if available_moves:
        move = random.choice(available_moves)
        board[move] = 'O'
        update_board()

# Handle button click
def on_click(index):
    global current_player, board
    if board[index] == ' ' and current_player == 'X':  # Ensure the cell is empty
        board[index] = 'X'
        update_board()
        if check_win(board, 'X'):
            messagebox.showinfo("Game Over", "You win!")
            reset_game()
        elif check_tie(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            reset_game()
        else:
            current_player = 'O'
            ai_move()
            if check_win(board, 'O'):
                messagebox.showinfo("Game Over", "AI wins!")
                reset_game()
            elif check_tie(board):
                messagebox.showinfo("Game Over", "It's a tie!")
                reset_game()
            current_player = 'X'

# Update the GUI board
def update_board():
    for i in range(9):
        buttons[i].config(text=board[i])

# Reset the game
def reset_game():
    global board, current_player
    board = [' ' for _ in range(9)]
    current_player = 'X'
    update_board()

# Create the GUI
for i in range(9):
    btn = tk.Button(window, text=' ', font=('Arial', 24), height=2, width=5,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i // 3, column=i % 3)
    buttons.append(btn)

# Start the main loop
window.mainloop()
