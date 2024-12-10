from pygame import Surface
from Render.RenderObject import RenderObject
from Render.RenderContainer import RenderContainer
from Render.Camera import Camera
from Utils.Vector3D import Vector3D
from abc import ABC, abstractmethod

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
                if self.checkVisible(renderObject):
                    self.draw(renderObject)
        
    def checkVisible(self, renderObject:RenderObject) -> bool:
        distance:float = self.camera.point.distance(renderObject.point)
        if distance >= self.minRenderDistance and distance <= self.maxRenderDistance:
            width, height, depth = renderObject.dimensions
            screenX, screenY, screenZ = RenderObject.calculateScreenProjection(self.width, self.height, self.angle, self.camera.rotation.x, self.camera.rotation.y, self.camera.rotation.z, self.camera.viewVector(renderObject.point).coordinates())
            if screenZ > float():
                screenSizeX:float = ((self.width * width / screenZ) * self.angle) / 2
                screenSizeY:float = ((self.height * height / screenZ) * self.angle) / 2
                return screenX + screenSizeX >= float() and screenX - screenSizeX <= self.width or screenY + screenSizeY >= float() and screenY - screenSizeY <= self.height
            return screenZ >= -(depth / 2)
        return bool()
    
    @abstractmethod
    def draw(self, renderObject:RenderObject) -> None: ...
    
    @abstractmethod
    def render(self) -> None: ...

    @abstractmethod
    def initRender(self) -> None: ...