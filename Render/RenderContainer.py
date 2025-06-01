from Render.Grid3D import Grid3D
from Render.AbstractRenderObject import AbstractRenderObject
from Render.AbstractCamera import AbstractCamera

class RenderContainer:

    CHUNK_WIDTH:int = 10
    CHUNK_HEIGHT:int = 10
    CHUNK_DEPTH:int = 10

    chunks:Grid3D

    def __init__(self) -> None:
        self.chunks = Grid3D(RenderContainer.CHUNK_WIDTH, RenderContainer.CHUNK_HEIGHT, RenderContainer.CHUNK_DEPTH)

    def getRenderObjects(self, camera:AbstractCamera) -> tuple[AbstractRenderObject]:
        return tuple(self.chunks.raycast(2, 250, 50, camera.forward(), camera.point))

    def addToRender(self, renderObject:AbstractRenderObject) -> None:
        self.chunks.add(renderObject, renderObject.point)

    def removeFromRender(self, renderObject:AbstractRenderObject) -> None:
        self.chunks.remove(renderObject, renderObject.point)