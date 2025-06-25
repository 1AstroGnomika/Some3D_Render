from pygame import Surface, image
from Render.Hardware.Buffers.AbstractGLResourcePool import AbstractGLInputData, AbstractGLResourceData, AbstractGLResourcePool
from OpenGL.GL import (
    glGenTextures, glBindTexture, glTexParameteri, glTexImage2D, glDeleteTextures,
    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER,
    GL_LINEAR, GL_RGBA, GL_UNSIGNED_BYTE
)

class TextureGLInputData(AbstractGLInputData):

    width:int
    height:int
    texture:bytes

    def __init__(self, texture:Surface):
        self.width = texture.get_width()
        self.height = texture.get_height()
        self.texture = image.tobytes(texture, "RGBA")

    def __hash__(self) -> int:
        return hash((
            self.width,
            self.height,
            self.texture
        ))

class TextureGLResourceData(AbstractGLResourceData):

    texture:int

    def __init__(self, texture:int) -> None:
        self.texture = texture

class TextureGLResourcePool(AbstractGLResourcePool):

    def createGLResource(self, textureInput:TextureGLInputData) -> TextureGLResourceData:
        textureData:TextureGLResourceData = TextureGLResourceData(glGenTextures(1))
        glBindTexture(GL_TEXTURE_2D, textureData.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, textureInput.width, textureInput.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureInput.texture)
        return textureData

    def deleteGLResource(self, glTextureData:TextureGLResourceData) -> None:
        glDeleteTextures([glTextureData.texture])