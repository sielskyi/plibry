

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
    if month == 2 and check_year_is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


class DateTimeUtil():
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

    def set_date_time(self, year=0, month=1, day=1, hour=0, min=0, sec=0, msec=0):
        "Set datetime items"
        assert (month >= 1 and month <= 12), 'Wrong value of month'
        assert (day >= 1 and day <= get_days_in_month(year, month)), 'Wrong value of day'
        assert (hour >= 0 and hour <= 23), 'Wrong value of hours'
        assert (min >= 0 and min <= 59), 'Wrong value of minutes'
        assert (sec >= 0 and sec <= 59), 'Wrong value of seconds'
        assert (msec >= 0 and msec <= 999), 'Wrong value of miliseconds'

        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._min = min
        self._sec = sec
        self._msec = msec

    def limit_date_to_max(self, year=None, month=None, day=None):
        "Limit date to specified value"
        if year != None:
            if self._year > year:
                self._year = year
        if month != None:
            assert (month >= 1 and month <= 12), 'Wrong value of month'
            if self._month > month:
                self._month = month
        if day != None:
            assert (day >= 1 and day <= get_days_in_month(year, month)), 'Wrong value of day'
            if self._day > day:
                self._day = day

    def set_from_any(self, years=0, months=0, days=0, hours=0, mins=0, secs=0, msecs=0):
        "get real date-time values counting from any values of arguments"
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

