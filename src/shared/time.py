from datetime import datetime


def get_date_time_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
