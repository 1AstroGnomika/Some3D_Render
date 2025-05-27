import math

class Vector3D:

    x:float
    y:float
    z:float

    def __init__(self, x:float = 0.0, y:float = 0.0, z:float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other:"Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other:"Vector3D") -> "Vector3D":
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other:"Vector3D") -> "Vector3D":
        return Vector3D(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def __truediv__(self, other:"Vector3D") -> "Vector3D":
        return Vector3D(self.x / other.x, self.y / other.y, self.z / other.z)
    
    def __eq__(self, other:"Vector3D") -> bool:
        if type(self) == type(other):
            return self.coordinates() == other.coordinates()
        return bool()
    
    def __repr__(self) -> str:
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"
    
    def copy(self) -> "Vector3D":
        return Vector3D(self.x, self.y, self.z)

    def distance(self, other:"Vector3D") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def dot(self, other:"Vector3D") -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normalize(self) -> "Vector3D":
        if magnitude := self.magnitude():
            return self / Vector3D(magnitude, magnitude, magnitude)
        return Vector3D()

    def angle(self, other:"Vector3D") -> float:
        if magnitudes := self.magnitude() * other.magnitude():
            return math.acos(self.dot(other) / magnitudes)
        return float()
    
    def cross(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    
    def coordinates(self) -> tuple[float]:
        return (self.x, self.y, self.z)