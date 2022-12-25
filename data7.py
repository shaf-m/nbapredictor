from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import boxscorefourfactorsv2
from nba_api.stats.library.parameters import EndPeriod, EndRange, RangeType, StartPeriod, StartRange
import pandas as pd
import xlsxwriter
import openpyxl
from random import choice
import time
import datetime


df2 = pd.read_excel('decten.xlsx')
# print(df2)

winnerList = []
homeTeamList = []
oppTeamList = []
datesList = []
for index in df2.index:
    homeTeamList.append((df2['Home/Neutral'][index]))
    oppTeamList.append((df2['Visitor/Neutral'][index]))
    datesList.append((df2['Date'][index]))
    # print(df2['Home/Neutral'][index])
# print(homeTeamList)
# print(oppTeamList)
# print(datesList)

for matches in range(len(homeTeamList)):
    time.sleep(.600)
    print(f"Simulating Match {matches+1}/{len(homeTeamList)}")
    nba_teams = teams.get_teams()
    homeTeamSearch = [team for team in nba_teams if team['full_name'] == (homeTeamList[matches])][0]
    homeTeam_id = homeTeamSearch['id']
    homeTeam_abr = homeTeamSearch['abbreviation']
    oppTeamSearch = [team for team in nba_teams if team['full_name'] == (oppTeamList[matches])][0]
    oppTeam_id = oppTeamSearch['id']
    oppTeam_abr = oppTeamSearch['abbreviation']

    gameFinder = teamgamelog.TeamGameLog(team_id=homeTeam_id, season='2020-21')
    time.sleep(.600)

    games = gameFinder.get_data_frames()[0]
    dataframe = games
    file_name1 = 'rawdata.xlsx'
    dataframe.to_excel(file_name1)
    # print('DataFrame 1 (rawData) is written to Excel File successfully.')

    df = pd.read_excel('rawdata.xlsx')
    # print(df)

    gamesDataAgainstOpp = df[(df['MATCHUP'] == f'{homeTeam_abr} @ {oppTeam_abr}') |
                             (df['MATCHUP'] == f'{homeTeam_abr} vs. {oppTeam_abr}')]
    # print(gamesDataAgainstOpp)

    gamesIDAgainstOpp = gamesDataAgainstOpp['Game_ID'].tolist()
    # print(gamesIDAgainstOpp)

    homeCount = 0
    oppCount = 0
    tie = 0
    for ids in range(len(gamesIDAgainstOpp)):
        time.sleep(.600)
        fourFacterFinder = boxscorefourfactorsv2.BoxScoreFourFactorsV2(game_id=f"00{gamesIDAgainstOpp[ids]}",
                                                                       range_type=RangeType.default,
                                                                       start_period=StartPeriod.default,
                                                                       end_period=EndPeriod.default,
                                                                       start_range=StartRange.default,
                                                                       end_range=EndRange.default)
        fourFactors = fourFacterFinder.sql_teams_four_factors.get_data_frame()

        dataframe2 = fourFactors
        file_name2 = 'fourfactorsrawdata.xlsx'
        dataframe2.to_excel(file_name2)
        # print('DataFrame 2 (Four Factors) is written to Excel File successfully.')
        df2 = pd.read_excel('fourfactorsrawdata.xlsx')
        # print(df2)

        home_data = df2[df2['TEAM_ABBREVIATION'] == f"{homeTeam_abr}"]
        opp_data = df2[df2['TEAM_ABBREVIATION'] == f"{oppTeam_abr}"]

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

        if home_four_factor_total > opp_four_factor_total:
            print(f"Sim Winner:\t{homeTeam_abr}")
            homeCount += 1
        elif opp_four_factor_total > home_four_factor_total:
            print(f"Sim Winner\t{oppTeam_abr}")
            oppCount += 1
        else:
            tie += 1

    if homeCount > oppCount:
        print(f"Match-up Winner\t{homeTeam_abr}\t\t{matches+1}/{len(homeTeamList)}\n")
        winnerList.append(f"W - {homeTeam_abr}")
    elif oppCount > homeCount:
        print(f"Match-up Winner\t{oppTeam_abr}\t\t{matches+1}/{len(homeTeamList)}\n")
        winnerList.append(f"W - {oppTeam_abr}")
    elif oppCount == homeCount:
        randTeam_abr = choice([oppTeam_abr, homeTeam_abr])
        print(f"Match-up Winner\t{randTeam_abr}\t\t{matches+1}/{len(homeTeamList)}\n")
        winnerList.append(f"W - {randTeam_abr}")

print(winnerList)


df3 = pd.read_excel('dectenpredict.xlsx')
df3['Winners'] = winnerList
print(df3)
df3.to_excel('predictions.xlsx')

# with pd.ExcelWriter("dectenpredict.xlsx", mode="a", engine="openpyxl") as writer:
#    df3.to_excel(writer, sheet_name="Sheet2")
# df3 = pd.read_excel('dectenpredict.xlsx')
# df3['Winners'] = winnerList
# df3 = df3.assign(winner=winnerList)
print("Predicted winners added to December (dectenpredict) spreadsheet.")
