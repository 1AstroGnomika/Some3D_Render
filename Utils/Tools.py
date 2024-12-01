import random
from typing import Any, Callable

class Events:

    class Event:

        func:Callable
        args:Any
        kwargs:Any

        def __init__(self, func:Callable, *args, **kwargs) -> None:
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def __call__(self) -> Any:
            return self.func(*self.args, **self.kwargs)
    
    PRE_EVENTS_INDEX:str = "pre"
    POST_EVENT_INDEX:str = "post"
    __pre_events:dict[str, list[Callable]]
    __post_events:dict[str, list[Callable]]
    
    def __init__(self) -> None:
        self.__pre_events = dict()
        self.__post_events = dict()
        
    def __call__(self, func:Callable) -> Callable:
        name:str = func.__name__
        for event_list in (
            self.__pre_events,
            self.__post_events
        ): event_list.setdefault(name, list())
        def decorator(*args, **kwargs):
            event:Events.Event = Events.Event(func, *args, **kwargs)
            for pre_event in tuple(self.__pre_events.get(name, tuple())):
                pre_event(event)
            result = event()
            for post_event in self.__post_events.get(name, tuple()):
                post_event(event)
            return result
        return decorator
          
    def __getattr__(self, name:str) -> Callable:
        def decorator(func:Callable) -> Callable:
            event_list:list[Callable] = None
            func_name:str = func.__name__.split("_").pop(0)
            if func_name == Events.PRE_EVENTS_INDEX:
                event_list = self.__pre_events.get(name)
            elif func_name == Events.POST_EVENT_INDEX:
                event_list = self.__post_events.get(name)
            if not event_list is None:
                event_list.append(func)
            return func
        return decorator
        
    def __delattr__(self, name:str) -> None:
        for event_list in (
            self.__pre_events,
            self.__post_events
        ): event_list.pop(name, None)

    def clearEvents(self) -> None:
        for event_list in (
            self.__pre_events,
            self.__post_events
        ):
            for events in tuple(event_list.values()):
                events.clear()

def limiter(Vmin:float, Vmax:float, value:int) -> float:
    return Vmin if value < Vmin else Vmax if value > Vmax else value

def procent(value:float, procent:float, max_procent:float = 100) -> float:
    return (value * procent / max_procent)

def eventProbabilyty(procent:float, maxProcent:float = 100.0) -> bool:
    return random.uniform(float(), maxProcent) + procent > maxProcent