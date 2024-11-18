
import pygame
from Handler.AbstarctHandler import AbstarctHandler

class InputHandler(AbstarctHandler):

    @AbstarctHandler.handlerEvents
    def handle() -> None:
        InputHandler.handleMouse(pygame.mouse.get_pos())
        InputHandler.handleButtons(pygame.key.get_pressed())

    @AbstarctHandler.handlerEvents
    def handleButtons(buttons:tuple[int]) -> None:
        for button, pressed in enumerate(buttons):
            if pressed:
                InputHandler.buttonPressed(button)

    @AbstarctHandler.handlerEvents
    def handleMouse(mousePosition:tuple[float]) -> None:
        InputHandler.mouseMove(mousePosition)

    @AbstarctHandler.handlerEvents
    def buttonPressed(button:int) -> None:
        ...

    @AbstarctHandler.handlerEvents
    def mouseMove(mousePosition:tuple[float]) -> None:
        ...