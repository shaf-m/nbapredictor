from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas
import openpyxl

nba_teams = teams.get_teams()
# Select the dictionary for the Raptors, which contains their team ID
raptors = [team for team in nba_teams if team['abbreviation'] == 'BOS'][0]
raptors_id = raptors['id']
# print(raptors)

gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=raptors_id)
games = gamefinder.get_data_frames()[0]
dataframe = games.head(50)
file_name = 'shafnba.xlsx'
dataframe.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')
