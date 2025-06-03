import tkinter as tk
from tkinter import messagebox

ROWS = 6
COLS = 7
CELL_SIZE = 80
PLAYER_COLORS = ["red", "yellow"]

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.canvas = tk.Canvas(root, width= COLS * CELL_SIZE, height=(ROWS + 1) * CELL_SIZE, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.board = [[" " for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 0  # [0] for Player 1, [1] for Player 2
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x0 = c * CELL_SIZE + 5
                y0 = (r + 1) * CELL_SIZE + 5
                x1 = (c + 1) * CELL_SIZE - 5
                y1 = (r + 2) * CELL_SIZE - 5
                fill_color = "white"
                if self.board[r][c] == "X":
                    fill_color = "red"
                elif self.board[r][c] == "O":
                    fill_color = "yellow"
                self.canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline="black")

    def handle_click(self, event):
        col = event.x // CELL_SIZE
        if col < 0 or col >= COLS:
            return
        if self.board[0][col] != " ":
            return  # Column full

        row = self.get_next_open_row(col)
        if row == -1:
            return

        piece = "X" if self.turn == 0 else "O"
        self.board[row][col] = piece
        self.draw_board()

        if self.check_win(piece):
            messagebox.showinfo("Game Over", f"Player {self.turn + 1} ({PLAYER_COLORS[self.turn]}) wins!")
            self.canvas.unbind("<Button-1>")
            return

        if all(self.board[0][c] != " " for c in range(COLS)):
            messagebox.showinfo("Game Over", "It's a draw!")
            return

        self.turn = 1 - self.turn  # Switch turn

    def get_next_open_row(self, col):
        for r in range(ROWS - 1, -1, -1):
            if self.board[r][col] == " ":
                return r
        return -1

    def check_win(self, piece):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True
        # Positive diagonal
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True
        # Negative diagonal
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True
        return False

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4(root)
    root.mainloop()
