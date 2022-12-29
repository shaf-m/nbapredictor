from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import boxscorefourfactorsv2
from nba_api.stats.library.parameters import EndPeriod, EndRange, RangeType, StartPeriod, StartRange
import pandas as pd
from random import choice, uniform
import datetime
from time import sleep
from os import listdir
from os.path import isfile, join
import streamlit as st
from PIL import Image
import pytz


def page_init():
    st.set_page_config(page_title="Today's NBA Predictions", layout='wide')
    st.header('NBA Predictions of The Day')


def get_date():
    # Thu, Dec 1, 2022
    date_tmzn = datetime.datetime.now(pytz.timezone('EST'))
    # print(date_tmzn)
    dayWeek = (date_tmzn.strftime('%A'))[:3]
    # date_est = ((str(date_tmzn).split(' '))[0])
    # print(date_est)
    test = ((str(date_tmzn).split(' '))[0]).split('-')
    year = test[0]
    day = test[2]
    month = test[1]
    monthDict = {'01': 'Jan',
                 '02': 'Feb',
                 '03': 'Mar',
                 '04': 'Apr',
                 '05': 'May',
                 '06': 'Jun',
                 '07': 'Jul',
                 '08': 'Aug',
                 '09': 'Sep',
                 '10': 'Oct',
                 '11': 'Nov',
                 '12': 'Dec'}
    formattedDate = f'{dayWeek}, {monthDict[month]} {day}, {year}'
    # formattedDate = 'Mon, Dec 26, 2022'
    # print(formattedDate)
    return formattedDate


def games_today(today):
    dataframe = pd.read_excel('december.xlsx')
    rslt_df = dataframe[dataframe['Date'] == today]
    # print(rslt_df)
    rslt_df.to_excel('predictions.xlsx')
    df2 = pd.read_excel('predictions.xlsx')
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
    return winnerList, homeTeamList, oppTeamList, datesList


def team_name_to_abbreviation(matches, homeTeamList, oppTeamList):
    nba_teams = teams.get_teams()
    homeTeamSearch = [team for team in nba_teams if team['full_name'] == (homeTeamList[matches])][0]
    homeTeam_id = homeTeamSearch['id']
    homeTeam_abr = homeTeamSearch['abbreviation']
    oppTeamSearch = [team for team in nba_teams if team['full_name'] == (oppTeamList[matches])][0]
    oppTeam_id = oppTeamSearch['id']
    oppTeam_abr = oppTeamSearch['abbreviation']
    return homeTeam_abr, oppTeam_abr, homeTeam_id, oppTeam_id


def varying_sleep():
    randSleep = round((uniform(0.600, 0.900)), 3)
    sleep(randSleep)


def get_gameIDs_historical_matchups(homeTeam_abr, oppTeam_abr, homeTeam_id, season):

    gameFinder = teamgamelog.TeamGameLog(team_id=homeTeam_id, season=season)
    varying_sleep()

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
    return gamesIDAgainstOpp


def ff_algorithm_simulation_winner(homeCounter, oppCounter, homeTeam_abr,
                                   oppTeam_abr, tieCounter, gamesIDAgainstOpp, ids):

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

    home_four_factor_total = (home_EFG_PCT * 0.4) + (home_TOV_PCT * 0.25) + (home_OREB_PCT * 0.2) + (
            home_FTA_RATE * 0.15)
    opp_four_factor_total = (opp_EFG_PCT * 0.4) + (opp_TOV_PCT * 0.25) + (opp_OREB_PCT * 0.2) + (
            opp_FTA_RATE * 0.15)

    if home_four_factor_total > opp_four_factor_total:
        print(f"Simulation Winner:\t{homeTeam_abr}")
        homeCounter += 1
    elif opp_four_factor_total > home_four_factor_total:
        print(f"Simulation Winner\t{oppTeam_abr}")
        oppCounter += 1
    else:
        tieCounter += 1

    return homeCounter, oppCounter, tieCounter


def match_up_winner(homeCount, oppCount, homeTeam_abr, oppTeam_abr, homeTeamList, oppTeamList, winnerList, matches):
    if homeCount > oppCount:
        print(f"Match-up Winner\t{homeTeam_abr}\t\t{matches + 1}/{len(homeTeamList)}\n")
        winnerList.append(f"{homeTeamList[matches]}")
    elif oppCount > homeCount:
        print(f"Match-up Winner\t{oppTeam_abr}\t\t{matches + 1}/{len(homeTeamList)}\n")
        winnerList.append(f"{oppTeamList[matches]}")
    elif oppCount == homeCount:
        randTeam_abr = choice([homeTeamList[matches], oppTeamList[matches]])
        print(f"Match-up Winner\t{randTeam_abr}\t\t{matches + 1}/{len(homeTeamList)}\n")
        winnerList.append(f"{randTeam_abr}")
    return winnerList


def predictions_to_excel(winnerList):
    # print(winnerList)
    df3 = pd.read_excel('predictions.xlsx')
    df3['Winners'] = winnerList
    # print(df3)
    df3.to_excel('predictions.xlsx')
    print("Predicted winners added to December (predictions) spreadsheet.")


