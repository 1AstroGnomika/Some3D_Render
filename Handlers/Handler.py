from Utils.Tools import StaticClass, Events

class Handler(StaticClass):
    
    handlerEvents:Events = Events()

    def handle() -> None: ...