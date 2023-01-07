from math import floor
import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE
from typing import TYPE_CHECKING

from player import Player
from world import World
from camera import Camera
from ui import UI

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

player = Player(0, 0)


running = True

dt = 0

world = World.from_tmx("assets/maps/map0.tmx",
                       "config/world.sprites.json", player)


def handle_input():
    keys = pg.key.get_pressed()  # recupero tutti i tasti premuti (List[bool])

    look_dir = pg.math.Vector2()

    if keys[pg.K_a]:
        look_dir.x = -1
    elif keys[pg.K_s]:
        look_dir.y = 1
    elif keys[pg.K_d]:
        look_dir.x = 1
    elif keys[pg.K_w]:
        look_dir.y = -1

    if keys[pg.K_SPACE]:
        player.attack()

    if look_dir.magnitude_squared() > 1:  # se movimento diagonale, fix
        look_dir /= look_dir.magnitude()

    player.dir = look_dir
    # player.move(look_dir.x, look_dir.y)


camera = Camera(player, screen.get_width(), screen.get_height())
camera.add(player)

ui = UI(player)

while running:
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    handle_input()

    player.update(dt)

    player.update_x(dt)
    world.collide_horizontal(player, dt)

    player.update_y(dt)
    world.collide_vertical(player, dt)

    screen.fill("gray")

    # show sprite
    # screen.blit(player.image, player.rect)
    camera.update()
    screen.blit(world.surface, (-camera.camera.x, -camera.camera.y))

    desired_rect = player.get_desired_rect(dt)
    desired_rect.left -= camera.camera.x
    desired_rect.top -= camera.camera.y
    # print(desired_rect)
    pg.draw.rect(screen, (0, 0, 255), desired_rect, 2)
    # print("NW = ",len(world.non_walkable_sprites.sprites()))

    for nwp in world.non_walkable_sprites.sprites():
        assert nwp.rect is not None
        # screen.blit(nwp.image, (nwp.rect.left-camera.camera.x,nwp.rect.top -camera.camera.y))
        pg.draw.rect(screen, (255, 0, 0), nwp.rect.copy(
        ).move(-camera.camera.x, -camera.camera.y), 4)
    bb = player.rect.copy()
    bb.left -= camera.camera.x
    bb.top -= camera.camera.y
    pg.draw.rect(screen, (255, 255, 0), bb, 2)

    collisions = pg.sprite.spritecollide(
        player, world.non_walkable_sprites, False)
    if collisions:
        for c in collisions:
            assert c.rect is not None
            screen.blit(c.image, c.rect.copy(
            ).move(-camera.camera.x, -camera.camera.y))
    # Draw the objects in the camera group on the screen
    for sprite in camera.sprites():
        if TYPE_CHECKING:
            assert sprite.image is not None
            assert sprite.rect is not None
        screen.blit(
            sprite.image, sprite.rect.copy().move(-camera.camera.x, -camera.camera.y))

    if player.attacking:
        screen.blit(
            player.sword_image, player.sword_rect.copy().move(-camera.camera.x, -camera.camera.y))
    
    ui.draw()
    pg.display.update()


pg.quit()
