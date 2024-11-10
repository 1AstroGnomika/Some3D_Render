import math
from OpenGL.GL import *
from OpenGL.GLU import *
from Utils.Tools import StaticClass
from Utils.Vector3D import Vector3D
from Renders import RenderObject
from Renders.Camera import Camera
from Renders.RenderContainer import RenderContainer

class Render(StaticClass):

    camera:Camera = Camera(Vector3D())
    renderContainer:RenderContainer = RenderContainer()

    @staticmethod
    def setRenderProperties(angle:float, width:int, heigth:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        gluPerspective(angle, width / heigth, minRenderDistance, maxRenderDistance)

    @staticmethod
    def draw(renderObject: RenderObject) -> None:
        for vector in renderObject.renderVectors():
            glVertex3fv(vector.coordinates())

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