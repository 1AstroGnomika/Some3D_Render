from OpenGL.GL import *
from OpenGL.GLU import *
from Utils.Tools import StaticClass
from GameObjects.GameObject import GameObject
from Renders.Camera import Camera
from Utils.Vector3D import Vector3D
from Renders.RenderContainer import RenderContainer

class Render(StaticClass):

    camera:Camera = Camera(float(), float(), Vector3D(float(), float(), -5.0))
    renderContainer:RenderContainer = RenderContainer()

    @staticmethod
    def setRenderProperties(angle:float, width:int, heigth:int, minRenderDistance:float, maxRenderDistance:float) -> None:
        gluPerspective(angle, width / heigth, minRenderDistance, maxRenderDistance)

    @staticmethod
    def draw(gameObject:GameObject) -> None:
        glBegin(GL_LINES)
        for edges in gameObject.edges:
            for vertex in edges:
                glVertex3fv(gameObject.vertices[vertex])
        glEnd()

    @staticmethod
    def drawAll() -> None:
        for renderObjects in tuple(Render.renderContainer.renderObjects.values()):
            for renderObject in iter(renderObjects):
                Render.draw(renderObject)

    @staticmethod
    def render() -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glTranslatef(*Render.camera.coordinates())
        glPushMatrix()
        glRotatef(0, 1, 0, 0)
        glRotatef(0, 0, 1, 0)
        Render.drawAll()
        glPopMatrix()