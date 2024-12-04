from pygame import Surface
from Render.RenderObject import RenderObject
from Render.RenderContainer import RenderContainer
from Render.Camera import Camera
from Utils.Vector3D import Vector3D
from abc import ABC, abstractmethod
from typing import Optional

class AbstractRender(ABC):
    
    angle:float
    width:int
    height:int
    minRenderDistance:float
    maxRenderDistance:float
    display:Surface
    camera:Camera
    renderContainer:RenderContainer

    def __init__(self, angle:float, width:int, height:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        self.angle = angle
        self.width = width
        self.height = height
        self.minRenderDistance = minRenderDistance
        self.maxRenderDistance = maxRenderDistance
        self.camera = Camera(Vector3D(), Vector3D())
        self.renderContainer = RenderContainer()
        self.initRender()
    
    def drawAll(self) -> None:
        for renderObjects in tuple(self.renderContainer.renderObjects.values()):
            for renderObject in iter(renderObjects):
                distance:float = self.camera.point.distance(renderObject.point)
                checkDistance:bool = distance >= self.minRenderDistance and distance <= self.maxRenderDistance
                checkVisible:bool = self.onScreen(RenderObject.screenVertex(self.width, self.height, self.angle, self.camera.rotation.x, self.camera.rotation.y, self.camera.rotation.z, self.viewVector(renderObject.point).coordinates()))
                if checkDistance and checkVisible:
                    self.draw(renderObject)

    def viewVector(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.camera.point
    
    def onScreen(self, screenVertex:tuple[float, float]) -> bool:
        screenX, screenY = screenVertex
        return screenX >= float() and screenX <= self.width and screenY >= float() and screenY <= self.height
    
    @abstractmethod
    def draw(self, renderObject:RenderObject) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def initRender(self) -> None: ...