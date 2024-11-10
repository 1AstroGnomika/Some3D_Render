from Utils.Vector3D import Vector3D

class Camera:

    position:Vector3D
    __lastCameraPosition:Vector3D

    def __init__(self, position:Vector3D) -> None:
        self.position = position
        self.__lastCameraPosition = Vector3D()

    def positionShift(self) -> Vector3D:
        result:Vector3D = self.position - self.__lastCameraPosition
        self.__lastCameraPosition = self.position.copy()
        return result