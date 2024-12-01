from App.AbstractApp import AbstractApp

class GameLogic:

    App:AbstractApp = None
    
    def __new__(cls, *args, **kwargs) -> None:
        raise TypeError(f"Class object {cls.__name__} cannot be create!")
    
    @staticmethod
    def mainLoop() -> None:
        while GameLogic.App.running:
            GameLogic.App.update()