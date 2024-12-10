from Utils.Vector3D import Vector3D
from Render.Transform import Transform

class Camera(Transform):
    
    def viewVector(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.point