from Render.AbstractRender import AbstractRender
from abc import ABC, abstractmethod

class AbstractApp(ABC):
    
    running:bool = True
    render:AbstractRender