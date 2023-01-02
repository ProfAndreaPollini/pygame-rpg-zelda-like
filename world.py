from dataclasses import dataclass
from typing import List
import pygame as pg

from settings import SPRITE_SIZE, SPRITE_SCALE
from spritesheet import Spritesheet


@dataclass
class Tile:
  name: str


class World:

  def __init__(self, config_filename: str, tile_size=(SPRITE_SIZE, SPRITE_SIZE)) -> None:
    self.tiles: List[Tile] = []
    self.size = (0, 0)
    self.tile_size = tile_size
    self.spritesheet = Spritesheet(config_filename)

  def at(self, row: int, col: int) -> Tile:
    return self.tiles[col + row*self.size[1]]

  def add_tile(self, tile: Tile):
    self.tiles.append(tile)

  def update_surface(self):
    self.surface = pg.surface.Surface(
        (self.size[1] * self.tile_size[1] * SPRITE_SCALE, self.size[0]*self.tile_size[0]*SPRITE_SCALE))
    for i in range(len(self.tiles)):
      row = i // self.size[1]
      col = i % self.size[1]
      name = self.tiles[i].name

      s = self.spritesheet.get_surface(name)
      # print(f"{row=} {col=} {name=} {s=}")
      self.surface.blit(
          s, (col * self.tile_size[1]*SPRITE_SCALE, row*self.tile_size[0]*SPRITE_SCALE))

  def __repr__(self) -> str:
    return f"{self.size=} |> {self.tiles}"

  @staticmethod
  def from_file(filename: str, spritesheet_conf_file: str) -> "World":
    map_config = []
    with open(filename) as fp:
      for line in fp:
        line = line.strip()
        map_config.append(line)

    world = World(spritesheet_conf_file)
    world.size = (len(map_config), len(list(map_config[0])))
    for r, row in enumerate(map_config):
      for c, t in enumerate(list(row)):
        match t:
          case "#":
            tile_name = "wall"
          case ".":
            tile_name = "floor"
        world.add_tile(Tile(tile_name))

    world.update_surface()
    return world
