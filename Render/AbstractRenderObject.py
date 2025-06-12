from abc import abstractmethod
from Render.AbstractTransform import AbstractTransform
from Utils.Vector3D import Vector3D

class AbstractRenderObject(AbstractTransform):

    size:float

    def __init__(self, vertices:tuple[tuple[float, float, float]], triangles:tuple[tuple[int, int, int]], size:float, point:Vector3D, rotation:Vector3D) -> None:
        self.size = size
        self.initVertices(vertices, triangles)
        super().__init__(point, rotation)

        @abstractmethod
        def initVertices(self, vertices:tuple[tuple[float, float, float]], triangles:tuple[tuple[int, int, int]]) -> None: ...