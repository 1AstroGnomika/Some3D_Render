from pygame import Surface
from dataclasses import dataclass

@dataclass
class Mesh:

    vertices:list[tuple[float, float, float]]
    normals:list[tuple[float, float, float]]
    texcoords:list[tuple[float, float]]
    faces:list[tuple[tuple[int, int, int]]]
    texture:Surface