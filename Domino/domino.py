import customtkinter as ctk
from tkinter import Canvas, messagebox
import random

# Helper functions
def generate_domino_set():
    """Generate all domino tiles (0-6)."""
    return [(i, j) for i in range(7) for j in range(i, 7)]

def shuffle_dominoes(domino_set):
    """Shuffle the domino set."""
    random.shuffle(domino_set)
    return domino_set

def can_play(domino, board):
    """Check if a domino can be played on either side of the board."""
    if not board:
        return True
    return domino[0] in [board[0][0], board[-1][1]] or domino[1] in [board[0][0], board[-1][1]]

def get_playable_side(domino, board):
    """Determine the side where the domino can be played."""
    if not board:
        return "left"  # Any domino can start
    if domino[1] == board[0][0] or domino[0] == board[0][0]:
        return "left"
    if domino[0] == board[-1][1] or domino[1] == board[-1][1]:
        return "right"
    return None

def play_domino(domino, board, side):
    """Play a domino on the chosen side of the board."""
    if side == "left":
        if domino[1] == board[0][0]:
            board.insert(0, domino)
            return True
        elif domino[0] == board[0][0]:
            board.insert(0, domino[::-1])
            return True
    elif side == "right":
        if domino[0] == board[-1][1]:
            board.append(domino)
            return True
        elif domino[1] == board[-1][1]:
            board.append(domino[::-1])
            return True
    return False

# Domino Drawing Function
def draw_domino(canvas, value1, value2, size=80):
    """Draws a domino with dots based on value1 and value2, with a middle line."""
    dot_radius = size // 10
    dot_positions = [
        [],  # 0
        [(0, 0)],  # 1
        [(-1, -1), (1, 1)],  # 2
        [(-1, -1), (0, 0), (1, 1)],  # 3
        [(-1, -1), (1, -1), (-1, 1), (1, 1)],  # 4
        [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)],  # 5
        [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)],  # 6 flipped
    ]

    canvas.delete("all")
    canvas_width = size * 2
    canvas_height = size
    canvas.configure(width=canvas_width, height=canvas_height)

    # Draw dividing line
    canvas.create_line(size, 0, size, size, fill="black", width=2)

    # Draw left side (value1)
    for x, y in dot_positions[value1]:
        canvas.create_oval(
            size // 2 + (x * size // 4) - dot_radius,
            size // 2 + (y * size // 4) - dot_radius,
            size // 2 + (x * size // 4) + dot_radius,
            size // 2 + (y * size // 4) + dot_radius,
            fill="black"
        )

    # Draw right side (value2)
    for x, y in dot_positions[value2]:
        canvas.create_oval(
            3 * size // 2 + (x * size // 4) - dot_radius,
            size // 2 - (y * size // 4) - dot_radius,  # Flipping for 6
            3 * size // 2 + (x * size // 4) + dot_radius,
            size // 2 - (y * size // 4) + dot_radius,
            fill="black"
        )

# CustomTkinter Game Class
class DominoGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Domino Game: Player vs Computer")
        self.geometry("1200x800+100+50")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Game variables
        self.domino_set = shuffle_dominoes(generate_domino_set())
        self.board = [self.domino_set.pop()]  # Start with a random domino from the deck
        self.player_hand = self.domino_set[:7]
        self.computer_hand = self.domino_set[7:14]
        self.draw_pile = self.domino_set[14:]
        self.current_turn = "Player"

        # Widgets
        self.computer_frame = ctk.CTkScrollableFrame(self, height=180, orientation="horizontal", width=1100)
        self.board_frame = ctk.CTkScrollableFrame(self, height=350, width=1100)
        self.player_hand_scroll = ctk.CTkScrollableFrame(self, height=180, orientation="horizontal", width=1100)
        self.status_label = ctk.CTkLabel(self, text="Your Turn!", font=("Arial", 16))
        self.draw_button = ctk.CTkButton(self, text="Draw Tile", command=self.player_draw)

        self.computer_frame.pack(side="top", fill="both", padx=10, pady=10)
        self.board_frame.pack(side="top", fill="both", padx=10, pady=10, expand=True)
        self.status_label.pack(side="top", pady=5)
        self.draw_button.pack(side="bottom", pady=10)
        self.player_hand_scroll.pack(side="bottom", fill="both", padx=10, pady=10)
        
        self.render_player_hand()
        self.render_board()
        self.render_computer_hand()

    def render_player_hand(self):
        """Render player's hand as clickable tiles with dots."""
        for widget in self.player_hand_scroll.winfo_children():
            widget.destroy()
        
        for domino in self.player_hand:
            canvas = Canvas(self.player_hand_scroll, width=160, height=80, bg="white")
            draw_domino(canvas, domino[0], domino[1])
            canvas.bind("<Button-1>", lambda event, d=domino: self.player_move(d))
            canvas.pack(side="left", padx=5)

    def render_computer_hand(self):
        """Render the computer's hand as same-sized blank tiles."""
        for widget in self.computer_frame.winfo_children():
            widget.destroy()
        
        for _ in self.computer_hand:
            canvas = Canvas(self.computer_frame, width=160, height=80, bg="gray")
            canvas.create_line(80, 0, 80, 80, fill="black", width=2)  # Middle divider
            canvas.pack(side="left", padx=5)

    def render_board(self):
        """Render the game board with dots."""
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        row_length = 12  # Maximum dominoes per row
        for i, domino in enumerate(self.board):
            canvas = Canvas(self.board_frame, width=160, height=80, bg="white")
            draw_domino(canvas, domino[0], domino[1])
            canvas.grid(row=i // row_length, column=i % row_length, padx=5, pady=5)

    def player_move(self, domino):
        """Handle player's move."""
        side = get_playable_side(domino, self.board)
        if side:
            play_domino(domino, self.board, side)
            self.player_hand.remove(domino)
            self.status_label.configure(text="Computer's Turn")
            self.render_board()
            self.render_player_hand()
            self.check_winner()
            self.after(1000, self.computer_move)  # Delay for computer's move
        else:
            messagebox.showerror("Invalid Move", "You can't play this domino!")

    def computer_move(self):
        """Handle computer's move."""
        while True:
            playable_dominoes = [d for d in self.computer_hand if get_playable_side(d, self.board)]
            if playable_dominoes:
                domino = random.choice(playable_dominoes)
                side = get_playable_side(domino, self.board)
                play_domino(domino, self.board, side)
                self.computer_hand.remove(domino)
                self.status_label.configure(text="Your Turn!")
                break
            elif self.draw_pile:
                self.computer_hand.append(self.draw_pile.pop())
                self.status_label.configure(text="Computer draws a tile...")
            else:
                self.status_label.configure(text="Draw pile is empty! Computer skips.")
                break
        self.render_board()
        self.render_computer_hand()
        self.check_winner()

    def player_draw(self):
        """Player draws a tile."""
        if self.draw_pile:
            self.player_hand.append(self.draw_pile.pop())
            self.status_label.configure(text="You drew a tile!")
            self.render_player_hand()
        else:
            self.status_label.configure(text="Draw pile is empty! Your turn is skipped.")
            self.after(1000, self.computer_move)

    def check_winner(self):
        """Check if there's a winner."""
        if not self.player_hand:
            messagebox.showinfo("Game Over", "You Win!")
            self.quit()
        elif not self.computer_hand:
            messagebox.showinfo("Game Over", "Computer Wins!")
            self.quit()
        elif not self.draw_pile and not any(get_playable_side(d, self.board) for d in self.player_hand + self.computer_hand):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.quit()

# Run the game
if __name__ == "__main__":
    game = DominoGame()
    game.mainloop()
