from datetime import datetime,timedelta
from zoneinfo import ZoneInfo


eastern = ZoneInfo('America/New_York')


# datetime.datetime(2025, 3, 27, 11, 59, 59, 631706, tzinfo=zoneinfo.ZoneInfo(key='America/New_York'))
eastern_time = datetime.now(eastern)


# datetime.date(2025, 3, 27)
eastern_date = eastern_time.date()

def get_eastern_date():
    eastern = ZoneInfo('America/New_York')

    eastern_time = datetime.now(eastern)

    eastern_date = eastern_time.date()

    return eastern_date



def get_current_week_dates(input_date=None,week_offset=0):
    '''
    return format
    [datetime.date(2025, 3, 24),
    datetime.date(2025, 3, 25),
    datetime.date(2025, 3, 26),
    datetime.date(2025, 3, 27),
    datetime.date(2025, 3, 28),
    datetime.date(2025, 3, 29),
    datetime.date(2025, 3, 30)]
    '''
    if input_date is None:
        input_date = get_eastern_date()

    start_of_week = input_date - timedelta(days=input_date.weekday()) + timedelta(days=week_offset*7)

    return [start_of_week + timedelta(days=i) for i in range(7)]