import pygame
from Renders.Render import Render
from GameObjects.GameObject import GameObject
from Handlers.InputHandler import InputHandler
from Utils.Vector3D import Vector3D
from Utils.Tools import Events
from Keys import Buttons

if __name__ == "__main__":

    pygame.init()

    ANGLE:float = 50.0
    WIDTH:int = 800
    HEIGTH:int = 600
    MINRENDERDISTANCE:float = 0.1
    MAXRENDERDISTANCE:float = 50.0
    CAMERASPEED:float = 0.05

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
        Vector3D(z=-5.0),
        float(),
        float()
        )
    )

    @InputHandler.handlerEvents.buttonPressed
    def post_buttonPressed(event:Events.Event) -> None:
        button:int = event.args[0]
        match button:
            case Buttons.KEY_W:
                Render.camera.point.z += CAMERASPEED
            case Buttons.KEY_S:
                Render.camera.point.z -= CAMERASPEED
            case Buttons.KEY_A:
                Render.camera.point.x += CAMERASPEED
            case Buttons.KEY_D:
                Render.camera.point.x -= CAMERASPEED
            case Buttons.KEY_LSHIFT:
                Render.camera.point.y += CAMERASPEED
            case Buttons.KEY_SPACE:
                Render.camera.point.y -= CAMERASPEED
            case _:
                print(button)

    @InputHandler.handlerEvents.mouseMove
    def post_mouseMove(event:Events.Event) -> None:
        ...

    def mainLoop() -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            InputHandler.handle(pygame.mouse.get_pos(), tuple(pygame.key.get_pressed()))
            Render.render()
            pygame.display.flip()
    
    mainLoop()