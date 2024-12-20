from pygame import Surface
from Render.AbstractRenderObject import AbstractRenderObject
from Render.RenderContainer import RenderContainer
from Render.AbstractCamera import AbstractCamera
from abc import ABC, abstractmethod

class AbstractRender(ABC):
    
    display:Surface
    camera:AbstractCamera
    renderContainer:RenderContainer

    def __init__(self, camera:AbstractCamera) -> None:
        self.camera = camera
        self.renderContainer = RenderContainer()
        self.initRender()
    
    def drawAll(self) -> None:
        for renderObjects in tuple(self.renderContainer.renderObjects.values()):
            for renderObject in sorted(iter(renderObjects), key=lambda renderObject: self.camera.point.distance(renderObject.point)):
                if renderObject := self.camera(renderObject):
                    self.draw(renderObject)
    
    @abstractmethod
    def draw(self, renderObject:AbstractRenderObject) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def initRender(self) -> None: ...