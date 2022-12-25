from datetime import date
import pandas as pd

# Thu, Dec 1, 2022
dayWeek = (date.today().strftime('%A'))[:3]
test = str(date.today()).split('-')
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
print(formattedDate)

dataframe = pd.read_excel('december.xlsx')
rslt_df = dataframe[dataframe['Date'] == formattedDate]
print(rslt_df)



