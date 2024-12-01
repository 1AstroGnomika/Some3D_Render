from pygame.time import Clock
from Utils.Timer import Timer
from typing import Type
from Render.AbstractRender import AbstractRender
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from abc import ABC, abstractmethod

class AbstractApp(ABC):
    
    timer:Timer
    pygameTimer:Clock
    render:AbstractRender
    running:bool = True
    
    def __init__(self, frames:float, *args, **kwargs) -> None:
        self.timer = Timer(frames)
        self.pygameTimer = Clock()
        self.render = self.getRender()(*args, **kwargs)
    
    def update(self) -> None:
        self.timer.ticks()
        EventHandler.handle()
        InputHandler.handle()
        self.render.render()
        self.pygameTimer.tick(self.timer.ticksPerSecond)
        
    @abstractmethod
    def getRender(self) -> Type[AbstractRender]:
        ...