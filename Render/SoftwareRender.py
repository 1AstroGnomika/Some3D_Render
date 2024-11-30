import pygame
from Constants import Colors
from Render.RenderObject import RenderObject
from Render.AbstractRender import AbstractRender

class SoftwareRender(AbstractRender):

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.width, self.height))

    def draw(self, renderObject:RenderObject) -> None:
        for vectors in renderObject.vectors():
            polygons:list[tuple[int, int]] = list()
            for x, y in map(lambda screen_position: screen_position, map(lambda vertex: RenderObject.screenVertex(self.width, self.height, self.angle, self.camera.rotation.x, self.camera.rotation.y, self.camera.rotation.z, vertex.coordinates()), map(lambda vertex: self.camera.position - (renderObject.point - vertex), vectors))):
                if x or y:
                    polygons.append((round(x), round(y)))
            if len(polygons) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()