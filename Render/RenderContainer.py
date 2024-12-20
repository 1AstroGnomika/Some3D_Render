from Render.AbstractRenderObject import AbstractRenderObject

class RenderContainer:

    __renderObjects:dict[str, set[AbstractRenderObject]]

    def __init__(self) -> None:
        self.__renderObjects = dict()

    @property
    def renderObjects(self) -> dict[str, set[AbstractRenderObject]]:
        return self.__renderObjects

    @staticmethod
    def getContainerName(renderObject:AbstractRenderObject) -> str:
        return type(renderObject).__name__

    def addToRender(self, renderObject:AbstractRenderObject) -> None:
        renderContainer:set[renderObject] = self.renderObjects.get(name := RenderContainer.getContainerName(renderObject))
        if renderContainer is None:
            renderContainer = self.renderObjects.setdefault(name, set())
        renderContainer.add(renderObject)

    def removeFromRender(self, renderObject:AbstractRenderObject) -> None:
        if container := self.__renderObjects.get(RenderContainer.getContainerName(renderObject)):
            container.discard(renderObject)