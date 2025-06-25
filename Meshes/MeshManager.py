from pygame import image
from pathlib import Path
from Meshes.Mesh import Mesh
from Utils.Binary.Decoder import Decoder
from Utils.Binary.Encoder import Encoder

class MeshManager:

    VERTICES:int = 1
    TEXCOORDS:int = 2
    NORMALS:int = 3
    FACES:int = 4
    TEXTURE:int = 5

    @staticmethod
    def load(filepath:str) -> Mesh:
        path:Path = Path(filepath)
        model:Mesh = Mesh(list(), list(), list(), list(), None)
        package:Decoder = Decoder(open(filepath, "rb").read())
        while package.available:
            number:int = package.readInt()
            decoder:Decoder = Decoder(package.readBytes(package.readInt()))
            match number:
                case MeshManager.VERTICES:
                    while decoder.available:
                        model.vertices.append((
                            decoder.readFloat(),
                            decoder.readFloat(),
                            decoder.readFloat()
                        ))
                case MeshManager.TEXCOORDS:
                    while decoder.available:
                        model.texcoords.append((
                            decoder.readFloat(),
                            decoder.readFloat()
                        ))
                case MeshManager.NORMALS:
                    while decoder.available:
                        model.normals.append((
                            decoder.readFloat(),
                            decoder.readFloat(),
                            decoder.readFloat()
                        ))
                case MeshManager.FACES:
                    while decoder.available:
                        model.faces.append((
                            (decoder.readInt(), decoder.readInt(), decoder.readInt()),
                            (decoder.readInt(), decoder.readInt(), decoder.readInt()),
                            (decoder.readInt(), decoder.readInt(), decoder.readInt())
                        ))
                case MeshManager.TEXTURE:
                    model.texture = image.load(f"{path.parent}/{path.stem}.png")
        return model

    @staticmethod
    def save(model:Mesh, filepath:str) -> None:
        with open(filepath, "wb") as result:
            vertices:Encoder = Encoder(MeshManager.VERTICES)
            for x, y, z in model.vertices:
                vertices.writeFloat(x)
                vertices.writeFloat(y)
                vertices.writeFloat(z)
            result.write(vertices.package())
            texcoords:Encoder = Encoder(MeshManager.TEXCOORDS)
            for x, y in model.texcoords:
                texcoords.writeFloat(x)
                texcoords.writeFloat(y)
            result.write(texcoords.package())
            normals:Encoder = Encoder(MeshManager.NORMALS)
            for x, y, z in model.normals:
                normals.writeFloat(x)
                normals.writeFloat(y)
                normals.writeFloat(z)
            result.write(normals.package())
            faces:Encoder = Encoder(MeshManager.FACES)
            for face in model.faces:
                for x, y, z in face:
                    faces.writeInt(x)
                    faces.writeInt(y)
                    faces.writeInt(z)
            result.write(faces.package())
            if model.texture:
                result.write(Encoder(MeshManager.TEXTURE).package())