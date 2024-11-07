from Utils.Vector3D import Vector3D

class Camera(Vector3D):

    pitch:float  # Вертикальный угол (наклон)
    yaw:float  # Горизонтальный угол (поворот)

    def __init__(self, pitch:float, yaw:float, position:Vector3D):
        self.pitch = pitch
        self.yaw = yaw
        super().__init__(*position.coordinates())

    def nextCoordinates(self, speed:float) -> tuple[float]:
        ...