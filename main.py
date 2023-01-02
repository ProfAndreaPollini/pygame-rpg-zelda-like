import pygame as pg
from settings import SCREEN_SIZE

print("hello world")

screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

running = True


while running:
  for event in pg.event.get():
    if event.type == pg.QUIT:
      running = False

  screen.fill("black")

  pg.display.update()


pg.quit()
