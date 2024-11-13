from functools import lru_cache
from math import radians, sin, cos
from typing import Iterable
from Utils.Vector3D import Vector3D

class RenderObject:

    RENDER_CACHE:int = 256
    vertices:list[tuple[float]]
    edges:list[tuple[int]]
    point:Vector3D
    pitch:float
    yaw:float
    size:float

    def __init__(self, vertices:list[tuple[float]], edges:list[tuple[int]], point:Vector3D, pitch:float, yaw:float, size:float) -> None:
        self.vertices = vertices
        self.edges = edges
        self.point = point
        self.pitch = pitch
        self.yaw = yaw
        self.size = size

    @lru_cache(maxsize=RENDER_CACHE)
    @staticmethod
    def calculateRotationAngles(pitch:float, yaw:float) -> tuple[float, float, float, float]:
        pitch = radians(pitch)
        yaw = radians(yaw)
        cos_pitch = cos(pitch)
        sin_pitch = sin(pitch)
        cos_yaw = cos(yaw)
        sin_yaw = sin(yaw)
        return cos_pitch, sin_pitch, cos_yaw, sin_yaw

    @lru_cache(maxsize=RENDER_CACHE)
    @staticmethod
    def scaleVertex(vertices:tuple[float, float, float], size:float) -> tuple[float, float, float]:
        return tuple(map(lambda value: value * size, vertices))

    @lru_cache(maxsize=RENDER_CACHE)
    @staticmethod
    def rotateVertex(coordinates:tuple[float, float, float], cos_pitch:float, sin_pitch:float, cos_yaw:float, sin_yaw:float) -> tuple[float, float, float]:
        x, y, z = coordinates
        y_rotated = y * cos_pitch - z * sin_pitch
        z_rotated = y * sin_pitch + z * cos_pitch
        x_rotated = x * cos_yaw + z_rotated * sin_yaw
        z_rotated_final = -x * sin_yaw + z_rotated * cos_yaw
        return x_rotated, y_rotated, z_rotated_final
    
    @lru_cache(maxsize=RENDER_CACHE)
    @staticmethod
    def renderVector(pitch:float, yaw:float, vertice:tuple[float, float, float], size:float) -> Vector3D:
        cos_pitch, sin_pitch, cos_yaw, sin_yaw = RenderObject.calculateRotationAngles(pitch, yaw)
        scaled_vector = RenderObject.scaleVertex(vertice, max(size, float()))
        rotated_vector = RenderObject.rotateVertex(scaled_vector, cos_pitch, sin_pitch, cos_yaw, sin_yaw)
        return Vector3D(*rotated_vector)
    
    @lru_cache(maxsize=RENDER_CACHE)
    @staticmethod
    def checkVectorDistance(fromPos:tuple[float, float, float], toPos:tuple[float, float, float], minDistance:float, maxDistance:float) -> bool:
        distance:float = Vector3D(*fromPos).distance(Vector3D(*toPos))
        return distance >= minDistance and distance <= maxDistance

    def renderVectors(self) -> Iterable[Vector3D]:
        for edge in self.edges:
            for vertex_index in edge:
                yield RenderObject.renderVector(self.pitch, self.yaw, self.vertices[vertex_index], self.size)
