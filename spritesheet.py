import json
from typing import Any, Dict, List
import pygame as pg

from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE


class Spritesheet:

  def __init__(self, filename: str) -> None:
    with open(filename, 'r') as file:
      # Load the JSON data
      spritesheet_config = json.load(file)
    self.spritesheet = pg.image.load(
        spritesheet_config["spritesheet"]).convert_alpha()
    self.sprites: Dict[str, pg.surface.Surface] = {}

    self.sprites_setup(spritesheet_config["sprites"])

  def sprites_setup(self, config: List[Any]):
    for sprite_config in config:
      name, pos, size, scale = sprite_config["name"], sprite_config["pos"], sprite_config.get(
          "size", (SPRITE_SIZE, SPRITE_SIZE)), sprite_config.get("scale", SPRITE_SCALE)
      self.define_surface(name, pos[1], pos[0], size, scale)

  def define_surface(self, name: str, row: int, col: int, size=(SPRITE_SIZE, SPRITE_SIZE), scale=SPRITE_SCALE) -> None:
    "define a new surface for the current spritesheet"
    sprite_subsurface = self.spritesheet.subsurface(
        col*size[0], row*size[1], *size)
    original_size = sprite_subsurface.get_size()

    scaled = pg.transform.scale(
        sprite_subsurface, (original_size[0]*scale, original_size[1]*scale))
    self.sprites[name] = scaled

  def get_player_surface(self) -> pg.surface.Surface:
    return self.get_surface("idle_up")


  def get_surface(self, name: str) -> pg.surface.Surface:
    """return the surface by name"""
    return self.sprites.get(name,pg.surface.Surface((SPRITE_SIZE*SPRITE_SCALE,SPRITE_SIZE*SPRITE_SCALE)))