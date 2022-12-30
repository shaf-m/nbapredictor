# Welcome to nbapredictor

## Overview
This is a full-stack web-based application that was created to predict the winners of future NBA games.
All data manipulation is done using Pandas.
The winners of each match-up are predicted based on simulation games, which are based on Four Factor calculations of each match-up.
The program commences by determining the current date in the eastern time zone (EST).
The NBA schedule for the rest of the 2022-23 season is stored in individual Excel spreadsheets corresponding to each month, accessed from [Basketball Reference](https://www.basketball-reference.com/).
Based on the current month, the NBA schedule is accessed and opened.
The program then accesses and filters the schedule to only display the schedule for the current (or manually specified) day.
Next, the program creates 'bundles' for each match-up, corresponding to the home and away teams in the match-up.
Using the unofficial [NBA API](https://github.com/swar/nba_api), the historical match-ups between the teams in each bundle are extracted.
This data is then used to determine the Four Factor score of each team, in each match-up, in each bundle see the corresponding section below).
Then, for each historical matchup, the program runs 'simulation matches', based solely on the Four Factor calculations.
The team with the most simulation match victories in each match-up will be concluded to be the predicted winner of that match-up.
This data is then stored inside the initial Excel spreadsheet consisting of the daily schedule, however, a new column is added that displays the predicted winner of each match-up.
This spreadsheet is used to extract data-frames for each match-up, which are used as data libraries to extract the information and display it in a clean, modern user interface (see examples below). The information is displayed in three columns; home team, away team, and the predicted (pred.) winner of each match-up. Furthermore, the logos for each NBA team are displayed by accessing links for these images through [Loodibee](https://loodibee.com/nba/). In addition,  the UI supports dark and light mode, toggled automatically by accessing the user’s default browser theme setting. 
The frontend of this application was created, deployed and hosted through [Streamlit](https://streamlit.io/). Streamlit is an open source app framework in Python, which is commonly used for machine learning and data science purposes. This application was designed through multiple input (read) and output (write) Excel spreadsheets to make it simpler for a backend tester to debug and also further analyze the calculations and data. Although the accuracy of these predictions have been 65-70% accurate, these predictions can be more accurately made if virtual machines and scikit-learn were used to run simultaneous simulations for multiple seasons at once (current, and past three NBA seasons).


## The Four Factors of Basketball

How do basketball teams win games?
While searching for an answer to that question, Dean Oliver identified what he called the "Four Factors of Basketball Success".
The four factors are to score efficiently, protect the basketball on offense, grab as many rebounds as possible, and get to the foul line as often as possible.
The number in parentheses is the approximate weight assigned to each factor. Shooting is the most important factor, followed by turnovers, rebounding, and free throws.


| Factor  | Shooting  | Turnovers  | Rebounding | Free Throws |
| :------------: | :------------: |:---------------:| :-----:|:------------: 
| Weighting  | 40% | 25% | 20% | 15% |


#### 1. Shooting
- The shooting factor is measured using Effective Field Goal Percentage (eFG%). The formula for both offense and defense is $$(FG + 0.5 * 3P) / FGA$$

#### 2. Turnovers
- The turnover factor is measured using Turnover Percentage (TOV%). The formula for both offense and defense is $$TOV / (FGA + 0.44 * FTA + TOV)$$

#### 3. Rebounding
- The rebounding factor is measured using ORB%. The formula for offensive rebounding is $$ORB / (ORB + Opp DRB)$$

#### 4. Free Throws
- The free throw factor is a measure of both how often a team gets to the line and how often they make them. The formula for both offense and defense is $$FT / FGA$$


## UI and Demonstration

The following is a demonstration for the predictions (based on data from the 2020-21 season) of Tuesday, December 27th, 2022.
Comparing the predictions to the final scores, we see 7/10 games were predicted correctly, giving us an accuracy of 70%.
Of the games that were inaccurately predicted, the final score margin was very slim, of under 10 points.
As mentioned in the Overview, these predictions can be more accurately made if virtual machines were used to run simultaneous simulations for multiple seasons at once (current, and past three NBA seasons). However, considering data from only a single season was used and yielded in an accuracy of 70%, this is quite appreciable.


https://user-images.githubusercontent.com/121407023/210023224-0d722f09-96a1-49ef-8572-b84aba393ad0.mov

[December 27th Predictions.pdf](https://github.com/shaf-m/nbapredictor/files/10322624/December.27th.Predictions.pdf)

[NBA Dec 27th Final Scores.pdf](https://github.com/shaf-m/nbapredictor/files/10322625/NBA.Dec.27th.Final.Scores.pdf)

<hr>

In order to limit call requests to the API, the website is currently closed to the public. 
If you'd like to experience nbapredictor for yourself, or if you have any questions, comments, or suggestions, please feel free to reach out to me by email at shafmuhammad3@gmail.com.

