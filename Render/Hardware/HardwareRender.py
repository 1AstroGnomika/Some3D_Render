import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from Render.AbstractRender import AbstractRender
from Render.Hardware.HardwareCamera import HardwareCamera
from Render.Hardware.HardwareRenderObject import HardwareRenderObject

class HardwareRender(AbstractRender):

    camera: HardwareCamera

    def initRender(self) -> None:
        self.display = pygame.display.set_mode((self.camera.width, self.camera.height), pygame.OPENGL | pygame.DOUBLEBUF)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glShadeModel(GL_SMOOTH)

    def draw(self, renderObject: HardwareRenderObject) -> None:
        glUseProgram(renderObject.shader.program)
        model_loc:int = glGetUniformLocation(renderObject.shader.program, "model")
        if model_loc != -1:
            model = glm.mat4(1)
            model = glm.translate(model, glm.vec3(renderObject.point.reverse().coordinates()))
            model = glm.rotate(model, glm.radians(renderObject.rotation.z), glm.vec3(0.0, 0.0, 1.0))
            model = glm.rotate(model, glm.radians(renderObject.rotation.x), glm.vec3(0.0, 1.0, 0.0)) # idk wtf but its work so
            model = glm.rotate(model, glm.radians(renderObject.rotation.y), glm.vec3(1.0, 0.0, 0.0)) # idk wtf but its work so
            model = glm.scale(model, glm.vec3(renderObject.size))
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        view_loc:int = glGetUniformLocation(renderObject.shader.program, "view")
        if view_loc != -1:
            view = glm.lookAt(
                self.camera.point.reverse().coordinates(),
                (self.camera.point + self.camera.forward()).reverse().coordinates(),
                self.camera.up().reverse().coordinates()
            )
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        projection_loc:int = glGetUniformLocation(renderObject.shader.program, "projection")
        if projection_loc != -1:
            projection = glm.perspective(glm.radians(self.camera.fow), self.camera.width / self.camera.height, self.camera.minRenderDistance, self.camera.maxRenderDistance)
            glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glBindVertexArray(renderObject.VAOIndex)
        glDrawArrays(GL_LINES, 0, len(renderObject.vertices) // 3)

    def render(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawAll()
        pygame.display.flip()
