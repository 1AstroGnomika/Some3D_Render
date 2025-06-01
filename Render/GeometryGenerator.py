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

    @staticmethod
    def cube(size: float):
        s = size / 2
        vertices = [
            (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),  # back
            (-s, -s, s),  (s, -s, s),  (s, s, s),  (-s, s, s)   # front
        ]
        triangles = [
            (4, 5, 6), (4, 6, 7),
            (1, 0, 3), (1, 3, 2),
            (0, 4, 7), (0, 7, 3),
            (5, 1, 2), (5, 2, 6),
            (0, 1, 5), (0, 5, 4),
            (3, 7, 6), (3, 6, 2),
        ]
        return tuple(vertices), tuple(triangles)

    @staticmethod
    def plane(width: float, height: float, segments_x: int, segments_y: int):
        vertices = []
        triangles = []

        for i in range(segments_y + 1):
            for j in range(segments_x + 1):
                x = width * (j / segments_x - 0.5)
                y = height * (i / segments_y - 0.5)
                vertices.append((x, y, 0.0))

        for i in range(segments_y):
            for j in range(segments_x):
                top_left = i * (segments_x + 1) + j
                top_right = top_left + 1
                bottom_left = (i + 1) * (segments_x + 1) + j
                bottom_right = bottom_left + 1

                # Инвертирован порядок вершин — нормаль будет смотреть в +Z
                triangles.append((top_left, bottom_right, bottom_left))
                triangles.append((top_left, top_right, bottom_right))

        return tuple(vertices), tuple(triangles)


        return tuple(vertices), tuple(triangles)

    @staticmethod
    def cylinder(radius: float, height: float, segments: int):
        vertices = []
        triangles = []

        # Bottom and top center
        vertices.append((0, 0, -height / 2))  # bottom center
        vertices.append((0, 0, height / 2))   # top center

        # Side vertices
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            vertices.append((x, y, -height / 2))  # bottom
            vertices.append((x, y, height / 2))   # top

        for i in range(segments):
            i1 = 2 + i * 2
            i2 = 2 + ((i + 1) % segments) * 2

            # Bottom face
            triangles.append((0, i2, i1))

            # Top face
            triangles.append((1, i1 + 1, i2 + 1))

            # Side
            triangles.append((i1, i2, i2 + 1))
            triangles.append((i1, i2 + 1, i1 + 1))

        return tuple(vertices), tuple(triangles)
