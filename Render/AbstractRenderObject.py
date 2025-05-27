from abc import abstractmethod
from Render.AbstacrtTransform import AbstacrtTransform
from Utils.Vector3D import Vector3D

class AbstractRenderObject(AbstacrtTransform):

    vertices:tuple[tuple[float, float, float]]
    triangles:tuple[tuple[int, int, int]]
    size:float

    def __init__(self, vertices:tuple[tuple[float, float, float]], triangles:tuple[tuple[int, int, int]], size:float, point:Vector3D, rotation:Vector3D) -> None:
        self.vertices = vertices
        self.triangles = triangles
        self.size = size
        super().__init__(point, rotation)