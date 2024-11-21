from datetime import date
from datetime import datetime


def my_date():
    today = date.today()
    return str(today)


def my_time():
    now = datetime.now()
    return now.strftime("%I:%M-%p")

# print(my_date())
# print(my_time())
