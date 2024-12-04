import pygame
from Constants import Colors
from Render.RenderObject import RenderObject
from Render.AbstractRender import AbstractRender

class SoftwareRender(AbstractRender):

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.width, self.height))

    def draw(self, renderObject:RenderObject) -> None:
        for vectorVertices in renderObject.vectorVertices():
            polygons:list[tuple[int, int]] = list()
            for screenVertex in map(lambda vertex: RenderObject.screenVertex(self.width, self.height, self.angle, self.camera.rotation.x, self.camera.rotation.y, self.camera.rotation.z, vertex.coordinates()), map(lambda vertex: self.viewVector(renderObject.point - vertex), vectorVertices)):
                if self.onScreen(screenVertex):
                    polygons.append(tuple(map(round, screenVertex)))
                else:
                    break
            if len(polygons) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()