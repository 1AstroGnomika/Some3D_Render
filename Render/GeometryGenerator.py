import math

class GeometryGenerator:

    @staticmethod
    def sphere(radius: float, segments: int, rings: int):
        vertices = []
        triangles = []

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
                next = i * segments + (j + 1) % segments
                below = (i + 1) * segments + j
                below_next = (i + 1) * segments + (j + 1) % segments

                triangles.append((current, below, below_next))
                triangles.append((current, below_next, next))

        return tuple(vertices), tuple(triangles)