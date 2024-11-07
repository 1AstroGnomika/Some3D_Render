from Utils.Vector3D import Vector3D

class GameObject:

    vertices:list[tuple[float]]
    edges:list[tuple[int]]
    point:Vector3D
    pitch:float  # Вертикальный угол (наклон)
    yaw:float  # Горизонтальный угол (поворот)

    def __init__(self, vertices:list[tuple[float]], edges:list[tuple[int]], point:Vector3D, pitch:float, yaw:float) -> None:
        self.vertices = vertices
        self.edges = edges
        self.point = point
        self.pitch = pitch
        self.yaw = yaw