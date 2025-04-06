
from datetime import timedelta

class Plan:
    def __init__(self, name, daily_limit_gb, wait_time_sec, duration_days=None):
        self.name = name
        self.daily_limit_bytes = daily_limit_gb * 1024 * 1024 * 1024
        self.wait_time_sec = wait_time_sec
        self.duration = timedelta(days=duration_days) if duration_days else None

PLANS = {
    'free': Plan('Free', 1, 180),
    'silver': Plan('Silver', 5, 30, duration_days=30),
    'gold': Plan('Gold', 10, 0, duration_days=30),
    'diamond': Plan('Diamond', 30, 0, duration_days=30),
}
