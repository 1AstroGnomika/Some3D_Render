from typing import Type
from Render.SoftwareRender import SoftwareRender
from App.AbstractApp import AbstractApp

class SoftwareApp(AbstractApp):
     
     def getRender(self) -> Type[SoftwareRender]:
         return SoftwareRender