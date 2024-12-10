from pygame import Surface
from Render.RenderObject import RenderObject
from Render.RenderContainer import RenderContainer
from Render.Camera import Camera
from abc import ABC, abstractmethod

class AbstractRender(ABC):
    
    display:Surface
    camera:Camera
    renderContainer:RenderContainer

    def __init__(self, camera:Camera) -> None:
        self.camera = camera
        self.renderContainer = RenderContainer()
        self.initRender()
    
    def drawAll(self) -> None:
        for renderObjects in tuple(self.renderContainer.renderObjects.values()):
            for renderObject in iter(renderObjects):
                if self.camera.visible(renderObject):
                    self.draw(renderObject)
    
    @abstractmethod
    def draw(self, renderObject:RenderObject) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def initRender(self) -> None: ...