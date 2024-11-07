from GameObjects.GameObject import GameObject

class RenderContainer:

    __renderObjects:dict[str, set[GameObject]]

    def __init__(self) -> None:
        self.__renderObjects = dict()

    @property
    def renderObjects(self) -> dict[str, set[GameObject]]:
        return self.__renderObjects

    @staticmethod
    def getContainerName(gameObject:GameObject) -> str:
        return type(gameObject).__name__

    def addToRender(self, gameObject:GameObject) -> None:
        renderContainer:set[GameObject] = self.renderObjects.get(name := RenderContainer.getContainerName(gameObject))
        if renderContainer is None:
            renderContainer = self.renderObjects.setdefault(name, set())
        renderContainer.add(gameObject)

    def removeFromRender(self, gameObject:GameObject) -> None:
        if container := self.__renderObjects.get(RenderContainer.getContainerName(gameObject)):
            container.discard(gameObject)