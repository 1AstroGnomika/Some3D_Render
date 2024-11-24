from datetime import datetime

class Timer:
    
    DAY:int = 864000000000
    HOUR:int = 36000000000
    MINUTE:int = 600000000
    SECOND:int = 10000000
    MILLISECOND:int = 100000
    HOURS_IN_DAY:int = DAY / HOUR
    MINUTES_IN_HOUR:int = HOUR / MINUTE
    SECONDS_IN_MINUTE:int = MINUTE / SECOND
    MILLISECONDS_IN_SECOND:int = SECOND / MILLISECOND
    lastTotalSeconds:float
    ticksPerSecond:float
    lastTicks:float

    def __init__(self, ticksPerSecond:float = 1000):
        self.lastTotalSeconds = Timer.getTotalSeconds()
        self.ticksPerSecond = ticksPerSecond
        self.lastTicks = float()

    def ticks(self) -> float:
        oLastTotalSeconds = self.lastTotalSeconds
        self.lastTotalSeconds = Timer.getTotalSeconds()
        self.lastTicks = ((self.lastTotalSeconds - oLastTotalSeconds) / self.SECOND) * self.ticksPerSecond
        return self.lastTicks
    
    @staticmethod
    def getTotalSeconds() -> float:
        return (datetime.now() - datetime(1, 1, 1)).total_seconds() * Timer.SECOND