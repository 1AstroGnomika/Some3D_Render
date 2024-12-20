from typing import Type
from Render.Hardware.HardwareRender import HardwareRender
from Render.Hardware.HardwareCamera import HardwareCamera
from App.AbstractApp import AbstractApp

class HardwareApp(AbstractApp):
     
    def getCamera(self) -> type[HardwareCamera]:
        return HardwareCamera

    def getRender(self) -> Type[HardwareRender]:
        return HardwareRender