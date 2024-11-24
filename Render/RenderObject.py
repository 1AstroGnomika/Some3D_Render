from functools import lru_cache
from math import radians, sin, cos
from typing import Iterable
from Utils.Vector3D import Vector3D

class RenderObject:

    RENDER_CACHE: int = 512
    vertices: list[tuple[float]]
    edges: list[tuple[int]]
    point: Vector3D
    pitch: float
    yaw: float
    roll: float
    size: float

    def __init__(self, vertices: list[tuple[float]], edges: list[tuple[int]], point: Vector3D, pitch: float, yaw: float, roll: float, size: float) -> None:
        self.vertices = vertices
        self.edges = edges
        self.point = point
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.size = size

    @lru_cache(maxsize=RENDER_CACHE)
    def calculateRotationAngles(pitch: float, yaw: float, roll: float) -> tuple[float, float, float, float, float, float]:
        pitch = radians(pitch)
        yaw = radians(yaw)
        roll = radians(roll)
        cos_pitch, sin_pitch = cos(pitch), sin(pitch)
        cos_yaw, sin_yaw = cos(yaw), sin(yaw)
        cos_roll, sin_roll = cos(roll), sin(roll)
        return cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll

    @lru_cache(maxsize=RENDER_CACHE)
    def scaleVertex(vertices: tuple[float, float, float], size: float) -> tuple[float, float, float]:
        return tuple(map(lambda value: value * size, vertices))

    @lru_cache(maxsize=RENDER_CACHE)
    def rotateVertex(coordinates: tuple[float, float, float], cos_pitch: float, sin_pitch: float, cos_yaw: float, sin_yaw: float, cos_roll: float, sin_roll: float) -> tuple[float, float, float]:
        x, y, z = coordinates
        x_rotated = x * cos_roll - y * sin_roll
        y_rotated = x * sin_roll + y * cos_roll
        z_rotated = z
        y_rotated_final = y_rotated * cos_pitch - z_rotated * sin_pitch
        z_rotated_final = y_rotated * sin_pitch + z_rotated * cos_pitch
        x_final = x_rotated * cos_yaw + z_rotated_final * sin_yaw
        z_final = -x_rotated * sin_yaw + z_rotated_final * cos_yaw
        return x_final, y_rotated_final, z_final

    @lru_cache(maxsize=RENDER_CACHE)
    def vertex(pitch: float, yaw: float, roll: float, vertex: tuple[float, float, float], size: float) -> Vector3D:
        cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll = RenderObject.calculateRotationAngles(pitch, yaw, roll)
        scaled_vector = RenderObject.scaleVertex(vertex, max(size, float()))
        rotated_vector = RenderObject.rotateVertex(scaled_vector, cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll)
        return rotated_vector

    @lru_cache(maxsize=RENDER_CACHE)
    def screenVertex(screenWidth: float, screenHeight: float, angle: float, pitch: float, yaw: float, roll: float, vertex: tuple[float, float, float]) -> tuple[float, float, float]:
        screen_center_x: int = screenWidth // 2
        screen_center_y: int = screenHeight // 2
        aspect_ratio: float = angle * (screenWidth / screenHeight)
        vector: Vector3D = Vector3D(*RenderObject.vertex(pitch, yaw, roll, vertex, angle))
        return screen_center_x + (vector.x / vector.z) * aspect_ratio * screen_center_x, screen_center_y - (vector.y / vector.z) * aspect_ratio * screen_center_y, vector.z

    def vectors(self) -> Iterable[Iterable[Vector3D]]:
        for edge in self.edges:
            yield map(lambda vertexIndex: Vector3D(*RenderObject.vertex(self.pitch, self.yaw, self.roll, self.vertices[vertexIndex], self.size)), edge)
