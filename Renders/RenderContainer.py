from Renders.RenderObject import RenderObject

class RenderContainer:

    __renderObjects:dict[str, set[RenderObject]]

    def __init__(self) -> None:
        self.__renderObjects = dict()

    @property
    def renderObjects(self) -> dict[str, set[RenderObject]]:
        return self.__renderObjects

    @staticmethod
    def getContainerName(renderObject:RenderObject) -> str:
        return type(renderObject).__name__

    def addToRender(self, renderObject:RenderObject) -> None:
        renderContainer:set[renderObject] = self.renderObjects.get(name := RenderContainer.getContainerName(renderObject))
        if renderContainer is None:
            renderContainer = self.renderObjects.setdefault(name, set())
        renderContainer.add(renderObject)

    def removeFromRender(self, renderObject:RenderObject) -> None:
        if container := self.__renderObjects.get(RenderContainer.getContainerName(renderObject)):
            container.discard(renderObject)