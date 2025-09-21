import load_data as data
import chess.pgn
import json
import tkinter
import customtkinter

if __name__ == "__main__" :
    pgn_file_path = "game.pgn"
    username = "EzypoIiorz"
    archive_url = f"https://api.chess.com/pub/player/{username.lower()}"

    name, avatar = data.pgn(archive_url, username)

    pgns_data = []
    player_data = {
        "Username" : username,
        "Name" : name,
        "Avatar" : avatar,
        "Rapid" : [],
        "Blitz" : [],
        "Bullet" : []
    }

    with open('games_data.json', 'r', encoding='utf-8') as f:
        games_data = json.load(f)

    for game_data in games_data :
        pgn = game_data["PGN"]
        with open(pgn_file_path, 'w') as game_file :
            game_file.write(pgn)
        with open(pgn_file_path, 'r') as game_file :
            game = chess.pgn.read_game(game_file)

        result = game.headers.get("Termination")
        date = game.headers.get("Date")
        tournament = None
        if game.headers.get("Tournament") :
            tournament = game.headers.get("Tournament").split("/")[-1].rsplit('-', 1)[0].replace("-", " ").title()

        opening=data.opening(pgn_file_path)
        add = [item if item else None for item in [result, date, opening.split(":")[0] if ":" in opening else opening, tournament]]
        pgns_data.append(add)

        if game_data["Time-Control"] in player_data.keys() :
            if game_data["White-Rating"] != 0:
                player_data[game_data["Time-Control"]].append(game_data["White-Rating"] if game_data["White-Username"] == username else game_data["Black-Rating"])

    for element, content in zip(games_data, pgns_data) :
        pgn = element["PGN"]
        del element["PGN"]
        element["Result"] = content[0]
        element["Date"] = content[1]
        element["Opening"] = content[2]
        if content[3] != None :
            element["Tournament"] = content[3]
        element["PGN"] = pgn

    with open('games_data.json', 'w', encoding='utf-8') as f:
        json.dump(games_data, f, indent=4, ensure_ascii=False)

    with open('player_data.json', 'w') as f :
        json.dump(player_data, f, indent=4, ensure_ascii=False)

    data.opening_winrates()