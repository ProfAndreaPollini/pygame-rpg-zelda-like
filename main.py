from math import floor
import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE
from typing import TYPE_CHECKING

from player import Player
from world import World

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

player = Player(0, 0)


class Camera(pg.sprite.Group):
    def __init__(self, player, screen_width, screen_height):
        super().__init__()
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.old_center = self.player.rect.center

    def update(self):
        # Center the camera on the player
        self.center(self.player.rect.center)

    def center(self, center):
        center_x = center[0]
        center_y = center[1]
        # print(abs((center[0] -self.old_center[0])**2  - (self.old_center[1] - center[1])**2))
        if abs((center[0] - self.old_center[0])**2 - (self.old_center[1] - center[1])**2) > 100:
            # Keep the center of the camera within the boundaries of the game world
            # max(center[0], self.screen_width // 2)
            center_x = 0.5*center[0] + 0.5*self.old_center[0]
            # center_x = min(center_x, self.player.image.width -
            #    self.screen_width // 2)
            # max(center[1], self.screen_height // 2)
            center_y = 0.5*center[1] + 0.5*self.old_center[1]
            # center_y = min(center_y, self.player.image.height -
            #    self.screen_height // 2)
            self.old_center = center
        self.camera = pg.rect.Rect(center_x - self.screen_width // 2, center_y -
                                   self.screen_height // 2, self.screen_width, self.screen_height)



running = True

dt = 0

world = World.from_tmx("assets/maps/map0.tmx",
                       "config/world.sprites.json", player)

print(player.rect.center)

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

    if look_dir.magnitude_squared() > 1:  # se movimento diagonale, fix
        look_dir /= look_dir.magnitude()

    player.dir = look_dir
    # player.move(look_dir.x, look_dir.y)


camera = Camera(player, screen.get_width(), screen.get_height())
camera.add(player)
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

    pg.display.update()


pg.quit()
