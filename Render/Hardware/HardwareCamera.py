from Render.AbstractCamera import AbstractCamera
from Render.Hardware.HardwareRenderObject import HardwareRenderObject

class HardwareCamera(AbstractCamera):
    
    def __call__(self, renderObject: HardwareRenderObject) -> HardwareRenderObject:
        return renderObject