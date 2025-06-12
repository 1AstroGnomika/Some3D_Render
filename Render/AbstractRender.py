from pygame import Surface
from typing import Iterable
from Render.AbstractRenderObject import AbstractRenderObject
from Render.AbstractCamera import AbstractCamera
from abc import ABC, abstractmethod

class AbstractRender(ABC):
    
    display:Surface
    camera:AbstractCamera
    renderObjects:Iterable[AbstractRenderObject] = None

    def __init__(self, camera:AbstractCamera) -> None:
        self.camera = camera
        self.initRender()
    
    def drawAll(self) -> None:
        if self.renderObjects:
            for renderObject in sorted(self.renderObjects, key=lambda renderObject: self.camera.point.distance(renderObject.point), reverse=True):
                if renderObject := self.camera(renderObject):
                    self.draw(renderObject)
    
    @abstractmethod
    def draw(self, renderObject:AbstractRenderObject) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def initRender(self) -> None: ...