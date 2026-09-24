import tkinter as tk
import chess


PIECES = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}


class ChessUI:
    def __init__(self, on_move=None, on_stockfish=None):
        """
        on_move:
            Function called after the player makes a legal move.

        on_stockfish:
            Function called when the Stockfish Move button is pressed.
        """

        self.board = chess.Board()

        self.on_move = on_move
        self.on_stockfish = on_stockfish

        self.selected_square = None
        self.buttons = {}

        self.root = tk.Tk()
        self.root.title("Robot Chess")

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=20, pady=20)

        self.status = tk.Label(
            self.root,
            text="White to move",
            font=("Arial", 14)
        )
        self.status.pack(pady=(0, 10))

        self.stockfish_button = tk.Button(
            self.root,
            text="Stockfish Move",
            command=self.stockfish_clicked
        )
        self.stockfish_button.pack(pady=(0, 20))

        self.create_board()
        self.update_board()


    def create_board(self):
        """Create the 8 x 8 chess board."""

        for row in range(8):
            for col in range(8):

                # Tkinter rows go top to bottom.
                # Chess ranks go bottom to top.
                square = chess.square(col, 7 - row)

                button = tk.Button(
                    self.board_frame,
                    width=4,
                    height=2,
                    font=("Arial", 24),
                    command=lambda s=square: self.square_clicked(s)
                )

                if (row + col) % 2 == 0:
                    button.config(bg="bisque")
                else:
                    button.config(bg="sienna")

                button.grid(row=row, column=col)

                self.buttons[square] = button


    def update_board(self):
        """Update the pieces shown on the board."""

        for square, button in self.buttons.items():

            piece = self.board.piece_at(square)

            if piece:
                button.config(text=PIECES[piece.symbol()])
            else:
                button.config(text="")

        if self.board.turn == chess.WHITE:
            self.status.config(text="White to move")
        else:
            self.status.config(text="Black to move")


    def square_clicked(self, square):
        """Handle player selecting a start and destination square."""

        # First click: select a piece
        if self.selected_square is None:

            piece = self.board.piece_at(square)

            if piece is not None:

                self.selected_square = square

                self.status.config(
                    text=f"Selected {chess.square_name(square)}"
                )

            return


        # Second click: select destination
        move = chess.Move(
            self.selected_square,
            square
        )

        if move in self.board.legal_moves:

            self.board.push(move)

            self.selected_square = None

            self.update_board()

            # Tell main.py that the player moved
            if self.on_move:
                self.on_move(move)

        else:

            self.status.config(text="Illegal move")
            self.selected_square = None


    def stockfish_clicked(self):
        """Run the Stockfish callback supplied by main.py."""

        if self.on_stockfish:
            self.on_stockfish()


    def make_move(self, move):
        """
        Make a move from another part of the program.

        Useful for Stockfish moves.
        """

        if move in self.board.legal_moves:

            self.board.push(move)
            self.update_board()

            return True

        return False


    def get_board(self):
        """Return the python-chess board."""

        return self.board


    def run(self):
        """Start the Tkinter program."""

        self.root.mainloop()