from Render.Hardware.Buffers.AbstractGLResourcePool import AbstractGLInputData, AbstractGLResourceData, AbstractGLResourcePool
from OpenGL.GL import (
    GL_FLOAT, GL_FALSE, GL_ARRAY_BUFFER, GL_STATIC_DRAW,
    glGenVertexArrays, glGenBuffers,
    glBindVertexArray, glBindBuffer,
    glBufferData, glVertexAttribPointer, glEnableVertexAttribArray,
    glDeleteBuffers, glDeleteVertexArrays
)
from ctypes import c_void_p

class MeshGLInputData(AbstractGLInputData):

    vertixes:bytes

    def __init__(self, vertixes:bytes):
        self.vertixes = vertixes

    def __hash__(self):
        return hash(self.vertixes)

class MeshGLResourceData(AbstractGLResourceData):
    
    vao:int
    vbo:int
    polygons:int

    def __init__(self, vao:int, vbo:int, polygons:int):
        self.vao = vao
        self.vbo = vbo
        self.polygons = polygons

class MeshGLResourcePool(AbstractGLResourcePool):

    def createGLResource(self, meshInput: MeshGLInputData) -> MeshGLResourceData:
        stride:int = 8 * 4
        meshData = MeshGLResourceData(glGenVertexArrays(1), glGenBuffers(1), (len(meshInput.vertixes) // 4) // 8 // 1)
        glBindVertexArray(meshData.vao)
        glBindBuffer(GL_ARRAY_BUFFER, meshData.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(meshInput.vertixes), meshInput.vertixes, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, c_void_p((3 + 2) * 4))
        glEnableVertexAttribArray(2)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
        return meshData

    def deleteGLResource(self, glResourceData:MeshGLResourceData) -> None:
        glDeleteBuffers(1, [glResourceData.vbo])
        glDeleteVertexArrays(1, [glResourceData.vao])