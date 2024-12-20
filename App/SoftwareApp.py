from typing import Type
from Render.Software.SoftwareRender import SoftwareRender
from Render.Software.SoftwareCamera import SoftwareCamera
from App.AbstractApp import AbstractApp

class SoftwareApp(AbstractApp):
     
    def getCamera(self) -> type[SoftwareCamera]:
        return SoftwareCamera

    def getRender(self) -> Type[SoftwareRender]:
        return SoftwareRender