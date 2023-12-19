import tkinter as tk
from tkinter import messagebox
import numpy as np

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.resizable(width=False, height=False)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(
                    self.root,
                    text="",
                    font=("Helvetica", 24),
                    width=4,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                )
                self.buttons[i][j].grid(row=i, column=j)

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.reset_board()
            elif all(self.board[i][j] != "" for i in range(3) for j in range(3)):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                self.switch_player()
                if self.current_player == "O":
                    row, col = self.ai_make_move()
                    self.make_move(row, col)

    def ai_make_move(self):
        _, move = self.minimax(self.board, "O")
        return move

    def minimax(self, board, player):
        if self.check_winner(board) == "X":
            return -1, None
        elif self.check_winner(board) == "O":
            return 1, None
        elif all(board[i][j] != "" for i in range(3) for j in range(3)):
            return 0, None

        if player == "O":  # Maximize for "O"
            max_eval = float("-inf")
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = player
                        eval, _ = self.minimax(board, "X")
                        board[i][j] = ""  # Undo the move
                        if eval > max_eval:
                            max_eval = eval
                            best_move = (i, j)
            return max_eval, best_move
        else:  # Minimize for "X"
            min_eval = float("inf")
            best_move = None
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = player
                        eval, _ = self.minimax(board, "O")
                        board[i][j] = ""  # Undo the move
                        if eval < min_eval:
                            min_eval = eval
                            best_move = (i, j)
            return min_eval, best_move

    def check_winner(self, board=None):
        if board is None:
            board = self.board
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
        return None

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="")
                self.board[i][j] = ""
        self.current_player = "X"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    TicTacToe().run()
