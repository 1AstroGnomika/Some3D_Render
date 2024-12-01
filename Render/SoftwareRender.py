import pygame
from Constants import Colors
from Render.RenderObject import RenderObject
from Render.AbstractRender import AbstractRender

class SoftwareRender(AbstractRender):

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.width, self.height))

    def draw(self, renderObject:RenderObject) -> None:
        for vectors in renderObject.vectors():
            if len(polygons := tuple(filter(any, map(lambda screen_position: tuple(map(round, screen_position)), map(lambda vertex: RenderObject.screenVertex(self.width, self.height, self.angle, self.camera.rotation.x, self.camera.rotation.y, self.camera.rotation.z, vertex.coordinates()), map(lambda vertex: self.viewVector(renderObject.point - vertex), vectors)))))) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()