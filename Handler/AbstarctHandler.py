from abc import ABC, abstractstaticmethod
from Utils.Tools import Events

class AbstarctHandler(ABC):
    
    handlerEvents:Events = Events()

    @abstractstaticmethod
    def handle() -> None: ...