from typing import Dict
import pygame as pg

from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE


class Spritesheet:

  def __init__(self, filename: str) -> None:
    self.spritesheet = pg.image.load(filename).convert_alpha()
    self.sprites: Dict[str, pg.surface.Surface] = {}

  def define_surface(self, name: str, row: int, col: int, size=(SPRITE_SIZE, SPRITE_SIZE), scale=SPRITE_SCALE) -> None:
    "define a new surface for the current spritesheet"
    sprite_subsurface = self.spritesheet.subsurface(
        col*size[0], row*size[1], *size)
    original_size = sprite_subsurface.get_size()

    scaled = pg.transform.scale(
        sprite_subsurface, (original_size[0]*scale, original_size[1]*scale))
    self.sprites[name] = scaled

  def get_player_surface(self) -> pg.surface.Surface:
    return self.get_surface("player")

  # def get_surface(self, row, col, size=(SPRITE_SIZE, SPRITE_SIZE), scale=SPRITE_SCALE):
  #   sprite_subsurface = self.spritesheet.subsurface(
  #       (col*size[0], row*size[1], *size))
  #   original_size = sprite_subsurface.get_size()

  #   scaled = pg.transform.scale(
  #       sprite_subsurface, (original_size[0]*scale, original_size[1]*scale))
  #   return scaled

  def get_surface(self, name: str) -> pg.surface.Surface:
    """return the surface by name"""
    return self.sprites.get(name,pg.surface.Surface((SPRITE_SIZE*SPRITE_SCALE,SPRITE_SIZE*SPRITE_SCALE)))