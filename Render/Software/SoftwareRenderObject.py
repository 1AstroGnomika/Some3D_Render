from math import sin, cos, radians
from functools import lru_cache
from Render.AbstractRenderObject import AbstractRenderObject

class SoftwareRenderObject(AbstractRenderObject):

    SOFTWARE_RENDER_CACHE:int = 256

    def dimensions(self) -> tuple[float, float, float]:
        return SoftwareRenderObject.calculateDimensions(SoftwareRenderObject.calculateVertices(*self.rotation.coordinates(), self.size, self.vertices))
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateScale(coordinates:tuple[float, float, float], size:float) -> tuple[float, float, float]:
        return tuple(map(lambda coordinate: coordinate * size, coordinates))

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
    def calculateCoordinates(pitch:float, yaw:float, roll:float, size:float, coordinates:tuple[float, float, float]) -> tuple[float, float, float]:
        return SoftwareRenderObject.calculateRotate(SoftwareRenderObject.calculateScale(coordinates, max(size, float())), *SoftwareRenderObject.calculateRotationAngles(pitch, yaw, roll))
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateDimensions(points:tuple[tuple[float, float, float]]) -> tuple[float, float, float]:
        min_x = min_y = min_z = float()
        max_x = max_y = max_z = float()
        for point in points:
            x, y, z = point
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            min_z = min(min_z, z)
            max_z = max(max_z, z)
        return max_x - min_x, max_y - min_y, max_z - min_z
    
    @lru_cache(maxsize=SOFTWARE_RENDER_CACHE)
    def calculateVertices(pitch:float, yaw:float, roll:float, size:float, vertices:tuple[tuple[float, float, float]]) -> tuple[tuple[float, float, float]]:
        return tuple(map(lambda vertex: SoftwareRenderObject.calculateCoordinates(pitch, yaw, roll, size, vertex), vertices))
