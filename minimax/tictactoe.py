"""
Tic-Tac-Toe Game Logic
Core game logic for Tic-Tac-Toe
"""

class TicTacToe:
    def __init__(self):
        """Initialize a new game"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X is human, O is AI
        self.winner = None

    def make_move(self, row, col):
        """Make a move on the board"""
        if self.board[row][col] == ' ' and not self.winner:
            self.board[row][col] = self.current_player

            # Check for winner
            if self.check_winner():
                self.winner = self.current_player
            elif self.is_board_full():
                self.winner = 'Draw'
            else:
                # Switch players
                self.current_player = 'O' if self.current_player == 'X' else 'X'

            return True
        return False

    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return True

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True

        return False

    def is_board_full(self):
        """Check if the board is full"""
        for row in self.board:
            if ' ' in row:
                return False
        return True

    def get_empty_cells(self):
        """Get list of empty cells"""
        empty = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    empty.append((row, col))
        return empty

    def __str__(self):
        """String representation of the board"""
        s = "\n"
        for row in self.board:
            s += f" {row[0]} | {row[1]} | {row[2]} \n"
            s += "---|---|---\n"
        return s