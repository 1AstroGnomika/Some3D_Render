import pygame
from GameLogic import GameLogic
from App.SoftwareApp import SoftwareApp
from Render.RenderObject import RenderObject
from Render.GeometryGenerator import GeometryGenerator
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from Utils.Vector3D import Vector3D
from Utils.Tools import Events, limiter
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
    
    GameLogic.App.render.renderContainer.addToRender(CUBE := RenderObject(
        *GeometryGenerator.sphere(1, 25, 25),
        Vector3D(z=-0.0),
        0.0,
        0.0,
        0.0,
        1.0
        )
    )

    @InputHandler.handlerEvents.buttonPressed
    def post_buttonPressed(event:Events.Event) -> None:
        button:int = event.args[0]
        ticks:float = GameLogic.App.timer.lastTicks / GameLogic.App.timer.ticksPerSecond
        camera_speed:float = CAMERASPEED * ticks
        camera_rotation_speed:float = CAMERAROTATIONSPEED * ticks
        cube_rotation_speed:float = CUBEROTATESPEED * ticks
        cos_yaw, sin_yaw, cos_pitch, sin_pitch, cos_roll, sin_roll = RenderObject.calculateAngles(*GameLogic.App.render.camera.rotation.coordinates())
        if button == Buttons.KEY_W:
             GameLogic.App.render.camera.position.z += camera_speed * cos_yaw
             GameLogic.App.render.camera.position.y += camera_speed * sin_pitch
             GameLogic.App.render.camera.position.x -= camera_speed * sin_yaw
        elif button == Buttons.KEY_S:
             GameLogic.App.render.camera.position.z -= camera_speed * cos_yaw
             GameLogic.App.render.camera.position.y -= camera_speed * sin_pitch
             GameLogic.App.render.camera.position.x += camera_speed * sin_yaw
        elif button == Buttons.KEY_A:
             GameLogic.App.render.camera.position.z -= camera_speed * sin_yaw
             GameLogic.App.render.camera.position.y -= camera_speed * sin_roll
             GameLogic.App.render.camera.position.x -= camera_speed * cos_yaw
        elif button == Buttons.KEY_D:
             GameLogic.App.render.camera.position.z += camera_speed * sin_yaw
             GameLogic.App.render.camera.position.y += camera_speed * sin_roll
             GameLogic.App.render.camera.position.x += camera_speed * cos_yaw
        elif button == Buttons.KEY_LSHIFT:
            GameLogic.App.render.camera.position.y -= camera_speed
        elif button == Buttons.KEY_SPACE:
             GameLogic.App.render.camera.position.y += camera_speed
        elif button == Buttons.KEY_Q:
            GameLogic.App.render.camera.rotation.z += camera_rotation_speed
        elif button == Buttons.KEY_E:
            GameLogic.App.render.camera.rotation.z -= camera_rotation_speed
        elif button == Buttons.KEY_RIGHT:
             CUBE.yaw += cube_rotation_speed
        elif button == Buttons.KEY_LEFT:
             CUBE.yaw -= cube_rotation_speed
        elif button == Buttons.KEY_DOWN:
             CUBE.pitch += cube_rotation_speed
        elif button == Buttons.KEY_UP:
            CUBE.pitch -= cube_rotation_speed
        elif button == Buttons.KEY_NUM_PLUS:
            CUBE.size += cube_rotation_speed
        elif button == Buttons.KEY_NUM_MINUS:
            CUBE.size -= cube_rotation_speed
        elif button == Buttons.KEY_ESC:
            GameLogic.App.running = not GameLogic.App.running
        else:
            print(button)
        print(GameLogic.App.render.camera.position)

    @InputHandler.handlerEvents.mouseShift
    def post_mouseShift(event: Events.Event) -> None:
        shiftX, shiftY = event.args[0]
        if shiftX or shiftY:
            camera_rotation_speed: float = CAMERAROTATIONSPEED * (GameLogic.App.timer.lastTicks / GameLogic.App.timer.ticksPerSecond)
            rotX:float = ((shiftX / 100.0) * camera_rotation_speed)
            rotY:float = ((shiftY / 100.0) * camera_rotation_speed)
            GameLogic.App.render.camera.rotation.x -= rotX
            GameLogic.App.render.camera.rotation.y -= rotY
            if MOUSECAPTION:
                pygame.mouse.set_pos((GameLogic.App.render.width // 2, GameLogic.App.render.height // 2))

    @EventHandler.handlerEvents.handleEvent
    def post_event(event:Events.Event) -> None:
        pygameEvent:pygame.event.Event = event.args[0]
        if pygameEvent.type == pygame.QUIT:
            GameLogic.App.running = not GameLogic.App.running

    @EventHandler.handlerEvents.handle
    def post_handle(event:Events.Event) -> None:
        pygame.display.set_caption(f"Framarate: {round(GameLogic.App.pygameTimer.get_fps(), 1)}")

    GameLogic.mainLoop()