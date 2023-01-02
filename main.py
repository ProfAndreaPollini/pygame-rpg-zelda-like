import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE
 
from player import Player
from world import World

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

player = Player(50, 50)

running = True

dt = 0

world = World.from_file("config/world.map.txt", "config/world.sprites.json")
print(world)

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

    if look_dir.magnitude_squared() > 1: # se movimento diagonale, fix
      look_dir /= look_dir.magnitude()
   
    player.look_dir = look_dir
    player.move(look_dir.x, look_dir.y)


while running:
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    handle_input()

    screen.fill("black")
    screen.blit(world.surface, (100, 100))
    # show sprite
    screen.blit(player.image, player.rect)

    pg.display.update()


pg.quit()
