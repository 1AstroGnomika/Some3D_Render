import pygame, math
from Constants import Colors
from Render.RenderObject import RenderObject
from Render.AbstractRender import AbstractRender
from Utils.Vector3D import Vector3D

class SoftwareRender(AbstractRender):
    
    def __init__(self, *args, **kwargs) -> None:
        self.initParameters(*args, **kwargs)

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.width, self.height))
        
    def displayPosition(self, vertex: Vector3D) -> tuple[float, float]:
        position: Vector3D = vertex - self.camera.position
        cos_x:float = math.cos(self.camera.viewRotation.x)
        sin_x:float = math.sin(self.camera.viewRotation.x)
        cos_y:float = math.cos(self.camera.viewRotation.y)
        sin_y:float = math.sin(self.camera.viewRotation.y)
        aspect_ratio:float = (self.width / self.height) * self.camera.viewRotation.z
        rotated_x:float = cos_x * position.x + sin_x * position.z
        rotated_z:float = -sin_x * position.x + cos_x * position.z
        position.x = rotated_x
        position.z = rotated_z
        rotated_y:float = cos_y * position.y - sin_y * position.z
        rotated_z = sin_y * position.y + cos_y * position.z
        position.y = rotated_y
        position.z = rotated_z
        screen_x:int = int((self.width // 2) + (position.x / position.z) * (self.width // 2))
        screen_y:int = int((self.height // 2) - (position.y / position.z) * aspect_ratio * (self.height // 2))
        return screen_x, screen_y
        
    def draw(self, renderObject:RenderObject) -> None:
        for vectors in renderObject.renderVectors():
            pygame.draw.line(self.display, Colors.WHITE, *tuple(map(lambda vector: self.displayPosition(vector + renderObject.point), vectors)), 1)
                
    def drawAll(self) -> None:
        for renderObjects in tuple(self.renderContainer.renderObjects.values()):
            for renderObject in iter(renderObjects):
                self.draw(renderObject)
    
    def render(self) -> None:
        self.display.fill(Colors.BLACK)
        self.drawAll()
        pygame.display.flip()