def main_backend(season):
    # global season, winnerList, homeTeamList, oppTeamList, datesList, gamesIDAgainstOpp, matches, homeTeam_abr, oppTeam_abr, ids, homeCount, oppCount
    dateToday = get_date()
    print(f'\nSimulating games and predicting winners for {dateToday}.\n'
          f'Based on historical data from the {season} NBA season.\n')
    winnerListInit, homeTeamList, oppTeamList, datesList = games_today(dateToday)
    winnerList = []
    for matches in range(len(homeTeamList)):
        varying_sleep()

        homeTeam_abr, oppTeam_abr, homeTeam_id, oppTeam_id = \
            team_name_to_abbreviation(matches, homeTeamList, oppTeamList)

        print(f"Match-up: {oppTeam_abr} @ {homeTeam_abr}")
        print(f"Simulating Match {matches + 1}/{len(homeTeamList)}")

        gamesIDAgainstOpp = get_gameIDs_historical_matchups(homeTeam_abr, oppTeam_abr, homeTeam_id, season)

        homeCounter, oppCounter, tieCounter = 0, 0, 0
        homeCount, oppCount, tieCount = 0, 0, 0
        for ids in range(len(gamesIDAgainstOpp)):
            varying_sleep()
            homeCount, oppCount, tieCount = \
                ff_algorithm_simulation_winner(homeCounter, oppCounter, homeTeam_abr,
                                               oppTeam_abr, tieCounter, gamesIDAgainstOpp, ids)

        winnerList = match_up_winner(homeCount, oppCount, homeTeam_abr, oppTeam_abr,
                                     homeTeamList, oppTeamList, winnerListInit, matches)

    predictions_to_excel(winnerList)


def getLogo(teamLastName):
    teamLogos = [
        'https://loodibee.com/wp-content/uploads/nba-atlanta-hawks-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-boston-celtics-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-brooklyn-nets-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-charlotte-hornets-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-chicago-bulls-logo-300x300.png',
        'https://media-s3-us-east-1.ceros.com/cleveland-cavaliers/images/2022/09/16/'
        '8783d53c340e66de35183fc6acb83a9d/primary-goldonwine.jpg',
        'https://loodibee.com/wp-content/uploads/nba-dallas-mavericks-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-denver-nuggets-logo-2018-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-detroit-pistons-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-golden-state-warriors-logo-2020-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-houston-rockets-logo-2020-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-indiana-pacers-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-la-clippers-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-los-angeles-lakers-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-memphis-grizzlies-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-miami-heat-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-milwaukee-bucks-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-minnesota-timberwolves-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-new-orleans-pelicans-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-new-york-knicks-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-oklahoma-city-thunder-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-orlando-magic-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-philadelphia-76ers-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-phoenix-suns-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-portland-trail-blazers-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-sacramento-kings-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-san-antonio-spurs-logo-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-toronto-raptors-logo-2020-300x300.png',
        'https://loodibee.com/wp-content/uploads/utah-jazz-logo-2022-300x300.png',
        'https://loodibee.com/wp-content/uploads/nba-washington-wizards-logo-300x300.png']
    logo = ''
    # teamLastName = 'raptors'
    for link in teamLogos:
        if teamLastName.lower() == 'nets':
            logo = 'https://loodibee.com/wp-content/uploads/nba-brooklyn-nets-logo-300x300.png'
        elif teamLastName.lower() in link:
            logo = link
    return logo


def get_predictions():
    df3 = pd.read_excel('predictions.xlsx')
    winnerList = []
    homeTeamList = []
    oppTeamList = []
    datesList = []
    for index in df3.index:
        homeTeamList.append((df3['Home/Neutral'][index]))
        oppTeamList.append((df3['Visitor/Neutral'][index]))
        winnerList.append((df3['Winners'][index]))
        datesList.append((df3['Date'][index]))
    return winnerList, homeTeamList, oppTeamList, datesList


def main_frontend(winnerList, homeTeamList, oppTeamList, datesList, season):
    st.success('Done!   See predicted winners below.')
    st.subheader(f"Games of {datesList[0]}.")
    st.write('#####')
    st.write('#####')
    for x in range(len(homeTeamList)):
        st.write('#####')
        col1, col2, col3 = st.columns(3)
        with st.container():
            with col1:
                full_name = homeTeamList[x]
                last_name = (full_name.split(' ')).pop()
                st.subheader("Home")
                st.subheader(full_name)
                # image = Image.open(getLogo(last_name))
                st.image(getLogo(last_name), width=100)

            with col2:
                full_name = oppTeamList[x]
                last_name = (full_name.split(' ')).pop()
                st.subheader("Away")
                st.subheader(full_name)
                # image = Image.open(getLogo(last_name))
                st.image(getLogo(last_name), width=100)

            with col3:
                full_name = winnerList[x]
                last_name = (full_name.split(' ')).pop()
                st.subheader("Pred. Winner")
                st.subheader(full_name)
                # image = Image.open(getLogo(last_name))
                st.image(getLogo(last_name), width=100)

            st.write('#####')
            st.write('#####')
            st.write('#####')
    st.write('#####')
    st.write('#####')
    st.write('#####')
    st.write('#####')
    st.write('#####')
    st.write('© Created by Shaf Muhammad')
    st.write('Logos owned by the NBA')
    st.write('shafmuhammad3@gmail.com')
    st.write(f'Predictions based on data from the {season} season.')
    st.write('Version 1.0.0')


def main(season):
    page_init()
    with st.spinner('Predicting Winners... This may take a minute.'):
        main_backend(season)
        winnerList, homeTeamList, oppTeamList, datesList = get_predictions()
        main_frontend(winnerList, homeTeamList, oppTeamList, datesList, season)


main(season='2020-21')
