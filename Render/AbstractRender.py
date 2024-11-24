from pygame import Surface
from Render.RenderObject import RenderObject
from Render.RenderContainer import RenderContainer
from Render.Camera import Camera
from Utils.Vector3D import Vector3D
from abc import ABC, abstractmethod

class AbstractRender(ABC):
    
    angle:float
    width:int
    heigth:int
    minRenderDistance:float
    maxRenderDistance:float
    display:Surface
    camera:Camera
    renderContainer:RenderContainer

    def __init__(self, angle:float, width:int, heigth:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        self.angle = angle
        self.width = width
        self.heigth = heigth
        self.minRenderDistance = minRenderDistance
        self.maxRenderDistance = maxRenderDistance
        self.camera = Camera(Vector3D())
        self.renderContainer = RenderContainer()
        self.initRender()
    
    def drawAll(self) -> None:
        for renderObjects in tuple(self.renderContainer.renderObjects.values()):
            for renderObject in iter(renderObjects):
                distance:float = self.camera.position.distance(renderObject.point)
                checkDistance:bool = distance >= self.minRenderDistance and distance <= self.maxRenderDistance
                checkVisible:bool = RenderObject.vertex(self.camera.rotation.y, self.camera.rotation.x, self.camera.rotation.z, (self.camera.position - renderObject.point).coordinates(), renderObject.size)[-1] >= float()
                if checkDistance and checkVisible:
                    self.draw(renderObject)
    
    @abstractmethod
    def draw(self, renderObject:RenderObject) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def initRender(self) -> None: ...