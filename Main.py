import pygame
from GameLogic import GameLogic
from App.SoftwareApp import SoftwareApp
from App.HardwareApp import HardwareApp
from Render.AbstractRenderObject import AbstractRenderObject
from Render.Software.SoftwareRenderObject import SoftwareRenderObject
from Render.Hardware.HardwareRenderObject import HardwareRenderObject
from Render.GeometryGenerator import GeometryGenerator
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from Utils.Vector3D import Vector3D
from Utils.Tools import Events
from Constants import Buttons

if __name__ == "__main__":

    ANGLE:float = 1.0
    WIDTH:int = 800
    HEIGTH:int = 600
    MINRENDERDISTANCE:float = 0.0
    MAXRENDERDISTANCE:float = 500.0
    CAMERASPEED:float = 10.0
    CAMERAROTATIONSPEED:float = 10.0
    CUBEROTATESPEED:int = 10.0
    MOUSECAPTION:bool = True
    FRAMES:int = 60

    pygame.init()
    pygame.mouse.set_visible(not MOUSECAPTION)
    pygame.event.set_grab(MOUSECAPTION)

    GameLogic.App = SoftwareApp(FRAMES, ANGLE, WIDTH, HEIGTH, MINRENDERDISTANCE, MAXRENDERDISTANCE)
    
    RenderObject:AbstractRenderObject = {
        SoftwareApp.__name__: SoftwareRenderObject,
        HardwareApp.__name__: HardwareRenderObject,
    }.get(type(GameLogic.App).__name__)

    GameLogic.App.render.renderContainer.addToRender(RenderObject(
        *GeometryGenerator.sphere(10.0, 25, 25),
        1.0,
        Vector3D(0, 0, 25),
        Vector3D(),
    ))

    @InputHandler.handlerEvents.buttonPressed
    def post_buttonPressed(event:Events.Event) -> None:
        button:int = event.args[0]
        ticks:float = GameLogic.App.timer.lastTicks / GameLogic.App.timer.ticksPerSecond
        camera_speed:float = CAMERASPEED * ticks
        camera_rotation_speed:float = CAMERAROTATIONSPEED * ticks
        cube_rotation_speed:float = CUBEROTATESPEED * ticks
        multiple:Vector3D = Vector3D(camera_speed, camera_speed, camera_speed)
        forward:Vector3D = GameLogic.App.render.camera.forward() * multiple
        right:Vector3D = GameLogic.App.render.camera.right() * multiple
        up:Vector3D = GameLogic.App.render.camera.up() * multiple
        if button == Buttons.KEY_W:
            GameLogic.App.render.camera.point.x += forward.x
            GameLogic.App.render.camera.point.y += forward.y
            GameLogic.App.render.camera.point.z += forward.z
        elif button == Buttons.KEY_S:
             GameLogic.App.render.camera.point.x -= forward.x
             GameLogic.App.render.camera.point.y -= forward.y
             GameLogic.App.render.camera.point.z -= forward.z
        elif button == Buttons.KEY_A:
             GameLogic.App.render.camera.point.x -= right.x
             GameLogic.App.render.camera.point.y -= right.y
             GameLogic.App.render.camera.point.z -= right.z
        elif button == Buttons.KEY_D:
             GameLogic.App.render.camera.point.x += right.x
             GameLogic.App.render.camera.point.y += right.y
             GameLogic.App.render.camera.point.z += right.z
        elif button == Buttons.KEY_LSHIFT:
             GameLogic.App.render.camera.point.x -= up.x
             GameLogic.App.render.camera.point.y -= up.y
             GameLogic.App.render.camera.point.z -= up.z
        elif button == Buttons.KEY_SPACE:
             GameLogic.App.render.camera.point.x += up.x
             GameLogic.App.render.camera.point.y += up.y
             GameLogic.App.render.camera.point.z += up.z
        elif button == Buttons.KEY_Q:
            GameLogic.App.render.camera.rotation.z += camera_rotation_speed
        elif button == Buttons.KEY_E:
            GameLogic.App.render.camera.rotation.z -= camera_rotation_speed
        elif button == Buttons.KEY_ESC:
            GameLogic.App.running = not GameLogic.App.running
        else:
            print(button)

    @InputHandler.handlerEvents.mouseShift
    def post_mouseShift(event:Events.Event) -> None:
        shiftX, shiftY = event.args[0]
        if shiftX or shiftY:
            camera_rotation_speed: float = CAMERAROTATIONSPEED * (GameLogic.App.timer.lastTicks / GameLogic.App.timer.ticksPerSecond)
            rotX:float = ((shiftX / 100.0) * camera_rotation_speed)
            rotY:float = ((shiftY / 100.0) * camera_rotation_speed)
            GameLogic.App.render.camera.rotation.x -= rotX
            GameLogic.App.render.camera.rotation.y -= rotY
            if MOUSECAPTION:
                pygame.mouse.set_pos((GameLogic.App.render.camera.width // 2, GameLogic.App.render.camera.height // 2))

    @EventHandler.handlerEvents.handleEvent
    def post_event(event:Events.Event) -> None:
        pygameEvent:pygame.event.Event = event.args[0]
        if pygameEvent.type == pygame.QUIT:
            GameLogic.App.running = not GameLogic.App.running

    @EventHandler.handlerEvents.handle
    def post_handle(event:Events.Event) -> None:
        pygame.display.set_caption(f"Framarate: {round(GameLogic.App.pygameTimer.get_fps(), 1)}")

    GameLogic.mainLoop()