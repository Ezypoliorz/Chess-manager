import json
import random

with open('players.json', 'r') as f :
    players_data = json.load(f)

class Player :
    def __init__(self, name, rating, points, games, white):
        self.name = name
        self.rating = rating
        self.points = points
        self.games = games
        self.white = white

players = [Player(player["Name"], player["Rating"], player["Points"], player["Games"], player["White"]) for player in players_data]

games = {}
for player in players :
    player.rating += 200 * player.points
    player.rating -= 200 * (player.games - player.points)
players = sorted(players, key = lambda p : p.rating)
for i in range(0, len(players)-1, 2) :
    if player[i].white > player[i+1].white :
        games[player[i+1]] = players[i]
    elif player[i].white < player[i+1].white :
        games[player[i]] = players[i+1]
    else :
        random_number = random.randint(0, 1)
        games[player[i+random_number]] = player[i+(1-random_number)]
    games[players[i]] = players[i+1]

print(games)
for white, black in games.items() :
    print(f"White : {white.name}, Black : {black.name}")



"""
for i, player in enumerate(players) :
    if player not in games.values() :
        opponents = [possible_player for possible_player in players if possible_player.name != player.name and possible_player not in games.values() and possible_player not in games.keys()]
        opponents_adjusted = []
        for opponent in opponents :
            opponents_adjusted.extend([opponent]*int(1000/(abs(player.rating-opponent.rating))+1))
        games[player] = opponents_adjusted[random.randint(0, len(opponents_adjusted)-1)]"""