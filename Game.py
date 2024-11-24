from pygame.time import Clock
from Utils.Timer import Timer
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from App.AbstractApp import AbstractApp

class Game:

    timer:Timer
    pygameTimer:Clock
    app:AbstractApp

    def __init__(self, app:AbstractApp, framesPerSecond:float) -> None:
        self.timer = Timer(framesPerSecond)
        self.pygameTimer = Clock()
        self.app = app

    def update(self) -> None:
        self.timer.ticks()
        EventHandler.handle()
        InputHandler.handle()
        self.app.render.render()
        self.pygameTimer.tick(self.timer.ticksPerSecond)