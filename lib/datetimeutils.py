# @file datetimeutils.py
# @brief Utilities for date and time manipulating.
# @author Sielskyi Leonid (sielskyi)
#

_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def check_year_is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_days_in_year(year):
    "year -> number of days in that year."
    if check_year_is_leap(year):
        return 366
    return 365


def get_days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, month
    if (month == 2) and (check_year_is_leap(year)):
        return 29
    return _DAYS_IN_MONTH[month]


class DateTimeUtil():
    "Class of date and time utilities"
    _year = 0
    _month = 1
    _day = 1
    _hour = 0
    _min = 0
    _sec = 0
    _msec = 0

    def __init__(self):
        _year = 0
        _month = 1
        _day = 1
        _hour = 0
        _min = 0
        _sec = 0
        _msec = 0

    def get_date_time(self):
        "Get datetime items"
        return (self._year, self._month, self._day, self._hour, self._min, self._sec, self._msec)

    def get_year(self):
        "Get Year value"
        return self._year

    def get_month(self):
        "Get Month value"
        return self._month

    def get_day(self):
        "Get Day value"
        return self._day

    def get_hours(self):
        "Get Hours value"
        return self._hour

    def get_minutes(self):
        "Get Minutes value"
        return self._min

    def get_seconds(self):
        "Get Seconds value"
        return self._sec

    def get_miliseconds(self):
        "Get Miliseconds value"
        return self._msecs

    def get_date_string_formated(self, format="YYYY-MM-DD"):
        "Get formated string of Date (Year, Month, Day)"
        if format == "yyyY-mM-dD":
            datestr = str(self._year)
            datestr += '-'
            datestr += str(self._month)
            datestr += '-'
            datestr += str(self._day)
        elif format == "YYYYMMDD":
            datestr = str(self._year)
            if self._month <= 9:
                datestr += '0'
            datestr += str(self._month)
            if self._day <= 9:
                datestr += '0'
            datestr += str(self._day)
        else:
            datestr = str(self._year)
            datestr += '-'
            if self._month <= 9:
                datestr += '0'
            datestr += str(self._month)
            datestr += '-'
            if self._day <= 9:
                datestr += '0'
            datestr += str(self._day)
        return datestr

    def get_time_string_formated(self, format="HH:MM:SS.MSS"):
        "Get formated string of Time (Hours, Minutes, Seconds, Miliseconds)"
        timestr = ''
        if format == "HH:MM":
            if self._hour <= 9:
                timestr += '0'
            timestr += str(self._hour)
            timestr += ':'
            if self._min <= 9:
                timestr += '0'
            timestr += str(self._min)
        elif format == "hH:hM":
            timestr += str(self._hour)
            timestr += ':'
            timestr += str(self._min)
        elif format == "hH:hM:sS.msS":
            timestr += str(self._hour)
            timestr += ':'
            timestr += str(self._min)
            timestr += ':'
            timestr += str(self._sec)
            timestr += '.'
            timestr += str(self._msec)
        else:
            if self._hour <= 9:
                timestr += '0'
            timestr += str(self._hour)
            timestr += ':'
            if self._min <= 9:
                timestr += '0'
            timestr += str(self._min)
            timestr += ':'
            if self._sec <= 9:
                timestr += '0'
            timestr += str(self._sec)
            timestr += '.'
            if self._msec <= 99:
                timestr += '0'
                if self._msec <= 9:
                    timestr += '0'
            timestr += str(self._msec)
        return timestr

    def set_date_time(self, year=0, month=1, day=1, hour=0, min=0, sec=0, msec=0):
        "Set datetime items"
        self.modify_date_time(year, month, day, hour, min, sec, msec)


    def modify_date_time(self, year=None, month=None, day=None, hour=None, min=None, sec=None, msec=None):
        "Modify datetime to specified values"
        if year is not None:
            self._year = year
        if month is not None:
            assert ((month >= 1) and (month <= 12)), 'Wrong value of month'
            self._month = month
        if day is not None:
            assert ((day >= 1) and (day <= get_days_in_month(self._year, self._month))), 'Wrong value of day'
            self._day = day
        if hour is not None:
            assert ((hour >= 0) and (hour <= 23)), 'Wrong value of hours'
            self._hour = hour
        if min is not None:
            assert ((min >= 0) and (min <= 59)), 'Wrong value of minutes'
            self._min = min
        if sec is not None:
            assert ((sec >= 0) and (sec <= 59)), 'Wrong value of seconds'
            self._sec = sec
        if msec is not None:
            assert ((msec >= 0) and (msec <= 999)), 'Wrong value of miliseconds'
            self._msec = msec

    def limit_datetime_to_max(self, year=None, month=None, day=None, hour=None, min=None, sec=None, msec=None):
        "Limit date-time to specified maximum value"
        if year is not None:
            if self._year > year:
                self.modify_date_time(year=year)
                if month is not None:
                    if self._month > month:
                        self.modify_date_time(month=month)
                        if day is not None:
                            if self._day > day:
                                self.modify_date_time(day=day)
                                if hour is not None:
                                    if self._hour > hour:
                                        self.modify_date_time(hour=hour)
                                        if min is not None:
                                            if self._min > min:
                                                self.modify_date_time(min=min)
                                                if sec is not None:
                                                    if self._sec > sec:
                                                        self.modify_date_time(sec=sec)
                                                        if msec is not None:
                                                            if self._msec > msec:
                                                                self.modify_date_time(msec=msec)

    def limit_datetime_to_min(self, year=None, month=None, day=None, hour=None, min=None, sec=None, msec=None):
        "Limit date-time to specified minimum value"
        if year is not None:
            if self._year < year:
                self.modify_date_time(year=year)
                if month is not None:
                    if self._month < month:
                        self.modify_date_time(month=month)
                        if day is not None:
                            if self._day < day:
                                self.modify_date_time(day=day)
                                if hour is not None:
                                    if self._hour < hour:
                                        self.modify_date_time(hour=hour)
                                        if min is not None:
                                            if self._min < min:
                                                self.modify_date_time(min=min)
                                                if sec is not None:
                                                    if self._sec < sec:
                                                        self.modify_date_time(sec=sec)
                                                        if msec is not None:
                                                            if self._msec < msec:
                                                                self.modify_date_time(msec=msec)

    def add_any(self, years=0, months=0, days=0, hours=0, mins=0, secs=0, msecs=0):
        "add date-time values counting from any values of arguments"
        self.set_from_any((self._year + years), (self._month + months - 1), (self._day + days - 1),
                          (self._hour + hours), (self._min + mins), (self._sec + secs), (self._msec + msecs))

    def set_from_any(self, years=0, months=0, days=0, hours=0, mins=0, secs=0, msecs=0):
        "get date-time values counting from any values of arguments"
        secs += int(msecs / 1000)
        msecs %= 1000
        mins += int(secs / 60)
        secs %= 60
        hours += int(mins / 60)
        mins %= 60
        days += int(hours / 24)
        hours %= 24

        while True:
            years += int(months / 12)
            months %= 12
            if months == 0:
                while True:
                    days_in_year = get_days_in_year(years)
                    if days >= days_in_year:
                        days -= days_in_year
                        years += 1
                    else:
                        break
            days_in_month = get_days_in_month(years, (months + 1))
            if days >= days_in_month:
                days -= days_in_month
                months += 1
            else:
                break

        days += 1
        months += 1
        self.set_date_time(years, months, days, hours, mins, secs, msecs)

