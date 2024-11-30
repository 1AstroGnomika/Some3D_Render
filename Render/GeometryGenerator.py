import math

class GeometryGenerator:

    @staticmethod
    def sphere(radius: float, segments:int, rings:int):
        vertices = []
        edges = []
        for i in range(rings + 1):
            theta = math.pi * i / rings
            for j in range(segments):
                phi = 2 * math.pi * j / segments
                x = radius * math.sin(theta) * math.cos(phi)
                y = radius * math.sin(theta) * math.sin(phi)
                z = radius * math.cos(theta)
                vertices.append((x, y, z))
        for i in range(rings):
            for j in range(segments):
                current = i * segments + j
                next_horizontal = i * segments + (j + 1) % segments
                next_vertical = (i + 1) * segments + j
                edges.append((current, next_horizontal))
                if i < rings:
                    edges.append((current, next_vertical))
        return vertices, edges

    @staticmethod
    def cube(size: float):
        half = size / 2
        vertices = [
            (-half, -half, -half), (half, -half, -half), (half, half, -half), (-half, half, -half),
            (-half, -half, half), (half, -half, half), (half, half, half), (-half, half, half)
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]
        return vertices, edges
    
    @staticmethod
    def cubic_lattice(size: float, divisions: int):
        step = size / divisions
        vertices = []
        edges = []
        for i in range(divisions + 1):
            for j in range(divisions + 1):
                for k in range(divisions + 1):
                    x = i * step - size / 2
                    y = j * step - size / 2
                    z = k * step - size / 2
                    vertices.append((x, y, z))
        for i in range(divisions):
            for j in range(divisions):
                for k in range(divisions):
                    current = i * (divisions + 1) ** 2 + j * (divisions + 1) + k
                    if k < divisions: edges.append((current, current + 1))
                    if j < divisions: edges.append((current, current + (divisions + 1)))
                    if i < divisions: edges.append((current, current + (divisions + 1) ** 2))
        return vertices, edges

    @staticmethod
    def cylinder(radius: float, height: float, segments: int):
        vertices = []
        edges = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y, 0))
            vertices.append((x, y, height))
        for i in range(segments):
            edges.append((i * 2, ((i + 1) % segments) * 2))
            edges.append((i * 2 + 1, ((i + 1) % segments) * 2 + 1))
            edges.append((i * 2, i * 2 + 1))
        return vertices, edges

    @staticmethod
    def cone(radius: float, height: float, segments: int):
        vertices = [(0, 0, height)]
        edges = []
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y, 0))
        for i in range(segments):
            edges.append((0, i + 1))
        for i in range(segments):
            edges.append((i + 1, ((i + 1) % segments) + 1))
        return vertices, edges

    @staticmethod
    def torus(radius: float, tube_radius: float, segments: int, rings: int):
        vertices = []
        edges = []
        for i in range(rings):
            theta = 2 * math.pi * i / rings
            for j in range(segments):
                phi = 2 * math.pi * j / segments
                x = (radius + tube_radius * math.cos(phi)) * math.cos(theta)
                y = (radius + tube_radius * math.cos(phi)) * math.sin(theta)
                z = tube_radius * math.sin(phi)
                vertices.append((x, y, z))
        for i in range(rings):
            for j in range(segments):
                current = i * segments + j
                next_ring = ((i + 1) % rings) * segments + j
                next_segment = i * segments + (j + 1) % segments
                edges.append((current, next_ring))
                edges.append((current, next_segment))
        return vertices, edges