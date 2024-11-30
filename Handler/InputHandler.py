
import pygame
from Handler.EventHandler import EventHandler
from Utils.Tools import Events

class InputHandler(EventHandler):

    @EventHandler.handlerEvents
    def handle() -> None:
        InputHandler.handleMouse(pygame.mouse.get_pos())
        InputHandler.handleButtons(pygame.key.get_pressed())

    @EventHandler.handlerEvents
    def handleButtons(buttons:tuple[int]) -> None:
        for button, pressed in enumerate(buttons):
            if pressed:
                InputHandler.buttonPressed(button)

    @EventHandler.handlerEvents
    def handleMouse(mousePosition:tuple[float, float]) -> None:
        InputHandler.mouseMove(mousePosition)

    @EventHandler.handlerEvents
    def buttonPressed(button:int) -> None:
        ...

    @EventHandler.handlerEvents
    def mouseMove(mousePosition:tuple[float, float]) -> None:
        ...

    @EventHandler.handlerEvents
    def mouseShift(mouseShift:tuple[float, float]) -> None:
        ...

    @EventHandler.handlerEvents
    def mouseButtonDown(button:int) -> None:
        ...

    @EventHandler.handlerEvents
    def mouseButtonUp(button:int) -> None:
        ...

    @EventHandler.handlerEvents.handleEvent
    def post_handleEvent(event:Events.Event) -> None:
        pygameEvent:pygame.event.Event = event.args[0]
        if pygameEvent.type == pygame.MOUSEMOTION:
            InputHandler.mouseShift(pygameEvent.rel)
        elif pygameEvent.type == pygame.MOUSEBUTTONDOWN:
            InputHandler.mouseButtonDown(pygameEvent.button)
        elif pygameEvent.type == pygame.MOUSEBUTTONUP:
            InputHandler.mouseButtonUp(pygameEvent.button)