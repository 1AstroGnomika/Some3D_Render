from Utils.Vector3D import Vector3D
from Render.Transform import Transform
from Render.RenderObject import RenderObject

class Camera(Transform):
    
    angle:float
    width:int
    height:int
    minRenderDistance:float
    maxRenderDistance:float

    def __init__(self, angle:float, width:int, height:int, minRenderDistance:float, maxRenderDistance:float, point:Vector3D=None, rotation:Vector3D=None) -> None:
        self.angle = angle
        self.width = width
        self.height = height
        self.minRenderDistance = minRenderDistance
        self.maxRenderDistance = maxRenderDistance
        super().__init__(point or Vector3D(), rotation or Vector3D())

    def viewVector(self, vertex:Vector3D) -> Vector3D:
        return vertex - self.point
    
    def visible(self, renderObject:RenderObject) -> bool:
        distance:float = self.point.distance(renderObject.point)
        if distance >= self.minRenderDistance and distance <= self.maxRenderDistance:
            width, height, depth = renderObject.dimensions
            screenX, screenY, screenZ = RenderObject.calculateScreenProjection(self.width, self.height, self.angle, self.rotation.x, self.rotation.y, self.rotation.z, self.viewVector(renderObject.point).coordinates())
            if screenZ > float():
                screenSizeX:float = ((self.width * width / screenZ) * self.angle) / 2
                screenSizeY:float = ((self.height * height / screenZ) * self.angle) / 2
                return screenX + screenSizeX >= float() and screenX - screenSizeX <= self.width and screenY + screenSizeY >= float() and screenY - screenSizeY <= self.height
            return screenZ >= -(depth / 2)
        return bool()