from math import tan, radians
from functools import lru_cache
from Utils.Vector3D import Vector3D
from Render.AbstractCamera import AbstractCamera
from Render.Software.SoftwareRenderObject import SoftwareRenderObject

class SoftwareCamera(AbstractCamera):

    CAMERA_CACHE:int = 128

    def __call__(self, renderObject:SoftwareRenderObject) -> SoftwareRenderObject:
        if self.visible(renderObject):
            return renderObject
        return None

    @lru_cache(maxsize=CAMERA_CACHE)
    def calculateSurfaceProjection(renderWidth:float, renderHeight:float, fov:float, pitch:float, yaw:float, roll:float, vertex:tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = vertex
        cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll = SoftwareRenderObject.calculateAngles(pitch, yaw, roll)
        x, z = cos_pitch * x + sin_pitch * z, -sin_pitch * x + cos_pitch * z
        y, z = cos_yaw * y - sin_yaw * z, sin_yaw * y + cos_yaw * z
        x, y = cos_roll * x - sin_roll * y, sin_roll * x + cos_roll * y
        #aspect_ratio = renderWidth / renderHeight
        fov_rad = radians(fov)
        f = 1 / tan(fov_rad / 2)
        correct_z = z or 0.01
        screen_x = (x * f / correct_z)# * aspect_ratio
        screen_y = (y * f / correct_z)# * aspect_ratio
        pixel_x = (screen_x + 1) * renderWidth / 2
        pixel_y = (1 - screen_y) * renderHeight / 2
        return pixel_x, pixel_y, z
    
    @lru_cache(maxsize=CAMERA_CACHE)
    def calculateSurfaceRect(renderWidth:float, renderHeight:float, width:float, height:float, depth:float, screenX:float, screenY:float, screenZ:float) -> tuple[int, int, int, int]:
        screenSizeX = (renderWidth / 2.8) * (width / screenZ)
        screenSizeY = (renderHeight / 2.8) * (height / screenZ)
        return (
            int(screenX - screenSizeX),
            int(screenY - screenSizeY),
            int(screenSizeX * 2),
            int(screenSizeY * 2)
        )

    def viewVector(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.point
    
    def visible(self, renderObject:SoftwareRenderObject) -> bool:
        distance:float = self.point.distance(renderObject.point)
        if distance >= self.minRenderDistance and distance <= self.maxRenderDistance:
            width, height, depth = renderObject.dimensions()
            screenX, screenY, screenZ = SoftwareCamera.calculateSurfaceProjection(self.width, self.height, self.fow, self.rotation.x, self.rotation.y, self.rotation.z, self.viewVector(renderObject.point).coordinates())
            if screenZ > float():
                rectX, rectY, rectWidth, rectHeight = SoftwareCamera.calculateSurfaceRect(self.width, self.height, width, height, depth, screenX, screenY, screenZ)
                return (rectX + rectWidth > 0 and rectY + rectHeight > 0 and rectX < self.width and rectY < self.height)
            return screenZ >= -(depth / 2)
        return bool()
    
    def surfaceRect(self, renderObject:SoftwareRenderObject) -> tuple[int, int, int, int]:
        return SoftwareCamera.calculateSurfaceRect(self.width, self.height, *renderObject.dimensions(), *self.surfaceProjection(renderObject.point).coordinates())
    
    def surfaceProjection(self, vertex:Vector3D) -> Vector3D:
        return Vector3D(*SoftwareCamera.calculateSurfaceProjection(self.width, self.height, self.fow, self.rotation.x, self.rotation.y, self.rotation.z, self.viewVector(vertex).coordinates()))