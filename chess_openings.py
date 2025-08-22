import csv
import chess.pgn

def get_opening_name(eco_code, opening_moves_list):
    candidate_openings = {}
    max_common = 0
    max_common_pgn = ""
    opening = ""
    with open("ECO_database.tsv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        header = next(reader)
        eco_col_index = header.index('eco')
        name_col_index = header.index('name')
        pgn_col_index = header.index('pgn')
        for row in reader:
            if len(row) > max(eco_col_index, name_col_index):
                current_eco = row[eco_col_index].strip()
                current_name = row[name_col_index].strip()
                current_pgn = row[pgn_col_index].strip()
                
                if current_eco == eco_code.upper():
                    candidate_openings[current_name]=current_pgn

    for i in range(len(list(candidate_openings.keys()))):
        common = 0
        current_pgn = candidate_openings[list(candidate_openings.keys())[i]]

        c = 0
        current_pgn_list = current_pgn.split(" ")
        for i in range(len(current_pgn_list)-1):
            if "." in current_pgn_list[i-c]:
                del(current_pgn_list[i-c])
                c += 1
        current_pgn_list_formatted = []
        for i in range(0, len(current_pgn_list), 2):
            if i + 1 < len(current_pgn_list):
                current_pgn_list_formatted.append(current_pgn_list[i] + current_pgn_list[i+1])
            else:
                current_pgn_list_formatted.append(current_pgn_list[i])



        c = 0
        opening_moves_list_list = opening_moves_list.split(" ")
        for i in range(len(opening_moves_list_list)-1):
            if "." in opening_moves_list_list[i-c]:
                del(opening_moves_list_list[i-c])
                c += 1
        opening_moves_list_list_formatted = []
        for i in range(0, len(opening_moves_list_list), 2):
            if i + 1 < len(opening_moves_list_list):
                opening_moves_list_list_formatted.append(opening_moves_list_list[i] + opening_moves_list_list[i+1])
            else:
                opening_moves_list_list_formatted.append(opening_moves_list_list[i])





        for i in range(len(current_pgn_list_formatted)):
            if current_pgn_list_formatted[i] == opening_moves_list_list_formatted[i]:
                common += 1
            else:
                break
        if common > max_common:
            max_common_pgn = current_pgn
            max_common = common
        
    key_found = None
    for key, value in candidate_openings.items():
        if value == max_common_pgn :
            key_found = key
            break

    return key_found

def get_opening_moves(pgn_file_path):
    with open(pgn_file_path, mode='r', encoding="utf-8") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        eco_code = game.headers.get("ECO")

    with open(pgn_file_path, mode='r', encoding="utf-8") as pgn_file:
        content = pgn_file.read()
        moves = content[content.rfind(']') + 1:].strip()
    
    return eco_code, moves

def opening(pgn):
    eco_code, opening_moves_list = get_opening_moves(pgn)
    opening = get_opening_name(eco_code, opening_moves_list)

    return opening