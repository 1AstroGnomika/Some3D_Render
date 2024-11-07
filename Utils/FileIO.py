import os, typing

class Creator:

    path:str
    
    def __init__(self, path:str):
        self.path = os.path.abspath(path)
        self.createPath(self.path)
    
    def createPath(self, path:str):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

class Loader(Creator):

    mode:str
    encoding:str
    __file:typing.IO

    def __init__(self, path:str, mode:str, encoding:str) -> None:
        self.mode = mode
        self.encoding = encoding
        self.__file = None
        super().__init__(path)

    @property
    def file(self) -> typing.IO:
        if self.__file is None:
            self.__file = open(self.path, self.mode, encoding=self.encoding)
        return self.__file


class Reader(Loader):

    def read(self, default:typing.Any) -> typing.Any:
        try:
            return self.file.read()
        except:
            ...
        return default
                
class Writer(Loader):

    def write(self, data:typing.Any) -> None:
        self.file.write(data)