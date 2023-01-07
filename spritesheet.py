import json
from typing import Any, Dict, List
import pygame as pg
from animation import Animation

from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE


class Spritesheet:
    def __init__(self):
        self.sprites: Dict[str, pg.surface.Surface] = {}
        self.animations : Dict[str,Animation] = {}

    def load_from_json(self, filename: str) -> None:
        with open(filename, 'r') as file:
            # Load the JSON data
            spritesheet_config = json.load(file)
        self.spritesheet = pg.image.load(
            spritesheet_config["spritesheet"]).convert_alpha()
        self.__sprites_setup(spritesheet_config["sprites"])
        self.__animations_setup(spritesheet_config.get("animations",None))

    def __animations_setup(self,config: Dict[str,Dict[str,Any]]):
      if config is None: return

      for name, animation_config in config.items():
        sprite_names = animation_config["sprites"]
        length_ms = animation_config.get("length",1000)
        autostart = animation_config.get("autostart",True)
        loop = animation_config.get("loop",True)
        animation = Animation(name,sprite_names,length_ms,loop=loop,autostart=autostart)
        self.animations[name] = animation

    def __sprites_setup(self, config: List[Any]):
        for sprite_config in config:
            name, pos, size, scale = sprite_config["name"], sprite_config["pos"], sprite_config.get(
                "size", None), sprite_config.get("scale", SPRITE_SCALE)
            if size is None:
                self.define_surface(
                    name, pos[0]*SPRITE_SIZE, pos[1]*SPRITE_SIZE, (SPRITE_SIZE, SPRITE_SIZE), scale)
            else:
                self.define_surface(name, pos[0], pos[1], size, scale)

    def define_surface(self, name: str, row: int, col: int, size=(SPRITE_SIZE, SPRITE_SIZE), scale=SPRITE_SCALE) -> None:
        "define a new surface for the current spritesheet"
        print(f"define_srface({name}, {row},{col},{size},{scale})")
        sprite_subsurface = self.spritesheet.subsurface(
            col, row, *size)
        original_size = sprite_subsurface.get_size()

        scaled = pg.transform.scale(
            sprite_subsurface, (original_size[0]*scale, original_size[1]*scale))
        self.sprites[name] = scaled

    def add_sprite(self, name: str, surface: pg.surface.Surface, scale=SPRITE_SCALE):
        s = surface.copy()
        original_size = s.get_size()
        s = pg.transform.scale(
            s, (original_size[0]*scale, original_size[1]*scale))
        self.sprites[name] = s

    def get_surface(self, name: str) -> pg.surface.Surface:
        """return the surface by name"""
        return self.sprites.get(name, pg.surface.Surface((SPRITE_SIZE*SPRITE_SCALE, SPRITE_SIZE*SPRITE_SCALE)))


class Spritesheets:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Spritesheets, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance
   # _shared_state: Dict[str, Spritesheet] = {}

    def __init__(self):
        # self.__dict__ = self._shared_state
        self.spritesheet = Spritesheet()
        self.spritesheet.load_from_json(
            "config/player.sprites.json")
        self.weapon_spritesheet = Spritesheet()
        self.weapon_spritesheet.load_from_json(
            "config/dungeon.sprites.json")
