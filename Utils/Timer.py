from time import time

class Timer:
    
    DAY: int = 86400000
    HOUR: int = 3600000
    MINUTE: int = 60000
    SECOND: int = 1000
    MILLISECOND: int = 1
    HOURS_IN_DAY: int = DAY // HOUR
    MINUTES_IN_HOUR: int = HOUR // MINUTE
    SECONDS_IN_MINUTE: int = MINUTE // SECOND
    MILLISECONDS_IN_SECOND: int = SECOND // MILLISECOND
    lastTotalSeconds:float
    tickPerSecond:float
    lastTicks:float

    def __init__(self, tickPerSecond:float = 1000):
        self.lastTotalSeconds = Timer.getTotalMilliseconds()
        self.tickPerSecond = tickPerSecond
        self.lastTicks = float()

    def ticks(self) -> float:
        lastTotalSeconds = self.lastTotalSeconds
        self.lastTotalSeconds = Timer.getTotalMilliseconds()
        self.lastTicks = (self.lastTotalSeconds - lastTotalSeconds) * self.tickPerSecond
        return self.lastTicks
    
    @staticmethod
    def getTotalMilliseconds() -> int:
        return time()