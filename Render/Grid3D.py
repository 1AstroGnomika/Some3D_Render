import math
from typing import Any, Iterable
from Utils.Vector3D import Vector3D

class Grid3D:

    width:int
    height:int
    depth:int
    __childs:dict[tuple[int, int, int], list[Any]]

    def __init__(self, width:int, height:int, depth:int) -> None:
        self.width = width
        self.height = height
        self.depth = depth
        self.__childs = dict()

    def convert(self, point:Vector3D) -> Vector3D:
        return Vector3D(
            int(point.x / self.width),
            int(point.y / self.height),
            int(point.z / self.depth)
        )

    def add(self, child:Any, point:Vector3D) -> None:
        index:tuple[int, int, int] = self.convert(point).coordinates()
        childs:list[Any] = self.__childs.setdefault(index, [])
        childs.append(child)

    def remove(self, child:Any, point:Vector3D) -> None:
        index:tuple[int, int, int] = self.convert(point).coordinates()
        childs:list[Any] = self.__childs.get(index)
        if childs:
            childs.remove(child)
            if not childs:
                self.__childs.pop(index, None)

    def move(self, child:Any, old:Vector3D, new:Vector3D) -> None:
        self.remove(child, old)
        self.add(child, new)

    def direction(self, distance:int, forward:Vector3D, point:Vector3D) -> Iterable[list[Any]]:
        cell:Vector3D = self.convert(point)
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
            index = cell.coordinates()
            if index in self.__childs:
                yield self.__childs[index]
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
        raycast_filter:set[Any] = set()
        for ray_index in range(rays):
            ray:float = math.sqrt(ray_index / rays) * radius
            angle:float = ray_index * math.pi * (3 - math.sqrt(5))
            offset_x:float = math.cos(angle) * ray
            offset_y:float = math.sin(angle) * ray
            for childs in self.direction(distance, Vector3D(
                forward.x + offset_x * right.x + offset_y * up.x,
                forward.y + offset_x * right.y + offset_y * up.y,
                forward.z + offset_x * right.z + offset_y * up.z,
            ).normalize(), point):
                for child in childs:
                    if not child in raycast_filter:
                        yield child
                    else: break
                    raycast_filter.add(child)
                break