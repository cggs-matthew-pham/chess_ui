from chess_ui import ChessUI
import chess.engine


engine = chess.engine.SimpleEngine.popen_uci("engine/stockfish-windows-x86-64-universal.exe")
engine.configure(
    {
        "Skill Level": 1
    }
)

def player_moved(move):
    print("Player:", move)
    # Uncomment to automatically make AI move
    stockfish_move()


def stockfish_move():
    board = ui.get_board()

    result = engine.play(
        board,
        chess.engine.Limit(time=1)
    )

    move = result.move

    print("Stockfish:", move)

    ui.make_move(move)


ui = ChessUI(
    on_move=player_moved,
    on_stockfish=stockfish_move
)

ui.run()

engine.quit()