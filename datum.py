from tkinter import *
import datetime

now = datetime.datetime.now()
now.strftime('%Y-%m-%d')

def tomorrow():
    if int(now.strftime('%m')) == 2:
        tomorrow_year = int(now.strftime('%y'))
        if int(now.strftime('%d')) == 28:
            tomorrow_month = int(now.strftime('%m')) + 1
            tomorrow_day = 1
        else:
            tomorrow_month = int(now.strftime('%m'))
            tomorrow_day = int(now.strftime('%d')) + 1
    elif int(now.strftime('%m')) == 4 or 6 or 9 or 11:
        tomorrow_year = int(now.strftime('%y'))
        if int(now.strftime('%d')) == 30:
            tomorrow_month = int(now.strftime('%m')) + 1
            tomorrow_day = 1
        else:
            tomorrow_month = int(now.strftime('%m'))
            tomorrow_day = int(now.strftime('%d')) + 1
    elif datetime.date.month == 12:
        if datetime.date.day == 31:
            tomorrow_month = 1
            tomorrow_day = 1
            tomorrow_year = int(now.strftime('%y')) + 1
        else:
            tomorrow_month = int(now.strftime('%m'))
            tomorrow_day = int(now.strftime('%d')) + 1
            tomorrow_year = int(now.strftime('%y'))
    tomorrow_date = (str(tomorrow_year) + '-' + str(tomorrow_month) + '-' + str(tomorrow_day))
    return tomorrow_date
