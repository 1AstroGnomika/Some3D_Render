import pygame
from App.SoftwareApp import SoftwareApp
from App.HardwareApp import HardwareApp
from Render.AbstractRenderObject import AbstractRenderObject
from Render.Software.SoftwareRenderObject import SoftwareRenderObject
from Render.Hardware.HardwareRenderObject import HardwareRenderObject
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from Utils.Vector3D import Vector3D
from Utils.Tools import Events
from Constants import Buttons

if __name__ == "__main__":

    FOW:float = 120
    WIDTH:int = 1280
    HEIGTH:int = 768
    MINRENDERDISTANCE:float = 0.1
    MAXRENDERDISTANCE:float = 500.0
    CAMERASPEED:float = 10.0
    CAMERAROTATIONSPEED:float = 10.0
    CUBEROTATESPEED:int = 10.0
    MOUSECAPTION:bool = True
    FRAMES:int = 60

    pygame.init()
    pygame.mouse.set_visible(not MOUSECAPTION)
    pygame.event.set_grab(MOUSECAPTION)

    app = HardwareApp(FRAMES, FOW, WIDTH, HEIGTH, MINRENDERDISTANCE, MAXRENDERDISTANCE)
    
    RenderObject:AbstractRenderObject = {
        SoftwareApp.__name__: SoftwareRenderObject,
        HardwareApp.__name__: HardwareRenderObject,
    }.get(type(app).__name__)

    @InputHandler.handlerEvents.buttonPressed
    def post_buttonPressed(event:Events.Event) -> None:
        button:int = event.args[0]
        ticks:float = app.timer.lastTicks / app.timer.tickPerSecond
        camera_speed:float = CAMERASPEED * ticks
        camera_rotation_speed:float = CAMERAROTATIONSPEED * ticks
        multiple:Vector3D = Vector3D(camera_speed, camera_speed, camera_speed)
        forward:Vector3D = app.render.camera.forward() * multiple
        right:Vector3D = app.render.camera.right() * multiple
        up:Vector3D = app.render.camera.up() * multiple
        if button == Buttons.KEY_W:
            app.render.camera.point.x += forward.x
            app.render.camera.point.y += forward.y
            app.render.camera.point.z += forward.z
        elif button == Buttons.KEY_S:
             app.render.camera.point.x -= forward.x
             app.render.camera.point.y -= forward.y
             app.render.camera.point.z -= forward.z
        elif button == Buttons.KEY_A:
             app.render.camera.point.x -= right.x
             app.render.camera.point.y -= right.y
             app.render.camera.point.z -= right.z
        elif button == Buttons.KEY_D:
             app.render.camera.point.x += right.x
             app.render.camera.point.y += right.y
             app.render.camera.point.z += right.z
        elif button == Buttons.KEY_LSHIFT:
             app.render.camera.point.x -= up.x
             app.render.camera.point.y -= up.y
             app.render.camera.point.z -= up.z
        elif button == Buttons.KEY_SPACE:
             app.render.camera.point.x += up.x
             app.render.camera.point.y += up.y
             app.render.camera.point.z += up.z
        elif button == Buttons.KEY_Q:
            app.render.camera.rotation.z += camera_rotation_speed
        elif button == Buttons.KEY_E:
            app.render.camera.rotation.z -= camera_rotation_speed
        elif button == Buttons.KEY_ESC:
            app.running = not app.running
        else:
            print(button)

    @InputHandler.handlerEvents.mouseShift
    def post_mouseShift(event:Events.Event) -> None:
        shiftX, shiftY = event.args[0]
        if shiftX or shiftY:
            camera_rotation_speed: float = CAMERAROTATIONSPEED * (app.timer.lastTicks / app.timer.tickPerSecond)
            rotX:float = ((shiftX / 100.0) * camera_rotation_speed)
            rotY:float = ((shiftY / 100.0) * camera_rotation_speed)
            app.render.camera.rotation.x -= rotX
            app.render.camera.rotation.y -= rotY
            if MOUSECAPTION:
                pygame.mouse.set_pos((app.render.camera.width // 2, app.render.camera.height // 2))

    @InputHandler.handlerEvents.mouseButtonDown
    def post_mouseButtonDown(event:Events.Event) -> None:
        ...

    @InputHandler.handlerEvents.mouseButtonUp
    def post_mouseButtonUp(event:Events.Event) -> None:
        ...

    @EventHandler.handlerEvents.handleEvent
    def post_event(event:Events.Event) -> None:
        pygameEvent:pygame.event.Event = event.args[0]
        if pygameEvent.type == pygame.QUIT:
            app.running = not app.running

    @EventHandler.handlerEvents.handle
    def post_handle(event:Events.Event) -> None:
        pygame.display.set_caption(f"Framarate: {round(app.pygameTimer.get_fps(), 1)}")

    def parse_obj(path:str):
        vertices:list[tuple[int, int, int]] = list()
        triangles:list[tuple[int, int]] = []
        with open(path, 'r') as model:
            for line in model:
                parts = line.strip().split()
                if not parts:
                    continue
                if parts[0] == 'v':
                    x, y, z = tuple(map(float, parts[1:4]))
                    vertices.append((x, -y, z))
                elif parts[0] == 'f':
                    faces:list[int] = list()
                    for part in parts[1:]:
                        faces.append(int(part.split('/')[0]) - 1)
                    for index in range(1, len(faces) - 1):
                        triangles.append((
                            faces[0],
                            faces[index],
                            faces[index + 1]
                        ))
        return tuple(vertices), tuple(triangles)

    app.render.renderObjects = (
        RenderObject(*parse_obj("./Models/IS4.obj"), 5.0, Vector3D(0, 0, 35), Vector3D()),
        RenderObject(*parse_obj("./Models/monkey.obj"), 10.0, Vector3D(25, 0, 25), Vector3D()),
        RenderObject(*parse_obj("./Models/turtle.obj"), 1.5, Vector3D(-25, 0, 25), Vector3D(y=90))
    )
    while app.running:
        app.update()