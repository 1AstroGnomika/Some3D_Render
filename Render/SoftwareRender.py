import pygame
from Constants import Colors
from Render.RenderObject import RenderObject
from Render.AbstractRender import AbstractRender
from Utils.Vector3D import Vector3D

class SoftwareRender(AbstractRender):

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.width, self.heigth))

    def draw(self, renderObject:RenderObject) -> None:
        for vectors in renderObject.vectors():
            polygons:list[tuple[int, int]] = list()
            for x, y, z in map(lambda screen_position: screen_position, map(lambda vertex: RenderObject.screenVertex(self.width, self.heigth, self.angle, self.camera.rotation.y, self.camera.rotation.x, self.camera.rotation.z, vertex.coordinates()), map(lambda vertex: self.camera.position - (renderObject.point - vertex), vectors))):
                if z >= float():
                    polygons.append((round(x), round(y)))
            if len(polygons) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()