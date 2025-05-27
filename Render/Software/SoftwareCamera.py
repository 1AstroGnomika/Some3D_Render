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
    def calculateSurfaceProjection(screenWidth:float, screenHeight:float, angle:float, pitch:float, yaw:float, roll:float, vertex:tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = vertex
        cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll = SoftwareRenderObject.calculateAngles(pitch, yaw, roll)
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

    def viewVector(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.point
    
    def visible(self, renderObject:SoftwareRenderObject) -> bool:
        distance:float = self.point.distance(renderObject.point)
        if distance >= self.minRenderDistance and distance <= self.maxRenderDistance:
            width, height, depth = renderObject.dimensions()
            screenX, screenY, screenZ = SoftwareCamera.calculateSurfaceProjection(self.width, self.height, self.angle, self.rotation.x, self.rotation.y, self.rotation.z, self.viewVector(renderObject.point).coordinates())
            if screenZ > float():
                screenSizeX:float = ((self.width * width / screenZ) * self.angle) / 2
                screenSizeY:float = ((self.height * height / screenZ) * self.angle) / 2
                return screenX + screenSizeX >= float() and screenX - screenSizeX <= self.width and screenY + screenSizeY >= float() and screenY - screenSizeY <= self.height
            return screenZ >= -(depth / 2)
        return bool()
    
    def surfaceProjection(self, vertex:Vector3D) -> Vector3D:
        return Vector3D(*SoftwareCamera.calculateSurfaceProjection(self.width, self.height, self.angle, self.rotation.x, self.rotation.y, self.rotation.z, self.viewVector(vertex).coordinates()))