from pygame import Surface
from Render.RenderObject import RenderObject
from Render.RenderContainer import RenderContainer
from Render.Camera import Camera
from Utils.Vector3D import Vector3D
from abc import ABC, abstractmethod

class AbstractRender(ABC):
    
    width:int
    height:int
    minRenderDistance:float
    maxRenderDistance:float
    display:Surface
    camera:Camera
    renderContainer:RenderContainer

    def initParameters(self, alpha:float, width:int, height:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        self.width = width
        self.height = height
        self.minRenderDistance = minRenderDistance
        self.maxRenderDistance = maxRenderDistance
        self.camera = Camera(Vector3D(z=alpha), Vector3D())
        self.renderContainer = RenderContainer()
        self.initRender()

    @abstractmethod
    def initRender(self) -> None: ...
    
    @abstractmethod
    def draw(self, renderObject:RenderObject) -> None: ...
    
    @abstractmethod
    def drawAll(self) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...