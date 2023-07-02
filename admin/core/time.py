from datetime import datetime

import pytz


def time():
    timezone = pytz.timezone('Asia/Tehran')
    now = datetime.now(timezone)
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time
