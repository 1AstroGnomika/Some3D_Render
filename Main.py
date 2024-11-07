import pygame, time
from Renders.Render import Render
from GameObjects.GameObject import GameObject
from Utils.Vector3D import Vector3D

if __name__ == "__main__":

    pygame.init()

    ANGLE:float = 50.0
    WIDTH:int = 800
    HEIGTH:int = 600
    MINRENDERDISTANCE:float = 0.1
    MAXRENDERDISTANCE:float = 50.0

    Display:pygame.Surface = pygame.display.set_mode((WIDTH, HEIGTH), pygame.DOUBLEBUF | pygame.OPENGL)

    Render.setRenderProperties(ANGLE, WIDTH, HEIGTH, MINRENDERDISTANCE, MAXRENDERDISTANCE)
    
    Render.renderContainer.addToRender(GameObject(
        [
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1],
        ],
        [
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7],
        ],
        Vector3D(0, 0, 0))
    )

    while True:
        Render.render()
        pygame.display.flip()