from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import boxscorefourfactorsv2
from nba_api.stats.library.parameters import EndPeriod, EndRange, RangeType, StartPeriod, StartRange
import pandas as pd

nba_teams = teams.get_teams()
raptors = [team for team in nba_teams if team['abbreviation'] == 'TOR'][0]
raptors_id = raptors['id']

gameFinder = teamgamelog.TeamGameLog(team_id=raptors_id, season='2022-23')

games = gameFinder.get_data_frames()[0]
dataframe = games
file_name1 = 'rawdata.xlsx'
dataframe.to_excel(file_name1)
print('DataFrame 1 is written to Excel File successfully.')

df = pd.read_excel('rawdata.xlsx')
print(df)

opponentABR = "CHI"
gamesDataAgainstOpp = df[(df['MATCHUP'] == f'TOR @ {opponentABR}') | (df['MATCHUP'] == f'TOR vs. {opponentABR}')]
print(gamesDataAgainstOpp)

gamesIDAgainstOpp = gamesDataAgainstOpp['Game_ID'].tolist()
print(gamesIDAgainstOpp)


fourFacterFinder = boxscorefourfactorsv2.BoxScoreFourFactorsV2(game_id=f"00{gamesIDAgainstOpp[0]}",
                                                               range_type=RangeType.default,
                                                               start_period=StartPeriod.default,
                                                               end_period=EndPeriod.default,
                                                               start_range=StartRange.default,
                                                               end_range=EndRange.default)

fourFactors = fourFacterFinder.sql_teams_four_factors.get_data_frame()

dataframe2 = fourFactors
file_name2 = 'fourfactorsrawdata.xlsx'
dataframe2.to_excel(file_name2)
print('\nDataFrame 2 is written to Excel File successfully.')
df2 = pd.read_excel('fourfactorsrawdata.xlsx')
print(df2)

home_data = df2[df2['TEAM_ABBREVIATION'] == "TOR"]
opp_data = df2[df2['TEAM_ABBREVIATION'] == f"{opponentABR}"]

# Effective Field Goal Percentage
home_EFG_PCT = sum(home_data['EFG_PCT'])
opp_EFG_PCT = sum(opp_data['EFG_PCT'])

# Free Throw Attempt Rate
home_FTA_RATE = sum(home_data['FTA_RATE'])
opp_FTA_RATE = sum(opp_data['FTA_RATE'])

# Turnover Percentage
home_TOV_PCT = sum(home_data['TM_TOV_PCT'])
opp_TOV_PCT = sum(opp_data['TM_TOV_PCT'])

# Rebounding Percentage
home_OREB_PCT = sum(home_data['OREB_PCT'])
opp_OREB_PCT = sum(opp_data['OREB_PCT'])


home_four_factor_total = (home_EFG_PCT * 0.4) + (home_TOV_PCT * 0.25) + (home_OREB_PCT * 0.2) + (home_FTA_RATE * 0.15)
opp_four_factor_total = (opp_EFG_PCT * 0.4) + (opp_TOV_PCT * 0.25) + (opp_OREB_PCT * 0.2) + (opp_FTA_RATE * 0.15)


homeABR = "TOR"
print(f"\n\n{homeABR} Four Factor Breakdown:\n"
      f"1) {'Effective Field Goal %:':30} {home_EFG_PCT*100:.2f}\n"
      f"2) {'Turnover %:':30} {home_TOV_PCT*100:.2f}\n"
      f"3) {'Rebounding %:':30} {home_OREB_PCT*100:.2f}\n"
      f"4) {'Free Throw Attempt %:':30} {home_FTA_RATE*100:.2f}\n"
      f"----------------------------------------\n"
      f"{'Four Factor Total %:':33} {home_four_factor_total*100:.2f}")


print(f"\n{opponentABR} Four Factor Breakdown:\n"
      f"1) {'Effective Field Goal %:':30} {opp_EFG_PCT*100:.2f}\n"
      f"2) {'Turnover %:':30} {opp_TOV_PCT*100:.2f}\n"
      f"3) {'Rebounding %:':30} {opp_OREB_PCT*100:.2f}\n"
      f"4) {'Free Throw Attempt %:':30} {opp_FTA_RATE*100:.2f}\n"
      f"---------------------------------------\n"
      f"{'Four Factor Total %:':33} {opp_four_factor_total*100:.2f}")


if home_four_factor_total > opp_four_factor_total:
    print(f"\n--------- Expected Winner: {homeABR} --------")
elif opp_four_factor_total > home_four_factor_total:
    print(f"\n--------- Expected Winner: {opponentABR} --------")
