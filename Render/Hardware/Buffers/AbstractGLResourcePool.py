from abc import ABC, abstractmethod
from typing import Hashable, Any

class AbstractGLInputData(ABC):

    @abstractmethod
    def __hash__(self): ...

class AbstractGLResourceData(ABC):

    key:Hashable = None
    count:int = 0

class AbstractGLResourcePool(ABC):

    __glResources: dict[Hashable, AbstractGLResourceData]

    def __init__(self):
        self.__glResources = dict()

    @abstractmethod
    def createGLResource(self, glInputData:AbstractGLInputData) -> AbstractGLResourceData: ...

    @abstractmethod
    def deleteGLResource(self, glResourceData:AbstractGLResourceData) -> None: ...

    def getGLResource(self, glInputData:AbstractGLInputData) -> AbstractGLResourceData:
        if resource := self.__glResources.get(key := hash(glInputData)):
            resource.count += 1
            return resource
        resource:AbstractGLResourceData = self.createGLResource(glInputData)
        resource.key = key
        resource.count = 1
        self.__glResources[key] = resource
        return resource

    def releaseGLResource(self, glResourceData:AbstractGLResourceData) -> None:
        if glResourceData := self.__glResources.get(glResourceData.key):
            glResourceData.count -= 1
            if glResourceData.count <= 0:
                self.deleteGLResource(glResourceData)
                self.__glResources.pop(glResourceData.key)