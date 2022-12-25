from nba_api.live.nba.endpoints import scoreboard
import json

gamefinder = scoreboard.Scoreboard()
games = gamefinder.get_data_frames()[0]
dataframe = games
file_name = 'shafnba.xlsx'
dataframe.to_excel(file_name)
print('DataFrame is written to Excel File successfully.')

