import pygame
from Constants import Colors
from Render.RenderObject import RenderObject
from Render.AbstractRender import AbstractRender
from Utils.Vector3D import Vector3D

class SoftwareRender(AbstractRender):

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.camera.width, self.camera.height))

    def draw(self, renderObject:RenderObject) -> None:
        vertices:tuple[tuple[float, float, float]] = RenderObject.calculateVertices(*renderObject.rotation.coordinates(), renderObject.size, renderObject.vertices)
        for edge in renderObject.edges:
            polygons:list[tuple[int, int]] = list()
            for index in edge:
                screenX, screenY, screenZ = RenderObject.calculateScreenProjection(self.camera.width, self.camera.height, self.camera.angle, self.camera.rotation.x, self.camera.rotation.y, self.camera.rotation.z, self.camera.viewVector(renderObject.point - Vector3D(*vertices[index])).coordinates())
                if screenZ > float():
                    if screenX >= float() and screenX <= self.camera.width and screenY >= float() and screenY <= self.camera.height:
                        polygons.append((round(screenX), round(screenY)))
                else:
                    break
            if len(polygons) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()