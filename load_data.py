import requests
import multiprocessing
import time
import re
import json
import csv
import chess
import chess.pgn
import chess.svg
from stockfish import Stockfish

username = ''

def process_game(game_data):
    game, i, username = game_data

    if "pgn" in game and str(game["rules"]) == "chess" and game["initial_setup"] != game["fen"] and game["initial_setup"][:-4] != game["fen"]:
        game_url = game["url"]
        white_username = game["white"]["username"]
        white_rating = game["white"]["rating"]
        black_username = game["black"]["username"]
        black_rating = game["black"]["rating"]
        time_control = game["time_class"]
        
        personnal_result = "Win" if white_username == username and game["white"]["result"] == "win" or black_username == username and game["black"]["result"] == "win" else "Loss" if white_username != username and game["white"]["result"] == "win" or black_username != username and game["black"]["result"] == "win" else "Draw"
        
        game_pgn = "".join(re.split(r"{.*?}", game["pgn"]))
        
        return {
            "Game-ID": i,
            "Game-URL": game_url,
            "White-Username": white_username,
            "White-Rating": white_rating,
            "Black-Username": black_username,
            "Black-Rating": black_rating,
            "Time-Control": time_control.title(),
            "Personnal-Result": personnal_result,
            "PGN": game_pgn
        }
    return None

def pgn(get_archives_url, usernamee):
    global username
    username = usernamee
    print("Loading Games data from Chess.com API...")
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    response = requests.get(get_archives_url, headers=headers)
    response.raise_for_status()
    player_data = response.json()
    name = player_data["name"]
    avatar = player_data["avatar"]

    response = requests.get(f"{get_archives_url}/games/archives", headers=headers)
    response.raise_for_status()
    archives_data = response.json()
    archives_urls = archives_data["archives"]
    json_data = []

    i = 0
    previous_i = 0
    print("Loading PGNs data...")
    for j, archives_url in enumerate(archives_urls):
        response = requests.get(archives_url, headers=headers)
        response.raise_for_status()
        archive_data = response.json()
        data_for_pool = [(game, i+previous_i, username) for i, game in enumerate(archive_data["games"])]
        previous_i += len(archive_data)
        with multiprocessing.Pool() as pool:
            results = pool.map(process_game, data_for_pool)
            json_data += results
        
    with open('games_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)

    return name, avatar

def opening(pgn_file_path):
    with open(pgn_file_path, mode='r', encoding="utf-8") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        eco_code = game.headers.get("ECO")

    with open(pgn_file_path, mode='r', encoding="utf-8") as pgn_file:
        content = pgn_file.read()
        opening_moves_list = content.split("]\n\n")[-1][:-2]
        opening_moves_list = re.sub(r'\s*\d+\.\s*(\.\.)?\s*', ' ', opening_moves_list)
        opening_moves_list = opening_moves_list[1:]

    max_common = 0
    max_common_pgn = ""
    with open("ECO_database.tsv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)
        eco_col_index = header.index('eco')
        name_col_index = header.index('name')
        pgn_col_index = header.index('pgn')
        for row in reader:
            common = 0
            if len(row) > max(eco_col_index, name_col_index):
                current_name = row[name_col_index].strip()
                current_pgn = row[pgn_col_index].strip()
                current_pgn = re.sub(r'\d\. ', '', current_pgn)

                for i in range(min(len(current_pgn), len(opening_moves_list))) :
                    if opening_moves_list[i] == current_pgn[i] :
                        common += 1
                    else :
                        common -= 3
                        break
                if common > max_common:
                    max_common_pgn = current_name
                    max_common = common

    return max_common_pgn

def opening_winrates():
    print("Calculating win rate per opening...")
    with open('games_data.json', 'r', encoding='utf-8') as f:
        games_data = json.load(f)

    with open('openings_winrate.json', 'r', encoding='utf-8') as f:
        openings_data = json.load(f)

    openings_dict = {item["Opening-Name"]: item for item in openings_data}

    for game in games_data:
        opening_name = game["Opening"]
        
        if opening_name not in openings_dict:
            new_opening = {
                "Opening-Name": opening_name,
                "Wins": 0,
                "Won-Games": [],
                "Draws": 0,
                "Drawn-Games": [],
                "Losses": 0,
                "Lost-Games": [],
                "Win-Rate": 0
            }
            openings_dict[opening_name] = new_opening
            openings_data.append(new_opening)

        opening = openings_dict[opening_name]
        game_id = game["Game-ID"]

        result = game["Personnal-Result"]
        if result == "Win" and game_id not in opening["Won-Games"]:
            opening["Wins"] += 1
            opening["Won-Games"].append(game_id)
        elif result == "Draw" and game_id not in opening["Drawn-Games"]:
            opening["Draws"] += 1
            opening["Drawn-Games"].append(game_id)
        elif result == "Loss" and game_id not in opening["Lost-Games"]:
            opening["Losses"] += 1
            opening["Lost-Games"].append(game_id)

    for opening in openings_data:
        total_games = opening["Wins"] + opening["Draws"] + opening["Losses"]
        if total_games > 0:
            win_rate = (opening["Wins"] / total_games) * 100
            opening["Win-Rate"] = f"{win_rate:.2f}%"
        
        opening["Total-Games"] = total_games

    sorted_openings = sorted(openings_data, key=lambda x: x["Total-Games"], reverse=True)

    with open('openings_winrate.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_openings, f, indent=4, ensure_ascii=False)