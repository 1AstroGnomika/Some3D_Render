import pygame
from Handler.AbstarctHandler import AbstarctHandler

class EventHandler(AbstarctHandler):

    @AbstarctHandler.handlerEvents
    def handle() -> None:
        EventHandler.handleEvents(pygame.event.get())

    @AbstarctHandler.handlerEvents
    def handleEvents(events:list[pygame.event.Event]) -> None:
        for event in events:
            EventHandler.handleEvent(event)

    @AbstarctHandler.handlerEvents
    def handleEvent(events:pygame.event.Event) -> None:
        ...