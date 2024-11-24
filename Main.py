import pygame
from Game import Game
from App.SoftwareApp import SoftwareApp
from Render.RenderObject import RenderObject
from Handler.InputHandler import InputHandler
from Handler.EventHandler import EventHandler
from Utils.Vector3D import Vector3D
from Utils.Tools import Events
from Constants import Buttons

if __name__ == "__main__":

    ANGLE:float = 1.0
    WIDTH:int = 1024
    HEIGTH:int = 768
    MINRENDERDISTANCE:float = 0.0
    MAXRENDERDISTANCE:float = 50.0
    CAMERASPEED:float = 10.0
    CUBEROTATESPEED:int = 10.0
    MOUSECAPTION:bool = True

    pygame.init()
    pygame.mouse.set_visible(not MOUSECAPTION)
    pygame.event.set_grab(MOUSECAPTION)

    game:Game = Game(SoftwareApp(ANGLE, WIDTH, HEIGTH, MINRENDERDISTANCE, MAXRENDERDISTANCE), 60)

    game.app.render.renderContainer.addToRender(CUBE := RenderObject(
        [
            (-1, -1, -1),
            (1, -1, -1),
            (1, 1, -1),
            (-1, 1, -1),
            (-1, -1, 1),
            (1, -1, 1),
            (1, 1, 1),
            (-1, 1, 1),
        ],
        [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ],
        Vector3D(z=-10.0),
        0.0,
        0.0,
        0.0,
        1.0
        )
    )

    @InputHandler.handlerEvents.buttonPressed
    def post_buttonPressed(event:Events.Event) -> None:
        button:int = event.args[0]
        camera_speed:float = CAMERASPEED * (game.timer.lastTicks / game.timer.ticksPerSecond)
        cube_rotation_speed:float = CUBEROTATESPEED * (game.timer.lastTicks / game.timer.ticksPerSecond)
        if button == Buttons.KEY_W:
             game.app.render.camera.position.z -= camera_speed
        elif button == Buttons.KEY_S:
             game.app.render.camera.position.z += camera_speed
        elif button == Buttons.KEY_A:
             game.app.render.camera.position.x -= camera_speed
        elif button == Buttons.KEY_D:
             game.app.render.camera.position.x += camera_speed
        elif button == Buttons.KEY_LSHIFT:
             game.app.render.camera.position.y -= camera_speed
        elif button == Buttons.KEY_SPACE:
             game.app.render.camera.position.y += camera_speed
        elif button == Buttons.KEY_Q:
            game.app.render.camera.rotation.z += camera_speed
        elif button == Buttons.KEY_E:
            game.app.render.camera.rotation.z -= camera_speed
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
            game.app.running = not game.app.running
        else:
            print(button)
        print(game.app.render.camera.position)

    @InputHandler.handlerEvents.mouseMove
    def post_mouseMove(event:Events.Event) -> None:
        mouseX, mouseY = event.args[0]
        centerX, centerY = game.app.render.width // 2, game.app.render.heigth // 2
        shiftX, shiftY = centerX - mouseX, centerY - mouseY
        game.app.render.camera.rotation.x += shiftX / 10
        game.app.render.camera.rotation.y += shiftY / 10
        game.app.render.camera.rotation.x = game.app.render.camera.rotation.x % 360.0
        game.app.render.camera.rotation.y = game.app.render.camera.rotation.y % 360.0
        pygame.mouse.set_pos((centerX, centerY))

    @EventHandler.handlerEvents.handleEvent
    def post_event(event:Events.Event) -> None:
        pygameEvent:pygame.event.Event = event.args[0]
        if pygameEvent.type == pygame.QUIT:
            game.app.running = not game.app.running

    while game.app.running:
        game.update()