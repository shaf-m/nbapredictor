from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import teamgamelog

nba_teams = teams.get_teams()
raptors = [team for team in nba_teams if team['abbreviation'] == 'TOR'][0]
raptors_id = raptors['id']

gamefinder = teamgamelog.TeamGameLog(team_id=raptors_id)
games = gamefinder.get_data_frames()[0]
dataframe = games.head(50)
file_name = 'shafnba.xlsx'
dataframe.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')
