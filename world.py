from dataclasses import dataclass
from typing import Dict, List, Optional
import pygame as pg
from player import Player

from settings import SPRITE_SIZE, SPRITE_SCALE
from spritesheet import Spritesheet
from pytmx import TiledMap, TiledTileLayer
from pytmx.util_pygame import load_pygame, pygame_image_loader

@dataclass
class Tile:
  name: str


class WorldSpritesheet:

  def __init__(self) -> None:
    self.sprites: Dict[str, pg.surface.Surface] = {}

  def add_sprite(self, name: str, surface: pg.surface.Surface, scale=SPRITE_SCALE):
    s = surface.copy()
    original_size = s.get_size()
    s = pg.transform.scale(s, (original_size[0]*scale, original_size[1]*scale))
    self.sprites[name] = s

  def get_surface(self, name: str) -> pg.surface.Surface:
    """return the surface by name"""
    return self.sprites.get(name, pg.surface.Surface((SPRITE_SIZE*SPRITE_SCALE, SPRITE_SIZE*SPRITE_SCALE)))

class World:

  def __init__(self, config_filename: Optional[str] = None, tile_size=(SPRITE_SIZE, SPRITE_SIZE)) -> None:
    self.tiles: List[Tile] = []
    self.size = (0, 0)
    self.tile_size = tile_size
    self.spritesheet = WorldSpritesheet(
    ) if config_filename is None else Spritesheet(config_filename)

  def at(self, row: int, col: int) -> Tile:
    return self.tiles[col + row*self.size[1]]

  def add_tile(self, tile: Tile):
    self.tiles.append(tile)

  def __update_surface(self):
    self.surface = pg.surface.Surface(
        (self.size[1] * self.tile_size[1] * SPRITE_SCALE, self.size[0]*self.tile_size[0]*SPRITE_SCALE))
    for i in range(len(self.tiles)):
      row = i // self.size[1]
      col = i % self.size[1]
      name = self.tiles[i].name

      s = self.spritesheet.get_surface(name)
      #print(f"{row=} {col=} {name=} {s=}")
      self.surface.blit(
          s, (col * self.tile_size[1]*SPRITE_SCALE, row*self.tile_size[0]*SPRITE_SCALE))

  def __repr__(self) -> str:
    return f"{self.size=} |> {self.tiles}"

  @staticmethod
  def from_tmx(tmx_filename: str, spritesheet_conf_file: str, player: Player) -> "World":
    tmxdata = load_pygame(tmx_filename)

    terrain: TiledTileLayer = tmxdata.get_layer_by_name("terrain")
    player_object = tmxdata.get_object_by_name("player")
    print(f"{terrain.width=} {terrain.height=}")
    print(player_object.x,player_object.y)
    print(player_object.x*SPRITE_SCALE, player_object.y*SPRITE_SCALE)
    player.set(player_object.x*SPRITE_SCALE, player_object.y*SPRITE_SCALE)
    world = World()
    world.size = (terrain.height, terrain.width)
    gids = set()

    world.tiles = []
    for i in range((terrain.width * terrain.height)):
      world.tiles.append(Tile("0"))
    for x, y, gid in terrain.iter_data():
      # print(x, y, gid)
      if gid > 0:
        world.tiles[x + y * terrain.width].name = str(gid)
        # print(world.tiles[x + y * terrain.width].name)
      gids.add(gid)

    print(gids)
    for gid in list(gids):
      s = tmxdata.get_tile_image_by_gid(gid)
      if s is not None:
        world.spritesheet.add_sprite(str(gid), s)

    # print(list(tmxdata.get_tile_locations_by_gid(0)))
    # for row in range(terrain.height):
    #   for col in range(terrain.width):
    #     t = tmxdata.get_tile_properties(col, row, terrain.)
    #     print(t, end=", ")
    #   print()
    world.__update_surface()
    return world


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

    world.__update_surface()
    return world
