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
