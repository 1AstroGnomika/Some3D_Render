from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram

class Shader:

    SHADERS:dict[int, ShaderProgram] = dict()
    BASE_VERTEX_SOURCE:str = """
        #version 330 core
        layout (location = 0) in vec3 position;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        void main() {
            gl_Position = projection * view * model * vec4(position, 1.0);
        }
    """
    BASE_FRAGMENT_SOURCE:str = """
        #version 330 core
        out vec4 FragColor;
        void main() {
            FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
        }
    """

    program:ShaderProgram

    def __init__(self, vertexSource:str=BASE_VERTEX_SOURCE, fragmentSource:str=BASE_FRAGMENT_SOURCE) -> None:
        if program := Shader.SHADERS.get(shaderHash := hash(vertexSource + fragmentSource)):
            self.program = program
        else:
            self.program = compileProgram(
                compileShader(vertexSource, GL_VERTEX_SHADER),
                compileShader(fragmentSource, GL_FRAGMENT_SHADER)
            )
            Shader.SHADERS[shaderHash] = self.program