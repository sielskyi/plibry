
import datetimeutils as datetimeu

def main():

    datetimeu = DateTimeUtil()
    datetimeu.set_date_time(2018, 9, 26, 23, 36)
    print(datetimeu.get_date_time())
    datetimeu.limit_datetime_to_max(2017, 10, 25, 12, 50)
    print(datetimeu.get_date_time())
    datetimeu.add_any(50, 1, 3, 10, 25)
    print(datetimeu.get_date_time())

if __name__ is '__main__':
    main()