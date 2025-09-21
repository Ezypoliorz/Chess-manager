import json
import random

with open('players.json', 'r') as f :
    players_data = json.load(f)

class Player :
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

players = [Player(player["Name"], player["Rating"]) for player in players_data]

games = {}
for i, player in enumerate(players) :
    if player not in games.values() :
        opponents = [possible_player for possible_player in players if possible_player.name != player.name and possible_player not in games.values() and possible_player not in games.keys()]
        opponents_adjusted = []
        for opponent in opponents :
            opponents_adjusted.extend([opponent]*int(1000/(abs(player.rating-opponent.rating))+1))
        games[player] = opponents_adjusted[random.randint(0, len(opponents_adjusted)-1)]

print(games)
for white, black in games.items() :
    print(f"White : {white.name}, Black : {black.name}")