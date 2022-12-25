from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import scoreboard

nba_teams = teams.get_teams()
raptors = [team for team in nba_teams if team['abbreviation'] == 'TOR'][0]
raptors_id = raptors['id']

gamefinder = scoreboard.Scoreboard()
games = gamefinder.get_data_frames()[0]
dataframe = games
file_name = 'shafnba.xlsx'
dataframe.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')
