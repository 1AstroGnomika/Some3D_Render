from math import sin, cos
from abc import ABC
from Utils.Vector3D import Vector3D

class AbstractTransform(ABC):

    point:Vector3D
    rotation:Vector3D

    def __init__(self, point:Vector3D, rotation:Vector3D) -> None:
        self.point = point
        self.rotation = rotation

    def forward(self) -> Vector3D:
        cos_x, sin_x, cos_y, sin_y = cos(self.rotation.x), sin(self.rotation.x), cos(self.rotation.y), sin(self.rotation.y)
        return Vector3D(-sin_x * cos_y, sin_y, cos_x * cos_y)
    
    def right(self) -> Vector3D:
        return Vector3D(cos(self.rotation.x), float(), sin(self.rotation.x))

    def up(self) -> Vector3D:
        return Vector3D(float(), cos(self.rotation.z), float())