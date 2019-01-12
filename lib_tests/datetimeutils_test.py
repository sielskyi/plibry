import datetime
from datetimeext import *

def main():

    dte = DateTimeExt()
    dte.set_date_time(2018, 9, 26, 23, 36)
    assert (dte.get)
    print(dte.get_date_time())
    dte.limit_datetime_to_max(2017, 10, 25, 12, 50)
    print(dte.get_date_time())
    dte.add_any(50, 1, 3, 10, 25)
    print(dte.get_date_time())

if __name__ is '__main__':
    main()