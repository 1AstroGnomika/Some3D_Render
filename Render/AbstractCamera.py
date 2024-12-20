from abc import abstractmethod
from Render.AbstacrtTransform import AbstacrtTransform
from Render.AbstractRenderObject import AbstractRenderObject
from Utils.Vector3D import Vector3D

class AbstractCamera(AbstacrtTransform):
    
    angle:float
    width:int
    height:int
    minRenderDistance:float
    maxRenderDistance:float

    def __init__(self, angle:float, width:int, height:int, minRenderDistance:float, maxRenderDistance:float, point:Vector3D=None, rotation:Vector3D=None) -> None:
        self.angle = angle
        self.width = width
        self.height = height
        self.minRenderDistance = minRenderDistance
        self.maxRenderDistance = maxRenderDistance
        super().__init__(point or Vector3D(), rotation or Vector3D())

    @abstractmethod
    def __call__(self, renderObject:AbstractRenderObject) -> AbstractRenderObject: ... 