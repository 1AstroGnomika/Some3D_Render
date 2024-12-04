from functools import lru_cache
from typing import Iterable
from Utils.Vector3D import Vector3D
from Render.Transform import Transform

class RenderObject(Transform):

    vertices:list[tuple[float]]
    edges:list[tuple[int]]
    size:float

    def __init__(self, vertices:list[tuple[float]], edges:list[tuple[int]], size:float, point:Vector3D, rotation:Vector3D) -> None:
        self.vertices = vertices
        self.edges = edges
        self.size = size
        super().__init__(point, rotation)

    @lru_cache(maxsize=Transform.TRANSFORM_CACHE)
    def scaleVertex(vertices:tuple[float, float, float], size:float) -> tuple[float, float, float]:
        return tuple(map(lambda value: value * size, vertices))

    @lru_cache(maxsize=Transform.TRANSFORM_CACHE)
    def rotateVertex(coordinates:tuple[float, float, float], cos_pitch:float, sin_pitch:float, cos_yaw:float, sin_yaw:float, cos_roll:float, sin_roll:float) -> tuple[float, float, float]:
        x, y, z = coordinates
        x_rotated = x * cos_roll - y * sin_roll
        y_rotated = x * sin_roll + y * cos_roll
        z_rotated = z
        y_rotated_final = y_rotated * cos_pitch - z_rotated * sin_pitch
        z_rotated_final = y_rotated * sin_pitch + z_rotated * cos_pitch
        x_final = x_rotated * cos_yaw + z_rotated_final * sin_yaw
        z_final = -x_rotated * sin_yaw + z_rotated_final * cos_yaw
        return x_final, y_rotated_final, z_final

    @lru_cache(maxsize=Transform.TRANSFORM_CACHE)
    def vertex(pitch:float, yaw:float, roll:float, vertex:tuple[float, float, float], size:float) -> Vector3D:
        scaled_vector = RenderObject.scaleVertex(vertex, max(size, float()))
        rotated_vector = RenderObject.rotateVertex(scaled_vector, *Transform.calculateRotationAngles(pitch, yaw, roll))
        return rotated_vector
    
    @lru_cache(maxsize=Transform.TRANSFORM_CACHE)
    def screenVertex(screenWidth:float, screenHeight:float, angle:float, pitch:float, yaw:float, roll:float, vertex:tuple[float, float, float]) -> tuple[float, float]:
        x, y, z = vertex
        cos_yaw, sin_yaw, cos_pitch, sin_pitch, cos_roll, sin_roll = Transform.calculateAngles(pitch, yaw, roll)
        screen_center_x = screenWidth // 2
        screen_center_y = screenHeight // 2
        aspect_ratio = angle * (screen_center_x / screen_center_y)
        x, z = cos_yaw * x + sin_yaw * z, -sin_yaw * x + cos_yaw * z
        y, z = cos_pitch * y - sin_pitch * z, sin_pitch * y + cos_pitch * z
        x, y = cos_roll * x - sin_roll * y, sin_roll * x + cos_roll * y
        if z >= 0.01:
            screen_x = screen_center_x + (x / z) * aspect_ratio * screen_center_x
            screen_y = screen_center_y - (y / z) * aspect_ratio * screen_center_y
            return screen_x, screen_y
        return float("inf"), float("inf")

    def vectorVertices(self) -> Iterable[Iterable[Vector3D]]:
        for edge in self.edges:
            yield map(lambda vertexIndex: Vector3D(*RenderObject.vertex(*self.rotation.coordinates(), self.vertices[vertexIndex], self.size)), edge)
