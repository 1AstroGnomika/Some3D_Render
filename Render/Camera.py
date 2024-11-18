from Utils.Vector3D import Vector3D

class Camera:

    viewRotation:Vector3D
    position:Vector3D
    __lastCameraPosition:Vector3D

    def __init__(self, viewRotation:Vector3D, position:Vector3D) -> None:
        self.viewRotation = viewRotation
        self.position = position
        self.__lastCameraPosition = Vector3D()

    def positionShift(self) -> Vector3D:
        result:Vector3D = self.__lastCameraPosition - self.position
        self.__lastCameraPosition = self.position.copy()
        return result