from nba_api.live.nba.endpoints import scoreboard
import json

# Today's Score Board
games = scoreboard.ScoreBoard()

# json
games.get_json()

# dictionary
d = games.get_dict()

# my code
scoreboard = d['scoreboard']
games = scoreboard['games']

for x in games:
    print(x)
    print("\n\n")


