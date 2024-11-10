from math import radians, sin, cos
from typing import Iterable
from Utils.Vector3D import Vector3D

class RenderObject:

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

    def renderVectors(self) -> Iterable[Vector3D]:
        pitch = radians(self.pitch)
        yaw = radians(self.yaw)
        cos_pitch = cos(pitch)
        sin_pitch = sin(pitch)
        cos_yaw = cos(yaw)
        sin_yaw = sin(yaw)
        for edges in self.edges:
            for vertex in edges:
                vector:Vector3D = Vector3D(*tuple(map(lambda value: value * self.size, self.vertices[vertex])))
                y_rotated = vector.y * cos_pitch - vector.z * sin_pitch
                z_rotated = vector.y * sin_pitch + vector.z * cos_pitch
                yield Vector3D(vector.x * cos_yaw + z_rotated * sin_yaw, y_rotated, -vector.x * sin_yaw + z_rotated * cos_yaw) + self.point
    