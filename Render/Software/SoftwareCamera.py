from math import tan, radians
from Utils.Vectors.Vector3D import Vector3D
from Render.AbstractCamera import AbstractCamera
from Render.Software.SoftwareRenderObject import SoftwareRenderObject

class SoftwareCamera(AbstractCamera):

    def __call__(self, renderObject:SoftwareRenderObject) -> SoftwareRenderObject:
        if self.visible(renderObject):
            return renderObject
        return None

    def calculateSurfaceProjection(renderWidth:float, renderHeight:float, fov:float, pitch:float, yaw:float, roll:float, vertex:tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = vertex
        cos_pitch, sin_pitch, cos_yaw, sin_yaw, cos_roll, sin_roll = SoftwareRenderObject.calculateAngles(pitch, yaw, roll)
        x, z = cos_pitch * x + sin_pitch * z, -sin_pitch * x + cos_pitch * z
        y, z = cos_yaw * y - sin_yaw * z, sin_yaw * y + cos_yaw * z
        x, y = cos_roll * x - sin_roll * y, sin_roll * x + cos_roll * y
        aspect_ratio = renderWidth / renderHeight
        fov_rad = radians(fov)
        f = 1 / tan(fov_rad / 2)
        correct_z = z or 0.01
        screen_x = (x * f / correct_z)
        screen_y = (y * f / correct_z) * aspect_ratio
        pixel_x = (screen_x + 1) * renderWidth / 2
        pixel_y = (1 - screen_y) * renderHeight / 2
        return pixel_x, pixel_y, z

    def direction(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.point
    
    def visible(self, renderObject:SoftwareRenderObject) -> bool:
        distance:float = self.point.distance(renderObject.point)
        return distance >= self.minRenderDistance and distance <= self.maxRenderDistance
    
    def surfaceProjection(self, vertex:Vector3D) -> Vector3D:
        return Vector3D(*SoftwareCamera.calculateSurfaceProjection(self.width, self.height, self.fow, self.rotation.x, self.rotation.y, self.rotation.z, self.direction(vertex).coordinates()))