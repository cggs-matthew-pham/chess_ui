from chess_ui import ChessUI


def player_moved(move):
    print("Player:", move)


def stockfish_move():
    print("Stockfish button pressed")


ui = ChessUI(
    on_move=player_moved,
    on_stockfish=stockfish_move
)

ui.run()