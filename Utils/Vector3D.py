import math

class Vector3D:

    x:float
    y:float
    z:float

    def __init__(self, x:float, y:float, z:float):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other:"Vector3D") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def dot(self, other:"Vector3D") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def angle(self, other:"Vector3D") -> float:
        if magnitudes := self.magnitude() * other.magnitude():
            return math.acos(self.dot(other) / magnitudes)
        return float()
    
    def coordinates(self) -> tuple[float]:
        return (
            self.x,
            self.y,
            self.z
        )
