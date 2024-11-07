from Handlers.Handler import Handler

class InputHandler(Handler):

    @Handler.handlerEvents
    @staticmethod
    def handle(mousePosition:tuple[float], buttons:tuple[int]) -> None:
        InputHandler.handleMouse(mousePosition)
        InputHandler.handleButtons(buttons)

    @Handler.handlerEvents
    @staticmethod
    def handleButtons(buttons:tuple[int]) -> None:
        for button, pressed in enumerate(filter(bool, buttons)):
            InputHandler.buttonPressed(button)

    @Handler.handlerEvents
    @staticmethod
    def handleMouse(mousePosition:tuple[float]) -> None:
        InputHandler.mouseMove(mousePosition)

    @Handler.handlerEvents
    @staticmethod
    def buttonPressed(button:int) -> None:
        ...

    @Handler.handlerEvents
    @staticmethod
    def mouseMove(mousePosition:tuple[float]) -> None:
        ...