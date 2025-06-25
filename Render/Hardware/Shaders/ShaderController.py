from typing import Any
from ctypes import c_float, c_int
from OpenGL.GL import (
    GL_FALSE, GL_FLOAT, GL_FLOAT_VEC2, GL_FLOAT_VEC3, GL_FLOAT_VEC4,
    GL_INT, GL_INT_VEC2, GL_INT_VEC3, GL_INT_VEC4,
    GL_BOOL, GL_FLOAT_MAT2, GL_FLOAT_MAT3, GL_FLOAT_MAT4,
    glUniform1f, glUniform2f, glUniform3f, glUniform4f,
    glUniform1i, glUniform2i, glUniform3i, glUniform4i,
    glUniformMatrix2fv, glUniformMatrix3fv, glUniformMatrix4fv,
    glGetUniformfv, glGetUniformiv
)
from Render.Hardware.Buffers.ShaderGLResourcePool import ShaderGLResourceData

class ShaderController:

    @staticmethod
    def setUniform(shaderData:ShaderGLResourceData, name:str, value:Any) -> bool:
        if uniformData := shaderData.uniforms.get(name):
            location, uniformType = uniformData
            if uniformType == GL_FLOAT:
                glUniform1f(location, float(value))
            elif uniformType == GL_FLOAT_VEC2:
                glUniform2f(location, *value)
            elif uniformType == GL_FLOAT_VEC3:
                glUniform3f(location, *value)
            elif uniformType == GL_FLOAT_VEC4:
                glUniform4f(location, *value)
            elif uniformType == GL_INT or uniformType == GL_BOOL:
                glUniform1i(location, int(value))
            elif uniformType == GL_INT_VEC2:
                glUniform2i(location, *value)
            elif uniformType == GL_INT_VEC3:
                glUniform3i(location, *value)
            elif uniformType == GL_INT_VEC4:
                glUniform4i(location, *value)
            elif uniformType == GL_FLOAT_MAT2:
                glUniformMatrix2fv(location, 1, GL_FALSE, value)
            elif uniformType == GL_FLOAT_MAT3:
                glUniformMatrix3fv(location, 1, GL_FALSE, value)
            elif uniformType == GL_FLOAT_MAT4:
                glUniformMatrix4fv(location, 1, GL_FALSE, value)
            else: return False
            return True
        return False
    
    @staticmethod
    def getUniform(shaderData:ShaderGLResourceData, name: str) -> Any:
        value:Any = None
        if uniformData := shaderData.uniforms.get(name):
            location, uniformType = uniformData
            if uniformType == GL_FLOAT:
                value = (c_float * 1)()
                glGetUniformfv(shaderData.program, location, value)
                value = value[0]
            elif uniformType == GL_FLOAT_VEC2:
                value = (c_float * 2)()
                glGetUniformfv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_FLOAT_VEC3:
                value = (c_float * 3)()
                glGetUniformfv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_FLOAT_VEC4:
                value = (c_float * 4)()
                glGetUniformfv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_INT or uniformType == GL_BOOL:
                value = (c_int * 1)()
                glGetUniformiv(shaderData.program, location, value)
                value = value[0]
            elif uniformType == GL_INT_VEC2:
                value = (c_int * 2)()
                glGetUniformiv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_INT_VEC3:
                value = (c_int * 3)()
                glGetUniformiv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_INT_VEC4:
                value = (c_int * 4)()
                glGetUniformiv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_FLOAT_MAT2:
                value = (c_float * 4)()
                glGetUniformfv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_FLOAT_MAT3:
                value = (c_float * 9)()
                glGetUniformfv(shaderData.program, location, value)
                value = tuple(value)
            elif uniformType == GL_FLOAT_MAT4:
                value = (c_float * 16)()
                glGetUniformfv(shaderData.program, location, value)
                value = tuple(value)
        return value

    @staticmethod
    def hasUniform(shaderData:ShaderGLResourceData, name:str) -> bool:
        return name in shaderData.uniforms