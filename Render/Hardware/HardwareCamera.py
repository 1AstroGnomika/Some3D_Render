from Utils.Vector3D import Vector3D
from Render.AbstractCamera import AbstractCamera
from Render.Hardware.HardwareRenderObject import HardwareRenderObject

class HardwareCamera(AbstractCamera):
    
    def __call__(self, renderObject: HardwareRenderObject) -> HardwareRenderObject:
        return None
    
    def direction(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.point