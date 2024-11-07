from Utils.Vector3D import Vector3D
from GameObjects.GameObject import GameObject

class Camera(GameObject):

    central:GameObject
    __lastCameraPosition:Vector3D

    def __init__(self, gameObject:GameObject, *args, **kwargs):
        self.central = gameObject
        self.__lastCameraPosition = Vector3D()
        super().__init__(*args, **kwargs)

    def positionShift(self) -> Vector3D:
        result:Vector3D = self.point - self.__lastCameraPosition
        self.__lastCameraPosition = self.point.copy()
        return result