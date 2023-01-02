import pygame as pg

from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE


class Spritesheet:

  def __init__(self, filename: str) -> None:
    self.spritesheet = pg.image.load(filename).convert_alpha()

  def get_player_surface(self) -> pg.surface.Surface:
    player_sprite = self.spritesheet.subsurface(
        (0, 0, SPRITE_SIZE, SPRITE_SIZE))
    original_size = player_sprite.get_size()

    player_sprite = pg.transform.scale(
        player_sprite, (original_size[0]*SPRITE_SCALE, original_size[1]*SPRITE_SCALE))
    return player_sprite
