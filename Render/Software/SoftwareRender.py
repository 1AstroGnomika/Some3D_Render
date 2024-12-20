import pygame
from Constants import Colors
from Render.Software.SoftwareRenderObject import SoftwareRenderObject
from Render.Software.SoftwareCamera import SoftwareCamera
from Render.AbstractRender import AbstractRender
from Utils.Vector3D import Vector3D

class SoftwareRender(AbstractRender):

    camera:SoftwareCamera

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.camera.width, self.camera.height))

    def draw(self, renderObject:SoftwareRenderObject) -> None:
        vertices:tuple[tuple[float, float, float]] = SoftwareRenderObject.calculateVertices(*renderObject.rotation.coordinates(), renderObject.size, renderObject.vertices)
        for edge in renderObject.edges:
            polygons:list[tuple[int, int]] = list()
            for index in edge:
                surfaceVertex:Vector3D = self.camera.surfaceProjection(renderObject.point - Vector3D(*vertices[index]))
                if surfaceVertex.z > float():
                    polygons.append((int(surfaceVertex.x), int(surfaceVertex.y)))
                else:
                    break
            if len(polygons) > 1:
                pygame.draw.polygon(self.display, Colors.WHITE, polygons, int(renderObject.size))

    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()