from abc import abstractmethod
from Meshes.Mesh import Mesh
from Render.AbstractTransform import AbstractTransform
from Utils.Vectors.Vector3D import Vector3D

class AbstractRenderObject(AbstractTransform):

    size:Vector3D

    def __init__(self, mesh:Mesh, size:Vector3D, point:Vector3D, rotation:Vector3D) -> None:
        self.size = size
        self.processMesh(mesh)
        super().__init__(point, rotation)

    @abstractmethod
    def processMesh(self, mesh:Mesh) -> None: ...