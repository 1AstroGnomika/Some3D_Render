from functools import lru_cache
from math import sin, cos, radians
from Utils.Vector3D import Vector3D

class Transform:

    TRANSFORM_CACHE:int = 4096
    point:Vector3D
    rotation:Vector3D
    __lastPoint:Vector3D

    def __init__(self, point:Vector3D, rotation:Vector3D) -> None:
        self.point = point
        self.rotation = rotation
        self.__lastPoint = point.copy()

    @lru_cache(maxsize=TRANSFORM_CACHE)
    def calculateAngles(pitch:float, yaw:float, roll:float) -> tuple[float, float, float, float, float, float]:
        return cos(pitch), sin(pitch), cos(yaw), sin(yaw), cos(roll), sin(roll)
    
    @lru_cache(maxsize=TRANSFORM_CACHE)
    def calculateRadians(pitch:float, yaw:float, roll:float) -> tuple[float, float, float]:
        return radians(pitch), radians(yaw), radians(roll)

    @lru_cache(maxsize=TRANSFORM_CACHE)
    def calculateRotationAngles(pitch:float, yaw:float, roll:float) -> tuple[float, float, float, float, float, float]:
        return Transform.calculateAngles(*Transform.calculateRadians(pitch, yaw, roll))

    @lru_cache(maxsize=TRANSFORM_CACHE)
    def calculateForward(rotation:tuple[float, float, float]) -> tuple[float, float, float]:
        cos_yaw, sin_yaw, cos_pitch, sin_pitch, cos_roll, sin_roll = Transform.calculateAngles(*rotation)
        return -sin_yaw * cos_pitch, sin_pitch, cos_yaw * cos_pitch
    
    @lru_cache(maxsize=TRANSFORM_CACHE)
    def calculateRight(rotation:tuple[float, float, float]) -> tuple[float, float, float]:
        cos_yaw, sin_yaw, cos_pitch, sin_pitch, cos_roll, sin_roll = Transform.calculateAngles(*rotation)
        return cos_yaw * cos_roll - sin_yaw * sin_roll, -cos_pitch * sin_roll, sin_yaw * cos_roll + cos_yaw * sin_roll
    
    @lru_cache(maxsize=TRANSFORM_CACHE)
    def calculateUp(rotation:tuple[float, float, float]) -> tuple[float, float, float]:
        cos_yaw, sin_yaw, cos_pitch, sin_pitch, cos_roll, sin_roll = Transform.calculateAngles(*rotation)
        return sin_roll, cos_roll, sin_roll
    
    @property
    def forvard(self) -> Vector3D:
        return Vector3D(*Transform.calculateForward(self.rotation.coordinates()))
    
    @property
    def right(self) -> Vector3D:
        return Vector3D(*Transform.calculateRight(self.rotation.coordinates()))

    @property
    def up(self) -> Vector3D:
        return Vector3D(*Transform.calculateUp(self.rotation.coordinates()))
    
    @property
    def shift(self) -> Vector3D:
        result:Vector3D = self.__lastPoint - self.position
        self.__lastPoint = self.position.copy()
        return result