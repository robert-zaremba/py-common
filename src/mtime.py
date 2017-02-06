import calendar
from datetime import date, datetime


def to_unix(d):
    '''converts datetime object to unix time'''
    return calendar.timegm(d.timetuple())


def to_date(u):
    '''converts unix time to datetime.date object'''
    return date.fromtimestamp(u)


def to_dt(u):
    '''converts unix time to datetime.datetime object'''
    return datetime.fromtimestamp(u)


def fmt_unix_date(u):
    if u is None or u <= 0:
        return 'None'
    return to_date(u).strftime('%Y-%m-%d')


def fmt_unix(u):
    if u is None or u <= 0:
        return 'None'
    return to_dt(u).strftime('%Y-%m-%d %H:%M:%S')
