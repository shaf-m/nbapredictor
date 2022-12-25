from nba_api.stats.endpoints import leaguegamelog

log = leaguegamelog.LeagueGameLog(player_or_team_abbreviation='T')

gamesLog = log.get_data_frames()[0]
dataframe = gamesLog
file_name1 = 'gameslog.xlsx'
dataframe.to_excel(file_name1)
print('GamesLog is written to Excel File successfully.')
