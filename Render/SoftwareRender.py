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
                surfaceVector:Vector3D = self.camera.surfaceProjection(renderObject.point - Vector3D(*vertices[index]))
                if surfaceVector.z > float():
                    if surfaceVector.x >= float() and surfaceVector.x <= self.camera.width and surfaceVector.y >= float() and surfaceVector.y <= self.camera.height:
                        polygons.append((round(surfaceVector.x), round(surfaceVector.y)))
                else:
                    break
            if len(polygons) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()