import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE

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

    def update(self):
        # Center the camera on the player
        self.center(self.player.rect.center)

    def center(self, center):
        # Keep the center of the camera within the boundaries of the game world
        center_x = max(center[0], self.screen_width // 2)
        # center_x = min(center_x, self.player.image.width -
        #    self.screen_width // 2)
        center_y = max(center[1], self.screen_height // 2)
        # center_y = min(center_y, self.player.image.height -
        #    self.screen_height // 2)
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
    if keys[pg.K_s]:
        look_dir.y = 1
    if keys[pg.K_d]:
        look_dir.x = 1
    if keys[pg.K_w]:
        look_dir.y = -1

    if look_dir.magnitude_squared() > 1:  # se movimento diagonale, fix
        look_dir /= look_dir.magnitude()

    player.look_dir = look_dir
    player.move(look_dir.x, look_dir.y)


camera = Camera(player, screen.get_width(), screen.get_height())
camera.add(player)
while running:
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    handle_input()
    player.update(dt)

    screen.fill("gray")

    # show sprite
    # screen.blit(player.image, player.rect)
    camera.update()
    screen.blit(world.surface, (-camera.camera.x, -camera.camera.y))
    # Draw the objects in the camera group on the screen
    for sprite in camera:
        screen.blit(
            sprite.image, sprite.rect.move(-camera.camera.x, -camera.camera.y))

    pg.display.update()


pg.quit()
