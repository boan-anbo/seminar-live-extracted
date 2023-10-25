import datetime

import pytz


def get_all_times(utc_time: datetime, localTimezone: str ):

    response = {}
    response['local'] = get_local_from_utc(utc_time, localTimezone)
    response['America/Los_Angeles'] = get_pst(utc_time)
    response['America/Chicago'] = utc_time.astimezone(pytz.timezone('America/Chicago'))
    response['America/New_York'] = get_est(utc_time)
    response['Europe/London'] = get_gmt(utc_time)
    response['Europe/Berlin'] = utc_time.astimezone(pytz.timezone('Europe/Berlin'))
    response['Europe/Moscow'] = utc_time.astimezone(pytz.timezone('Europe/Moscow'))
    response['Asia/Shanghai'] = get_cst(utc_time)
    response['Asia/Tokyo'] = utc_time.astimezone(pytz.timezone('Asia/Tokyo'))
    response['Australia/Sydney'] = utc_time.astimezone(pytz.timezone('Australia/Sydney'))

def get_est(utc_time: datetime) -> datetime:
    return utc_time.astimezone(pytz.timezone('America/New_York'))

def get_pst(utc_time: datetime) -> datetime:
    return utc_time.astimezone(pytz.timezone('America/Los_Angeles'))

def get_cst(utc_time: datetime) -> datetime:
    return utc_time.astimezone(pytz.timezone('Asia/Shanghai'))

def get_gmt(utc_time: datetime) -> datetime:
    return utc_time.astimezone(pytz.timezone('Europe/London'))

def get_local_from_utc(utc_time: datetime, timezone: str) -> datetime:
    return utc_time.astimezone(pytz.timezone(timezone))
