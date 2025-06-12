import math
from typing import Any, Iterable
from Utils.Vector3D import Vector3D

class Grid3D:

    DIRECTIONS:tuple[tuple[int, int, int]] = (
        (1, 0, 0), (-1, 0, 0),
        (0, 1, 0), (0, -1, 0),
        (0, 0, 1), (0, 0, -1)
    )

    width:int
    height:int
    depth:int

    __childs:dict[tuple[int, int, int], Any]

    def __init__(self, width:int, height:int, depth:int) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.__childs = dict()

    def get_by_index(self, index:tuple[float, float, float]) -> Any:
        return self.__childs.get(index)
    
    def add_by_index(self, child:Any, index:tuple[float, float, float]) -> None:
        self.__childs[index] = child

    def remove_by_index(self, index:tuple[float, float, float]) -> None:
        self.__childs.pop(index, None)

    def move_by_index(self, old:tuple[float, float, float], new:tuple[float, float, float]) -> None:
        if child := self.get_by_index(old):
            self.remove_by_index(old)
            self.add_by_index(child, new)

    def convert_index(self, index:tuple[float, float, float]) -> tuple[int, int, int]:
        return (
            int(index[0] / self.width),
            int(index[1] / self.height),
            int(index[2] / self.depth),
        )

    def convert_vector(self, point:Vector3D) -> Vector3D:
        return Vector3D(*self.convert_index(point.coordinates()))

    def get_by_vector(self, point:Vector3D) -> Iterable[Any]:
        return self.get_by_index(self.convert_index(point.coordinates()))

    def add_by_vector(self, child:Any, point:Vector3D) -> None:
        self.add_by_index(child, self.convert_index(point.coordinates()))

    def remove_by_vector(self, point:Vector3D) -> None:
        self.remove_by_index(self.convert_index(point.coordinates()))

    def move_by_vector(self, old:Vector3D, new:Vector3D) -> None:
        self.move_by_index(self.convert_index(old.coordinates()), self.convert_index(new.coordinates()))

    def rect(self, min_point: Vector3D, max_point: Vector3D) -> Iterable[Any]:
        min_cell:Vector3D = self.convert_vector(min_point)
        max_cell:Vector3D = self.convert_vector(max_point)
        for x in range(min_cell.x, max_cell.x + 1):
            for y in range(min_cell.y, max_cell.y + 1):
                for z in range(min_cell.z, max_cell.z + 1):
                    if child := self.get_by_index((x, y, z)):
                        return child

    def direction(self, distance:int, forward:Vector3D, point:Vector3D) -> Iterable[Any]:
        cell:Vector3D = self.convert_vector(point)
        dir:Vector3D = forward.normalize()
        step:Vector3D = Vector3D(
            1 if dir.x > 0 else -1 if dir.x < 0 else 0,
            1 if dir.y > 0 else -1 if dir.y < 0 else 0,
            1 if dir.z > 0 else -1 if dir.z < 0 else 0
        )
        t_max:Vector3D = Vector3D(
            ((cell.x + (step.x > 0)) * self.width - point.x) / dir.x if dir.x != 0 else float('inf'),
            ((cell.y + (step.y > 0)) * self.height - point.y) / dir.y if dir.y != 0 else float('inf'),
            ((cell.z + (step.z > 0)) * self.depth - point.z) / dir.z if dir.z != 0 else float('inf'),
        )
        t_delta:Vector3D = Vector3D(
            abs(self.width / dir.x) if dir.x != 0 else float('inf'),
            abs(self.height / dir.y) if dir.y != 0 else float('inf'),
            abs(self.depth / dir.z) if dir.z != 0 else float('inf'),
        )
        for _ in range(distance):
            if child := self.get_by_index(cell.coordinates()):
                yield child
            if t_max.x < t_max.y and t_max.x < t_max.z:
                cell.x += step.x
                t_max.x += t_delta.x
            elif t_max.y < t_max.z:
                cell.y += step.y
                t_max.y += t_delta.y
            else:
                cell.z += step.z
                t_max.z += t_delta.z

    def raycast(self, radius:float, rays:int, distance:int, forward:Vector3D, point:Vector3D) -> Iterable[Any]:
        forward:Vector3D = forward.normalize()
        world_up:Vector3D = Vector3D(z=1) if abs(forward.x) < 1e-6 and abs(forward.y) else Vector3D(y=1)
        right:Vector3D = forward.cross(world_up).normalize()
        up:Vector3D = right.cross(forward).normalize()
        targets:set[Any] = set()
        for ray_index in range(rays):
            ray:float = math.sqrt(ray_index / rays) * radius
            angle:float = ray_index * math.pi * (3 - math.sqrt(5))
            offset_x:float = math.cos(angle) * ray
            offset_y:float = math.sin(angle) * ray
            for child in self.direction(distance, Vector3D(
                forward.x + offset_x * right.x + offset_y * up.x,
                forward.y + offset_x * right.y + offset_y * up.y,
                forward.z + offset_x * right.z + offset_y * up.z,
            ).normalize(), point):
                child_id:int = id(child)
                if not child_id in targets:
                    yield child
                targets.add(child_id)
                break

    def exposed(self) -> Iterable[tuple[tuple[int, int, int], tuple[int, int, int], Any]]:
        for x, y, z in self.__childs.keys():
            for dx, dy, dz in Grid3D.DIRECTIONS:
                if not (x + dx, y + dy, z + dz) in self.__childs:
                    yield (
                        (dx, dy, dz),
                        (x, y, z),
                        self.__childs[(x, y, z)]
                    )