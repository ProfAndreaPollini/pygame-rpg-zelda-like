import pygame as pg
from spritesheet import Spritesheets


class Sword(pg.sprite.Sprite):
  def __init__(self,):
    super().__init__()
    s = Spritesheets()

    self.spritesheet = s.weapon_spritesheet

    image = self.spritesheet.get_surface("sword")
    rect = image.get_rect()
    self.image = image
    self.rect: pg.rect.Rect = rect
    self.position = pg.math.Vector2(rect.left, rect.top)
    self.angle = 0

  @property
  def x(self):
    return self.position.x

  @property
  def y(self):
    return self.position.y

  @x.setter
  def x(self, value):
    self.position.x = value
    self.rect.left = round(value)

  @y.setter
  def y(self, value):
    self.position.y = value
    self.rect.top = round(value)

  def set(self, x: float, y: float):
    self.position.x = x
    self.position.y = y
    self.__update_rect(x, y)

  def __update_rect(self, x: float, y: float):
    self.rect.left = round(x)
    self.rect.top = round(y)

  def update(self, dt: float, angle: float):
    print(f"update sword: {angle=}")
    self.angle = angle
