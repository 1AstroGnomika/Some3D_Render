from Render.Hardware.Buffers.AbstractGLResourcePool import AbstractGLInputData, AbstractGLResourceData, AbstractGLResourcePool
from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, GL_ACTIVE_UNIFORMS, glGetActiveUniform, glGetUniformLocation, glGetProgramiv, glDeleteProgram
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram

class ShaderGLInputData(AbstractGLInputData):

    BASE_VERTEX_SOURCE:str = """
        #version 330 core

        layout(location = 0) in vec3 position;
        layout(location = 1) in vec2 texcoord;
        layout(location = 2) in vec3 normal;

        out vec2 fragTexCoord;
        out vec3 fragNormal;
        out vec3 fragPosition;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main()
        {
            vec4 worldPosition = model * vec4(position, 1.0);
            fragTexCoord = texcoord;
            fragNormal = mat3(transpose(inverse(model))) * normal;
            fragPosition = worldPosition.xyz;
            gl_Position = projection * view * worldPosition;
        }
    """
    BASE_FRAGMENT_SOURCE:str = """
        #version 330 core

        in vec2 fragTexCoord;
        in vec3 fragNormal;
        in vec3 fragPosition;

        out vec4 fragColor;

        uniform sampler2D texture0;

        void main() {
            fragColor = texture(texture0, fragTexCoord);
        }
    """

    vertexSource:str
    fragmentSource:str

    def __init__(self, vertexSource:str=BASE_VERTEX_SOURCE, fragmentSource:str=BASE_FRAGMENT_SOURCE):
        self.vertexSource = vertexSource
        self.fragmentSource = fragmentSource

    def __hash__(self):
        return hash(self.vertexSource + self.fragmentSource)

class ShaderGLResourceData(AbstractGLResourceData):

    program:ShaderProgram
    uniforms:dict[str, tuple[int, int]]

    def __init__(self, program:int, uniforms:dict[str, tuple[int, int]]):
        self.program = program
        self.uniforms = uniforms

class ShaderGLResourcePool(AbstractGLResourcePool):

    def createGLResource(self, shaderInput:ShaderGLInputData):
        shaderData:ShaderGLResourceData =  ShaderGLResourceData(compileProgram(
            compileShader(shaderInput.vertexSource, GL_VERTEX_SHADER),
            compileShader(shaderInput.fragmentSource, GL_FRAGMENT_SHADER)
        ), dict())
        for name, _, uniformType in map(lambda index: glGetActiveUniform(shaderData.program, index), range(glGetProgramiv(shaderData.program, GL_ACTIVE_UNIFORMS))):
            shaderData.uniforms[name.decode()] = (
                glGetUniformLocation(shaderData.program, name),
                uniformType
            )
        return shaderData

    def deleteGLResource(self, glShaderData:ShaderGLResourceData):
        glDeleteProgram(glShaderData.program)