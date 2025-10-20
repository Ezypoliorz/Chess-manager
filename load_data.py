import requests
import multiprocessing
import os
import time
import re
import json
import csv
import chess
import chess.pgn
import chess.svg
from stockfish import Stockfish

username = ''

num_cores = os.cpu_count()
pool_size = num_cores*2

def process_game(game_data):
    game, username = game_data

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

def _process_archive(archive_url_and_username):
    archives_url, username = archive_url_and_username
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    }
    
    try:
        response = requests.get(archives_url, headers=headers)
        response.raise_for_status()
        archive_data = response.json()
        
        games = archive_data["games"]

        data_for_processing = [(game, username) for game in games]
        
        results = []
        for game_data in data_for_processing:
            results.append(process_game(game_data))
        
        return [res for res in results if res is not None]
        
    except requests.exceptions.RequestException as e:
        print(f"Error while loading {archives_url} : {e}")
        return []

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

    print("Processing data...")

    data_for_pool = [(url, usernamee) for url in archives_urls]
    
    with multiprocessing.Pool(processes=pool_size) as pool:
        list_of_game_lists = pool.map(_process_archive, data_for_pool)
    
    json_data = [game for game_list in list_of_game_lists for game in game_list]
    
    final_games_data = []
    for new_id, game in enumerate(json_data):
        game["Game-ID"] = new_id + 1
        final_games_data.append(game)
        
    with open('games_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_games_data, f, indent=4, ensure_ascii=False)

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
                "Games": [],
                "Wins": 0,
                "Won-Games": [],
                "Draws": 0,
                "Drawn-Games": [],
                "Losses": 0,
                "Lost-Games": [],
                "Win-Rate": 0,
                "Opening-Moves": "",
                "Winrate-Evolution": [],
                "Average-Position": ""
            }
            openings_dict[opening_name] = new_opening
            openings_data.append(new_opening)

        opening = openings_dict[opening_name]
        game_id = game["Game-ID"]
        result = game["Personnal-Result"]
        opening["Games"].append({"Game-ID": game_id, "Result": result})

        if result == "Win" and game_id not in opening["Won-Games"]:
            opening["Wins"] += 1
            opening["Won-Games"].append(game_id)
        elif result == "Draw" and game_id not in opening["Drawn-Games"]:
            opening["Draws"] += 1
            opening["Drawn-Games"].append(game_id)
        elif result == "Loss" and game_id not in opening["Lost-Games"]:
            opening["Losses"] += 1
            opening["Lost-Games"].append(game_id)
        total_games = opening["Wins"] + opening["Draws"] + opening["Losses"]
        wins = 0
        for game_opening in opening["Games"][-200:] :
            if game_opening["Result"] == "Win" :
                wins += 1
        opening["Winrate-Evolution"].append({"Result": result, "Winrate": (wins / len(opening["Games"][-200:])) * 100})

    for opening in openings_data:
        total_games = opening["Wins"] + opening["Draws"] + opening["Losses"]
        if total_games > 0:
            win_rate = (opening["Wins"] / total_games) * 100
            opening["Win-Rate"] = f"{win_rate:.2f}%"
        
        opening["Total-Games"] = total_games

        opening_moves = []
        with open("ECO_database.tsv", mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter='\t')
            header = next(reader)
            name_col_index = header.index('name')
            pgn_col_index = header.index('pgn')
            for row in reader:
                if opening["Opening-Name"] in row[name_col_index].strip() :
                    opening_moves.append(row[pgn_col_index].strip())
        common = opening_moves[0]
        for i in range(1, len(opening_moves)):
            while opening_moves[i].startswith(common) is False:
                common = common[:-1]
        opening["Opening-Moves"] = common

    sorted_openings = sorted(openings_data, key=lambda x: x["Total-Games"], reverse=True)

    with open('openings_winrate.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_openings, f, indent=4, ensure_ascii=False)