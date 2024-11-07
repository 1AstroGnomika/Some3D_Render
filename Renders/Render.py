from OpenGL.GL import *
from OpenGL.GLU import *
from Utils.Tools import StaticClass
from Utils.Vector3D import Vector3D
from GameObjects.GameObject import GameObject
from Renders.Camera import Camera
from Renders.RenderContainer import RenderContainer

class Render(StaticClass):

    camera:Camera = Camera(None, list(), list(), Vector3D(), float(), float())
    renderContainer:RenderContainer = RenderContainer()

    @staticmethod
    def setRenderProperties(angle:float, width:int, heigth:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        gluPerspective(angle, width / heigth, minRenderDistance, maxRenderDistance)

    @staticmethod
    def draw(gameObject:GameObject) -> None:
        for edges in gameObject.edges:
            for vertex in edges:
                glVertex3fv((Vector3D(*gameObject.vertices[vertex]) + gameObject.point).coordinates())

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
        glRotatef(0, 1, 0, 0)
        glRotatef(0, 0, 1, 0)
        glBegin(GL_LINES)
        Render.drawAll()
        glEnd()
        glPopMatrix()