from time import sleep
from Utils.Timer import Timer
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from App.AbstractApp import AbstractApp

class Game:

    timer:Timer
    app:AbstractApp

    def __init__(self, app:AbstractApp, framesPerSecond:float) -> None:
        self.timer = Timer(framesPerSecond)
        self.app = app

    def update(self) -> None:
        EventHandler.handle()
        InputHandler.handle()
        self.app.render.render()
        sleep(1 / self.timer.ticksPerSecond)