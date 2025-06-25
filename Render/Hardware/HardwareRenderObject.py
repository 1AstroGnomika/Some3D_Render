from Render.Hardware.Buffers.ShaderGLResourcePool import ShaderGLInputData, ShaderGLResourceData, ShaderGLResourcePool
from Render.Hardware.Buffers.MeshGLResourcePool import MeshGLInputData, MeshGLResourceData, MeshGLResourcePool
from Render.Hardware.Buffers.TextureGLResourcePool import TextureGLInputData, TextureGLResourceData, TextureGLResourcePool
from Render.AbstractRenderObject import AbstractRenderObject
from Meshes.Mesh import Mesh
from array import array

class HardwareRenderObject(AbstractRenderObject):
    
    SHADERDATA:ShaderGLResourcePool = ShaderGLResourcePool()
    MESHDATA:MeshGLResourcePool = MeshGLResourcePool()
    TEXTUREDATA:TextureGLResourcePool = TextureGLResourcePool()

    __shader:ShaderGLResourceData = None
    __mesh:MeshGLResourceData = None
    __texture:TextureGLResourceData = None

    @property
    def shader(self) -> ShaderGLResourceData:
        return self.__shader

    @shader.setter
    def shader(self, shader:ShaderGLInputData):
        if self.__shader:
            HardwareRenderObject.SHADERDATA.releaseGLResource(self.__shader)
        if shader:
            self.__shader = HardwareRenderObject.SHADERDATA.getGLResource(shader)

    @property
    def mesh(self) -> MeshGLResourceData:
        return self.__mesh

    @mesh.setter
    def mesh(self, mesh:MeshGLInputData):
        if self.__mesh:
            HardwareRenderObject.MESHDATA.releaseGLResource(self.__mesh)
        if mesh:
            self.__mesh = HardwareRenderObject.MESHDATA.getGLResource(mesh)

    @property
    def texture(self) -> TextureGLResourceData:
        return self.__texture

    @texture.setter
    def texture(self, texture:TextureGLInputData):
        if self.__texture:
            HardwareRenderObject.TEXTUREDATA.releaseGLResource(self.__texture)
        if texture:
            self.__texture = HardwareRenderObject.TEXTUREDATA.getGLResource(texture)

    def processMesh(self, mesh: Mesh) -> None:
        self.shader = ShaderGLInputData()
        self.mesh = MeshGLInputData(array("f", tuple(
            item for face in mesh.faces for vi, vti, vni in face
            for item in (*mesh.vertices[vi], *mesh.texcoords[vti], *mesh.normals[vni])
        )).tobytes())
        self.texture = TextureGLInputData(mesh.texture) if mesh.texture else None

    def __del__(self) -> None:
        self.shader = None
        self.mesh = None
        self.texture = None