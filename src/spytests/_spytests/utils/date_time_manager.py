from datetime import datetime, timedelta
from typing import Optional


class DateTimeManager:
    def __init__(self):
        self.start_time = datetime.now()
        self.finish_time = datetime.now()

    @property
    def now(self) -> datetime:
        return datetime.now()

    def now_str(self, datatime: Optional[datetime]) -> datetime:
        return self._format_datetime(datatime or self.now)

    def start_at(self) -> str:
        self.start_time = datetime.now()
        return self._format_datetime(self.start_time)

    def finish_at(self) -> str:
        self.finish_time = datetime.now()
        return self._format_datetime(self.finish_time)

    def running_time(self) -> str:
        running_time = self.finish_time - self.start_time
        return self._format_running_time(running_time)

    def _format_datetime(self, time: datetime) -> str:
        return time.strftime("%d.%m.%Y %H:%M:%S")

    def _format_running_time(self, time: timedelta) -> str:
        return f'{time.seconds}s, {time.microseconds} ms'
