from datetime import timedelta, date, time
from copy import deepcopy

def is_palindrome(n):
    str(n) == str(n)[::-1]

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def generate_formats(date):
    year_full = date.strftime("%Y")
    year_short = date.strftime("%y")

    month_full = date.strftime("%m")
    month_short = month_full.lstrip("0")

    day_full = date.strftime("%d")
    day_short = day_full.lstrip("0")

    date_formats = ["Mdyy", "MMdyy", "Mddyy", "MMddyy", "Mdyyyy", "MMdyyyy", "Mddyyyy", "MMddyyyy", "dMyy", "dMMyy", "ddMyy", "ddMMyy", "dMyyyy", "dMMyyyy", "ddMyyyy", "ddMMyyyy"]

    formatted_dates = []

    for df in date_formats:
        cp = deepcopy(df)

        cp = cp.replace("MM", month_full)
        cp = cp.replace("M", month_short)

        cp = cp.replace("yyyy", year_full)
        cp = cp.replace("yy", year_short)

        cp = cp.replace("dd", day_full)
        cp = cp.replace("d", day_short)

        formatted_dates.append(cp)

    return formatted_dates


def generate_days(year):

    days = daterange(date(year, 1, 1), date(year+1, 1, 1))

    formatted_days = []
    for day in days:
        formatted_days += generate_formats(day)

    return formatted_days


def generate_time_formats(time):
    time_formats = ["hmmss", "hhmmss", "Hmmss", "HHmmss"]

    hour_12_full = time.strftime("%I")
    hour_24_full = time.strftime("%H")

    hour_12_short = hour_12_full.lstrip("0")
    hour_24_short = hour_24_full.lstrip("0")

    min_full = time.strftime("%M")
    sec_full = time.strftime("%S")

    formatted_times= []

    for df in time_formats:
        cp = deepcopy(df)

        cp = cp.replace("HH", hour_24_full)
        cp = cp.replace("hh", hour_12_full)

        cp = cp.replace("H", hour_24_short)
        cp = cp.replace("h", hour_12_short)

        cp = cp.replace("mm", min_full)
        cp = cp.replace("ss", sec_full)

        formatted_times.append(cp)

    return formatted_times

def generate_times():
    formatted_times = []
    for h in range(0,24):
        for m in range(0,59):
            for s in range(0,59):
                formatted_times += generate_time_formats(time(h,m,s))
    return formatted_times

if __name__ == "__main__":
    n = int(input())
    for _ in range(0, n):
        year = int(input())

        days = generate_days(year)
        times = generate_times()

        count = 0
        for d in days:
            for t in times:
                if is_palindrome(d+t):
                    count += 1

        print(count)
