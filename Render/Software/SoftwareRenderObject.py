from math import sin, cos, radians
from functools import lru_cache
from Meshes.Mesh import Mesh
from Render.AbstractRenderObject import AbstractRenderObject

class SoftwareRenderObject(AbstractRenderObject):

    SOFTWARE_RENDER_CACHE:int = 256
    
    mesh:Mesh = None

    def processMesh(self, mesh:Mesh) -> None:
        self.mesh = mesh
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateScale(coordinates:tuple[float, float, float], size:tuple[float, float, float]) -> tuple[float, float, float]:
        return (coordinates[0] * size[0], coordinates[1] * size[1], coordinates[2] * size[2])

    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateAngles(pitch:float, yaw:float, roll:float) -> tuple[float, float, float, float, float, float]:
        return cos(pitch), sin(pitch), cos(yaw), sin(yaw), cos(roll), sin(roll)
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateRadians(pitch:float, yaw:float, roll:float) -> tuple[float, float, float]:
        return radians(pitch), radians(yaw), radians(roll)

    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateRotationAngles(pitch:float, yaw:float, roll:float) -> tuple[float, float, float, float, float, float]:
        return SoftwareRenderObject.calculateAngles(*SoftwareRenderObject.calculateRadians(pitch, yaw, roll))
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateRotate(coordinates:tuple[float, float, float], cos_pitch:float, sin_pitch:float, cos_yaw:float, sin_yaw:float, cos_roll:float, sin_roll:float) -> tuple[float, float, float]:
        x, y, z = coordinates
        x_rot = x * cos_roll - y * sin_roll
        y_rot = x * sin_roll + y * cos_roll
        z_rot = z
        y_final = y_rot * cos_yaw - z_rot * sin_yaw
        z_rot_final = y_rot * sin_yaw + z_rot * cos_yaw
        return (x_rot * cos_pitch + z_rot_final * sin_pitch, y_final, -x_rot * sin_pitch + z_rot_final * cos_pitch)
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateCoordinates(pitch:float, yaw:float, roll:float, size:tuple[float, float, float], coordinates:tuple[float, float, float]) -> tuple[float, float, float]:
        return SoftwareRenderObject.calculateRotate(SoftwareRenderObject.calculateScale(coordinates, size), *SoftwareRenderObject.calculateRotationAngles(pitch, yaw, roll))