
from datetime import datetime


def get_current_date_time():
    date = datetime.now().date()
    time = datetime.now().time()

    day, month, year = date.day, date.month, date.year
    hour, minute = time.hour, time.minute
    current_date, current_time = f"{day}/{month}/{year}", f"{hour}:{minute}"

    return current_date, current_time


date, time = get_current_date_time()

print(date)