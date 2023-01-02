import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE
from spritesheet import Spritesheet


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.spritesheet = Spritesheet("config/player.sprites.json")

        self.image: pg.surface.Surface = self.spritesheet.get_player_surface()
        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos: pg.math.Vector2 = pg.math.Vector2(x, y)
        self.look_dir: pg.math.Vector2 = pg.math.Vector2()

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
