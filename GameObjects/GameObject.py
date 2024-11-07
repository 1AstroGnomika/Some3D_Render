from Utils.Vector3D import Vector3D

class GameObject:

    vertices:list[tuple[float]]
    edges:list[tuple[int]]
    point:Vector3D

    def __init__(self, vertices:list[tuple[float]], edges:list[tuple[int]], point:Vector3D) -> None:
        self.vertices = vertices
        self.edges = edges
        self.point = point