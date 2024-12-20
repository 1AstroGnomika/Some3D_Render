import pygame
from Render.AbstractRender import AbstractRender
from Render.Hardware.HardwareCamera import HardwareCamera
from Render.Hardware.HardwareRenderObject import HardwareRenderObject

class HardwareRender(AbstractRender):
    
    camera:HardwareCamera

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.camera.width, self.camera.height), pygame.OPENGL | pygame.DOUBLEBUF)

    def draw(self, renderObject:HardwareRenderObject) -> None:
        ...

    def render(self) -> None:
        pygame.display.flip()