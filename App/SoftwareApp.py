from Render.SoftwareRender import SoftwareRender
from App.AbstractApp import AbstractApp

class SoftwareApp(AbstractApp):

    def __init__(self, *args, **kwargs) -> None:
        self.render = SoftwareRender(*args, **kwargs)