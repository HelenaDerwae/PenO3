import datetime
import time
import Data_tables as dt


# --------SIMULATED-CLOCK--------
# def string(month, day, hour, minute):
#     """
#     String representation of the clock.
#     """
#     if month < 10:
#         month = '0' + str(month)
#         if day < 10:
#             day = '0' + str(day)
#             if hour < 10:
#                 hour = '0' + str(hour)
#                 if minute < 10:
#                     minute = '0' + str(minute)
#             else:
#                 if minute < 10:
#                     minute = '0' + str(minute)
#
#         else:
#             if day < 10:
#                 day = '0' + str(day)
#                 if hour < 10:
#                     hour = '0' + str(hour)
#                     if minute < 10:
#                         minute = '0' + str(minute)
#                 else:
#                     if minute < 10:
#                         minute = '0' + str(minute)
#             else:
#                 if hour < 10:
#                     hour = '0' + str(hour)
#                     if minute < 10:
#                         minute = '0' + str(minute)
#                 else:
#                     if minute < 10:
#                         minute = '0' + str(minute)
#     else:
#         if day < 10:
#             day = '0' + str(day)
#             if hour < 10:
#                 hour = '0' + str(hour)
#                 if minute < 10:
#                     minute = '0' + str(minute)
#             else:
#                 if minute < 10:
#                     minute = '0' + str(minute)
#         else:
#             if hour < 10:
#                 hour = '0' + str(hour)
#                 if minute < 10:
#                     minute = '0' + str(minute)
#             else:
#                 if minute < 10:
#                     minute = '0' + str(minute)
#     return '2018' + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute)
#
#
# def date_and_time():
#     """
#     Generates a simulation of one year.
#     """
#     datetime = []
#     for month in range(1,13):
#         if month in [1,3,5,7,8,10,12]:
#             for day in range(1,32):
#                 for hour in range(24):
#                     for minute in range(60):
#                         datetime.append(string(month, day, hour, minute))
#
#         elif month == 2:
#             for day in range(1,29):
#                 for hour in range(24):
#                     for minute in range(60):
#                         datetime.append(string(month, day, hour, minute))
#
#         else:
#             for day in range(1,31):
#                 for hour in range(24):
#                     for minute in range(60):
#                         datetime.append(string(month, day, hour, minute))
#     return datetime
#
#
# def simulated_clock(speed):
#     """
#     Returns the simulated time.
#     Speed makes the simulation going faster (24 is equivalent for one day in one minute).
#     """
#     timestamp = date_and_time()
#     start_time = time.clock()
#     while True:
#         time.sleep(1/speed)
#         index = int(round((time.clock() - start_time)*speed))
#         if index > 525600:
#             start_time = time.clock()
#             index = 0
#         simulated_date = timestamp[index]
#         dt.datetime.update_variable('datetime', simulated_date)
#
#
# def full_datetime_now():
#     """
#     Returns the full datetime of the moment of execution (incl. minutes).
#     """
#     now = dt.datetime.read_variable('datetime')
#     return now
#
#
# def full_time_now():
#     """
#     Returns the full time of the moment of execution (incl. minutes).
#     """
#     now = dt.datetime.read_variable('datetime')
#     return now[11:]
#
#
# def datetime_now():
#     """
#     Returns the datetime of the moment of execution.
#     """
#     now = dt.datetime.read_variable('datetime')
#     return now[0:14] + '00'
#
#
# def date_now():
#     """
#     Returns the date of the moment of execution.
#     """
#     now = dt.datetime.read_variable('datetime')
#     return now[0:10]
#
#
# def time_now():
#     """
#     Returns the time of the moment of execution.
#     """
#     now = dt.datetime.read_variable('datetime')
#     return now[11:13] + ':00'
#
#
# def previous_date():
#     """
#     Returns the previous date.
#     """
#     date = date_now()
#     previous_date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])) - datetime.timedelta(days=1)
#     return previous_date
#
#
# def next_date():
#     """
#     Returns the next date.
#     """
#     date = date_now()
#     next_day = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])) + datetime.timedelta(days=1)
#     return next_day
#
#
# def day_type():
#     """
#     Returns 'week' or 'weekend'.
#     """
#     date = date_now()
#     number = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])).isoweekday()
#     if number == 6 or number == 7:
#         return 'weekend'
#     else:
#         return 'week'
#
#
# if __name__ == '__main__':
#     simulated_clock(10000)


# ----------REAL-CLOCK----------
def full_datetime_now():
    """
    Returns the full datetime of the moment of execution (incl. minutes).
    """
    now = datetime.datetime.now()
    return now.strftime("2018-%m-%d %H:%M")


def full_time_now():
    """
    Returns the full time of the moment of execution (incl. minutes).
    """
    now = datetime.datetime.now()
    return now.strftime("%H:%M")


def datetime_now():
    """
    Returns the datetime of the moment of execution.
    """
    now = datetime.datetime.now()
    return now.strftime("2018-%m-%d %H:00")


def date_now():
    """
    Returns the date of the moment of execution.
    """
    now = datetime.datetime.now()
    return now.strftime("2018-%m-%d")


def time_now():
    """
    Returns the time of the moment of execution.
    """
    now = datetime.datetime.now()
    return now.strftime("%H:00")


def previous_date():
    """
    Returns the previous date.
    """
    previous_date = datetime.date.today() - datetime.timedelta(days=1)
    return previous_date


def next_date():
    """
    Returns the next date.
    """
    next_day = datetime.date.today() + datetime.timedelta(days=1)
    return next_day


def day_type():
    """
    Returns 'week' or 'weekend'.
    """
    date = datetime.date.today()
    number = datetime.date.isoweekday(date)
    if number == 6 or number == 7:
        return 'weekend'
    else:
        return 'week'
