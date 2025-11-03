import json
import random

class Player:
    def __init__(self, name, rating, points, games, white, black, previous_opponents):
        self.name = name
        self.rating = rating
        self.points = points
        self.games = games
        self.white = white
        self.black = black
        self.previous_opponents = previous_opponents

    def __repr__(self):
        return f"Player(Name='{self.name}', Points={self.points}, Rating={self.rating}, W={self.white}, B={self.black})"

def get_color_preference(player1, player2):    
    if abs(player1.white - player1.black) >= 2 or abs(player2.white - player2.black) >= 2:
        return True
    
    if player1.white < player2.white:
        return True
    elif player1.white > player2.white:
        return False
    return random.choice([True, False])

def find_pairings_recursive(remaining_players, current_pairings):
    if not remaining_players:
        return current_pairings

    p1 = remaining_players[0]
    rest_of_players = remaining_players[1:]

    for i, p2 in enumerate(rest_of_players):
        
        if p2.name in p1.previous_opponents or p1.name in p2.previous_opponents:
            continue

        p1_is_white = get_color_preference(p1, p2)

        if p1_is_white:
            white_player, black_player = p1, p2
        else:
            white_player, black_player = p2, p1

        new_remaining_players = rest_of_players[:i] + rest_of_players[i+1:]
        
        result = find_pairings_recursive(
            new_remaining_players, 
            current_pairings + [(white_player, black_player)]
        )

        if result is not None:
            return result

    return None

def generate_pairings(players):
    score_groups = {}
    for player in players:
        score_groups.setdefault(player.points, []).append(player)

    sorted_scores = sorted(score_groups.keys(), reverse=True)
    
    all_pairings = []
    downfloater = [] 

    for score in sorted_scores:
        group = score_groups[score]
        group.extend(downfloater)
        downfloater = [] 
        
        group.sort(key=lambda p: p.rating, reverse=True)

        if len(group) % 2 != 0:
            downfloater = [group.pop()]

        pairings = find_pairings_recursive(group, [])
        
        if pairings is None:
            print(f"ATTENTION : Échec de l'appariement pour le groupe à {score} points.")
            return None

        all_pairings.extend(pairings)

    if downfloater:
        print(f"Joueur restant (BYE/impossibilité) : {downfloater[0].name}")

    return all_pairings

with open('players.json', 'r') as f:
    players_data = json.load(f)
    
players_list = [
    Player(
        p["Name"], 
        p["Rating"], 
        p["Points"], 
        p["Games"], 
        p["White"], 
        p["Black"],
        p["Previous-opponents"]
    ) for p in players_data
]

matchups = generate_pairings(players_list)

print("\n--- Appariement des Joueurs ---")
if matchups:
    for white, black in matchups:
        print(f"Blanc: {white.name} (Pt: {white.points}, ELO: {white.rating}) vs Noir: {black.name} (Pt: {black.points}, ELO: {black.rating})")