from OpenGL.GL import *
from OpenGL.GLU import *
from Utils.Tools import StaticClass
from Utils.Vector3D import Vector3D
from Renders.RenderObject import RenderObject
from Renders.Camera import Camera
from Renders.RenderContainer import RenderContainer

class Render(StaticClass):

    MIN_RENDER_DISTANCE:float
    MAX_RENDER_DISTANCE:float
    camera:Camera = Camera(Vector3D())
    renderContainer:RenderContainer = RenderContainer()

    @staticmethod
    def setRenderProperties(angle:float, width:int, heigth:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        Render.MIN_RENDER_DISTANCE = minRenderDistance
        Render.MAX_RENDER_DISTANCE = maxRenderDistance
        gluPerspective(angle, width / heigth, minRenderDistance, maxRenderDistance)

    @staticmethod
    def draw(renderObject: RenderObject) -> None:
        for vector in renderObject.renderVectors():
            if RenderObject.checkVectorDistance(Render.camera.position.coordinates(), vector.coordinates(), Render.MIN_RENDER_DISTANCE, Render.MAX_RENDER_DISTANCE):
                glVertex3fv((renderObject.point + vector).coordinates())

    @staticmethod
    def drawAll() -> None:
        for renderObjects in tuple(Render.renderContainer.renderObjects.values()):
            for renderObject in iter(renderObjects):
                Render.draw(renderObject)

    @staticmethod
    def render() -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(*Render.camera.positionShift().coordinates())
        glPushMatrix()
        glBegin(GL_LINES)
        Render.drawAll()
        glEnd()
        glPopMatrix()