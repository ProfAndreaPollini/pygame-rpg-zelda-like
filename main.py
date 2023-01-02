import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE

print("hello world")

pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

running = True

# load sprite
player_spritesheet = pg.image.load(
    "assets/PixelMood4/Pixel Mood/Chars/Heros/Sprite sheet female hero.png").convert_alpha()

player_sprite = player_spritesheet.subsurface((0, 0, 16, 16))
original_size = player_sprite.get_size()

player_sprite = pg.transform.scale(
    player_sprite, (original_size[0]*SPRITE_SCALE, original_size[1]*SPRITE_SCALE))

while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

  screen.fill("black")

  # show sprite
  screen.blit(player_sprite, (50, 50))

  pg.display.flip()


pg.quit()
