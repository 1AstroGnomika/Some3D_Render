from OpenGL.GL import GL_FLOAT, GL_FALSE, GL_ARRAY_BUFFER, GL_STATIC_DRAW, glGenVertexArrays, glGenBuffers, glBindVertexArray, glBindBuffer, glBufferData, glVertexAttribPointer, glEnableVertexAttribArray
from numpy import array, float32
from Render.AbstractRenderObject import AbstractRenderObject
from Render.Hardware.Shaders.Shader import Shader

class HardwareRenderObject(AbstractRenderObject):
    
    shader:Shader
    VAOIndex:int
    VBOIndex:int
    vertices:array

    def initVertices(self, vertices:tuple[tuple[float, float, float]], triangles:tuple[tuple[int, int, int]]) -> None:
        self.vertices = array(object=tuple(vertex for triangle in triangles for index in triangle for vertex in vertices[index]), dtype=float32)
        self.shader = Shader()
        self.VAOIndex = glGenVertexArrays(1)
        self.VBOIndex = glGenBuffers(1)
        glBindVertexArray(self.VAOIndex)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOIndex)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)