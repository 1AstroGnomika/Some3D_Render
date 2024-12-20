from abc import abstractmethod
from Render.AbstacrtTransform import AbstacrtTransform
from Utils.Vector3D import Vector3D

class AbstractRenderObject(AbstacrtTransform):

    vertices:tuple[tuple[float, float, float]]
    edges:tuple[tuple[int]]
    size:float

    def __init__(self, vertices:tuple[tuple[float, float, float]], edges:tuple[tuple[int]], size:float, point:Vector3D, rotation:Vector3D) -> None:
        self.vertices = vertices
        self.edges = edges
        self.size = size
        super().__init__(point, rotation)