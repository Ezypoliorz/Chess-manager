import chess_openings as openings
import chess_games as games
import chess.pgn
import re

pgn_file_path = "game.pgn"
archive_url = "https://api.chess.com/pub/player/ezypoliorz27/games/archives"

pgns_list = games.pgn(archive_url)
pgns_data = []

for pgn in pgns_list:
    content=""
    print(type(pgn))
    print(len(pgn))
    if len(pgn)>1:
        content = pgn
        content_formatted = content
        content_formatted = re.split(r"0\\n|1\\n", content)
        print(content_formatted)
        for element_content in content_formatted:
            with open(pgn_file_path, mode='w', encoding="utf-8") as game_file:
                element_writing = "[" + str(element_content)
                print(element_content)
                game_file.write(element_writing)
                game_file.close()

            with open(pgn_file_path, mode='r', encoding="utf-8") as game_file:
                game = chess.pgn.read_game(game_file)
                white = game.headers.get("White")
                black = game.headers.get("Black")
                result = game.headers.get("Result")

            opening=openings.opening(pgn_file_path)
            add=[white, black, result, opening]
            print(add)
            pgns_data.append(add)

print(pgns_data)