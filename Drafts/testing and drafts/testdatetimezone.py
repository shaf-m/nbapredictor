import datetime
import pytz

# Thu, Dec 1, 2022
# date_x = date.today(pytz.timezone('Canada'))
# dayWeek = (date.today().strftime('%A'))[:3]
# test = str(date.today()).split('-')
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
print(formattedDate)
