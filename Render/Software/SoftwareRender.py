import pygame
from Constants import Colors
from Render.Software.SoftwareRenderObject import SoftwareRenderObject
from Render.Software.SoftwareCamera import SoftwareCamera
from Render.AbstractRender import AbstractRender
from Utils.Vectors.Vector3D import Vector3D

class SoftwareRender(AbstractRender):

    camera:SoftwareCamera

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.camera.width, self.camera.height))

    def draw(self, renderObject: SoftwareRenderObject) -> None:
        vertices:tuple[Vector3D] = tuple(renderObject.point - Vector3D(*SoftwareRenderObject.calculateCoordinates(*renderObject.rotation.coordinates(), renderObject.size.coordinates(), vertex)) for vertex in renderObject.mesh.vertices)
        projected:tuple[Vector3D] = tuple(self.camera.surfaceProjection(vertex) for vertex in vertices)
        for face1, face2, face3 in renderObject.mesh.faces:
            i1, i2, i3 = face1[0], face2[0], face3[0]
            v0, v1, v2 = vertices[i1], vertices[i2], vertices[i3]
            if (v1 - v0).cross(v2 - v0).dot(self.camera.point - v0) < 0:
                pv0, pv1, pv2 = projected[i1], projected[i2], projected[i3]
                if pv0.z > 0 and pv1.z > 0 and pv2.z > 0:
                    pygame.draw.polygon(self.display, Colors.WHITE, (
                        (int(pv0.x), int(pv0.y)),
                        (int(pv1.x), int(pv1.y)),
                        (int(pv2.x), int(pv2.y))
                    ), 1)
                    
    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()