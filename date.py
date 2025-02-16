from datetime import datetime as dt, timedelta

def get_today_date():
    now = dt.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%A"), now.weekday()

def get_future_date(int):
    now = dt.now()
    future_date = now + timedelta(days=int)
    return future_date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    full_date = get_today_date()[0]
    day = get_today_date()[1]
    int_day = get_today_date()[2]
    future = get_future_date(2)

    print(f"full_date: {full_date}") 
    print(f"day: {day}")
    print(f"int day: {int_day}")
    print(f"future: {future}")
