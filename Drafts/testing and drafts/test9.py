from nba_api.stats.static import players
player_dict = players.get_players()

# Use ternary operator or write function
# Names are case sensitive
siakam = [player for player in player_dict if player['full_name'] == 'Pascal Siakam'][0]
siakam_id = siakam['id']

# find team Ids
from nba_api.stats.static import teams
teams = teams.get_teams()
TOR = [x for x in teams if x['full_name'] == 'Toronto Raptors'][0]
TOR_id = TOR['id']


from nba_api.stats.endpoints import leaguegamefinder

#this time we convert it to a dataframe in the same line of code
TOR_games = leaguegamefinder.LeagueGameFinder(team_id_nullable=TOR_id, season).get_data_frames()[0]

print(TOR_games)