from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog, boxscorefourfactorsv2
from nba_api.stats.library.parameters import EndPeriod, EndRange, RangeType, StartPeriod, StartRange
import pandas as pd
from random import choice, uniform
import datetime
from time import sleep
import streamlit as st
import pytz


# Initializes the streamlit website.
# Optimized for desktop viewing.
def page_init():
    st.set_page_config(page_title="Today's NBA Predictions", layout='wide')
    st.header('NBA Predictions of The Day')


# Retrieves the current date, specifically formatted corresponding to the dates in the schedule.
def get_date():
    # Thu, Dec 1, 2022
    date_tmzn = datetime.datetime.now(pytz.timezone('EST'))
    # print(date_tmzn)
    dayWeek = (date_tmzn.strftime('%A'))[:3]
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
    # You can specify a date in the past or future, using the format below.
    # If you choose to manually specify a date, you must also manually change the file name for the monthly schedule.
    # formattedDate = 'Mon, Dec 26, 2022'
    # print(formattedDate)
    return formattedDate


# Retrieves the correct file name for the schedule of the current month.
def get_schedule():
    month = (datetime.datetime.now(pytz.timezone('EST'))).strftime('%B').lower()
    return f'{month}.xlsx'


# Filters all the games in the monthly schedule (spreadsheet) that will take place on the current day.
# Stores this data from required columns in a list, to be accessed later.
def games_today(today, schedule):
    dataframe = pd.read_excel(schedule)
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

    # print(homeTeamList)
    # print(oppTeamList)
    # print(datesList)
    return winnerList, homeTeamList, oppTeamList, datesList


# Converts the team's full name to its abbreviation.
def team_name_to_abbreviation(matches, homeTeamList, oppTeamList):
    nba_teams = teams.get_teams()

    homeTeamSearch = [team for team in nba_teams if team['full_name'] == (homeTeamList[matches])][0]
    homeTeam_id = homeTeamSearch['id']
    homeTeam_abr = homeTeamSearch['abbreviation']

    oppTeamSearch = [team for team in nba_teams if team['full_name'] == (oppTeamList[matches])][0]
    oppTeam_id = oppTeamSearch['id']
    oppTeam_abr = oppTeamSearch['abbreviation']

    return homeTeam_abr, oppTeam_abr, homeTeam_id, oppTeam_id


# Used to generate a downtime between 600ms and 900ms to try and bypass the NBA's bot prevention measures.
def varying_sleep():
    randSleep = round((uniform(0.600, 0.900)), 3)
    sleep(randSleep)


# Retrieves the game IDs of historical matchups between the two teams for the specified season.
# Stores these IDs as a list that is accessed later on and is used to calculate a team's Four Factor score.
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


# Calculates each team's Four Factor score for every match-up between the two teams.
# The highest Four Factor score is used to determine the winner of a 'simulation' match.
# The team with the most simulation match victories is concluded to be the predicted winner of the future match-up.
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


# Optional function that can be used as a tool to debug and analyze the in-depth findings of the Four Factor Algorithm.
def simulation_analysis(homeTeam_abr, oppTeam_abr,
                        home_EFG_PCT, home_TOV_PCT, home_OREB_PCT, home_FTA_RATE, home_four_factor_total,
                        opp_EFG_PCT, opp_TOV_PCT, opp_OREB_PCT, opp_FTA_RATE, opp_four_factor_total):

    print(f"\n\n{homeTeam_abr} Four Factor Breakdown:\n"
          f"1) {'Effective Field Goal %:':30} {home_EFG_PCT * 100:.2f}\n"
          f"2) {'Turnover %:':30} {home_TOV_PCT * 100:.2f}\n"
          f"3) {'Rebounding %:':30} {home_OREB_PCT * 100:.2f}\n"
          f"4) {'Free Throw Attempt %:':30} {home_FTA_RATE * 100:.2f}\n"
          f"----------------------------------------\n"
          f"{'Four Factor Total %:':33} {home_four_factor_total * 100:.2f}")

    print(f"\n{oppTeam_abr} Four Factor Breakdown:\n"
          f"1) {'Effective Field Goal %:':30} {opp_EFG_PCT * 100:.2f}\n"
          f"2) {'Turnover %:':30} {opp_TOV_PCT * 100:.2f}\n"
          f"3) {'Rebounding %:':30} {opp_OREB_PCT * 100:.2f}\n"
          f"4) {'Free Throw Attempt %:':30} {opp_FTA_RATE * 100:.2f}\n"
          f"---------------------------------------\n"
          f"{'Four Factor Total %:':33} {opp_four_factor_total * 100:.2f}")


# Determines the final winner of the future match-up based on the number of simulation victories of each team.
# Appends the name of the match-up team to a list of winners.
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


# The predicted winner of each match-up is added to a spreadsheet consisting of the match-ups of the current day.
def predictions_to_excel(winnerList):
    # print(winnerList)
    df3 = pd.read_excel('predictions.xlsx')
    df3['Winners'] = winnerList
    # print(df3)
    df3.to_excel('predictions.xlsx')
    # print("Predicted winners added to December (predictions) spreadsheet.")


# Backend data analysis, main function.
def main_backend(season):
    dateToday = get_date()
    schedule = get_schedule()

    print(f'\nSimulating games and predicting winners for {dateToday}.\n'
          f'Based on historical data from the {season} NBA season.\n')

    winnerListInit, homeTeamList, oppTeamList, datesList = games_today(dateToday, schedule)
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
    print('Backend data collection, analysis, and predictions have been completed successfully.')


# Retrieves the link to access the logo for each NBA team based on the team's last name.
def getLogo(teamLastName):
    logo = ''
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

    # teamLastName = 'raptors'
    for link in teamLogos:
        # Implemented a unique catch for the Nets as the function was confusing the file name with the Hornets.
        if teamLastName.lower() == 'nets':
            logo = 'https://loodibee.com/wp-content/uploads/nba-brooklyn-nets-logo-300x300.png'
        elif teamLastName.lower() in link:
            logo = link
    return logo


# Unpacks and retrieves the data and predictions stores in the spreadsheet containing the current predicted winners.
# Stores the match-up data in various lists to make displaying the outcomes easier.
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


# Frontend UI, main function.
def main_frontend(winnerList, homeTeamList, oppTeamList, datesList, season):
    st.success('Done!   See predicted winners below.')
    st.subheader(f"Games of {datesList[0]}.")

    st.write('#####')
    st.write('#####')

    for x in range(len(homeTeamList)):
        st.write('#####')
        homeColumn, awayColumn, winnerColumn = st.columns(3)

        with st.container():
            with homeColumn:
                full_name = homeTeamList[x]
                last_name = (full_name.split(' ')).pop()
                st.subheader("Home")
                st.subheader(full_name)
                st.image(getLogo(last_name), width=100)

            with awayColumn:
                full_name = oppTeamList[x]
                last_name = (full_name.split(' ')).pop()
                st.subheader("Away")
                st.subheader(full_name)
                st.image(getLogo(last_name), width=100)

            with winnerColumn:
                full_name = winnerList[x]
                last_name = (full_name.split(' ')).pop()
                st.subheader("Pred. Winner")
                st.subheader(full_name)
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


# Main function consisting of the backend and frontend of the application.
# Must specify the season you'd like to base the predictions off of.
def main(season):
    page_init()
    with st.spinner('Predicting Winners... This may take a minute.'):
        main_backend(season)
        winnerList, homeTeamList, oppTeamList, datesList = get_predictions()
        main_frontend(winnerList, homeTeamList, oppTeamList, datesList, season)


# Runs the application.
main(season='2020-21')
