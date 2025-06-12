from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram

class Shader:

    SHADERS:dict[int, ShaderProgram] = dict()
    BASE_VERTEX_SOURCE:str = """
        #version 330 core
        layout (location = 0) in vec3 position;
        out float eyeSpaceDepth;

        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;

        void main() {
            vec4 worldPos = model * vec4(position, 1.0);
            vec4 eyePos = view * worldPos;
            eyeSpaceDepth = -eyePos.z;
            gl_Position = projection * eyePos;
        }
    """
    BASE_FRAGMENT_SOURCE:str = """
        #version 330 core
        out vec4 FragColor;
        in float eyeSpaceDepth;

        void main() {
            float brightness = 1.0 / (0.05 * eyeSpaceDepth + 1.0);
            brightness = clamp(brightness, 0.0, 1.0);
            vec3 color = vec3(1.0) * brightness;
            FragColor = vec4(color, 1.0);
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