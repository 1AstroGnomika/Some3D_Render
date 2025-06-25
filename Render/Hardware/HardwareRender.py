import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from Render.AbstractRender import AbstractRender
from Render.Hardware.HardwareCamera import HardwareCamera
from Render.Hardware.HardwareRenderObject import HardwareRenderObject
from Render.Hardware.Shaders.ShaderController import ShaderController

class HardwareRender(AbstractRender):

    BASE_RENDER_PARAMETER_MODEL:str = "model"
    BASE_RENDER_PARAMETER_VIEW:str = "view"
    BASE_RENDER_PARAMETER_PROJECTION:str = "projection"
    BASE_RENDER_PARAMETER_TEXTURE:str = "texture0"

    camera: HardwareCamera

    def initRender(self) -> None:
        pygame.display.set_mode((self.camera.width, self.camera.height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glDepthFunc(GL_LESS)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        glShadeModel(GL_SMOOTH)
        

    def draw(self, renderObject:HardwareRenderObject) -> None:
        glUseProgram(renderObject.shader.program)
        if ShaderController.hasUniform(renderObject.shader, HardwareRender.BASE_RENDER_PARAMETER_MODEL):
            model = glm.mat4(1)
            model = glm.translate(model, glm.vec3(renderObject.point.reverse().coordinates()))
            model = glm.rotate(model, glm.radians(renderObject.rotation.z), glm.vec3(0.0, 0.0, 1.0))
            model = glm.rotate(model, glm.radians(renderObject.rotation.x), glm.vec3(0.0, 1.0, 0.0)) # idk wtf but its work so
            model = glm.rotate(model, glm.radians(renderObject.rotation.y), glm.vec3(1.0, 0.0, 0.0)) # idk wtf but its work so
            model = glm.scale(model, glm.vec3(renderObject.size.coordinates()))
            ShaderController.setUniform(renderObject.shader, HardwareRender.BASE_RENDER_PARAMETER_MODEL, model.to_tuple())
        if ShaderController.hasUniform(renderObject.shader, HardwareRender.BASE_RENDER_PARAMETER_VIEW):
           ShaderController.setUniform(renderObject.shader, HardwareRender.BASE_RENDER_PARAMETER_VIEW, glm.lookAt(
                self.camera.point.reverse().coordinates(),
                (self.camera.point + self.camera.forward()).reverse().coordinates(),
                self.camera.up().reverse().coordinates()
            ).to_tuple())
        if ShaderController.hasUniform(renderObject.shader, HardwareRender.BASE_RENDER_PARAMETER_PROJECTION):
            ShaderController.setUniform(renderObject.shader, HardwareRender.BASE_RENDER_PARAMETER_PROJECTION, glm.perspective(
                glm.radians(self.camera.fow),
                self.camera.width / self.camera.height,
                self.camera.minRenderDistance,
                self.camera.maxRenderDistance
            ).to_tuple())
        if renderObject.texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, renderObject.texture.texture)
        glBindVertexArray(renderObject.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, renderObject.mesh.polygons)

    def render(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.drawAll()
        pygame.display.flip()
