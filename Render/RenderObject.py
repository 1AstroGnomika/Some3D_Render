from functools import lru_cache
from Utils.Vector3D import Vector3D
from Render.Transform import Transform

class RenderObject(Transform):

    vertices:tuple[tuple[float, float, float]]
    edges:tuple[tuple[int]]
    size:float

    def __init__(self, vertices:tuple[tuple[float, float, float]], edges:tuple[tuple[int]], size:float, point:Vector3D, rotation:Vector3D) -> None:
        self.vertices = vertices
        self.edges = edges
        self.size = size
        super().__init__(point, rotation)

    @property
    def dimensions(self) -> tuple[float, float, float]:
        return Transform.calculateDimensions(RenderObject.calculateVertices(*self.rotation.coordinates(), self.size, self.vertices))
    
    @lru_cache(maxsize=Transform.TRANSFORM_CACHE)
    def calculateVertices(pitch:float, yaw:float, roll:float, size:float, vertices:tuple[tuple[float, float, float]]) -> tuple[tuple[float, float, float]]:
        return tuple(map(lambda vertex: Transform.calculateCoordinates(pitch, yaw, roll, size, vertex), vertices))
    
    @lru_cache(maxsize=Transform.TRANSFORM_CACHE)
    def calculateScreenProjection(screenWidth:float, screenHeight:float, angle:float, pitch:float, yaw:float, roll:float, vertex:tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = vertex
        cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll = Transform.calculateAngles(pitch, yaw, roll)
        screen_center_x = screenWidth // 2
        screen_center_y = screenHeight // 2
        aspect_ratio = angle * (screen_center_x / screen_center_y)
        x, z = cos_pitch * x + sin_pitch * z, -sin_pitch * x + cos_pitch * z
        y, z = cos_yaw * y - sin_yaw * z, sin_yaw * y + cos_yaw * z
        x, y = cos_roll * x - sin_roll * y, sin_roll * x + cos_roll * y
        correct_z = z or 0.01
        screen_x = screen_center_x + (x / correct_z) * aspect_ratio * screen_center_x
        screen_y = screen_center_y - (y / correct_z) * aspect_ratio * screen_center_y
        return screen_x, screen_y, z
