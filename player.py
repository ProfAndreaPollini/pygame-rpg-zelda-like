import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE
from spritesheet import Spritesheet


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # load sprite
        # player_spritesheet = pg.image.load(
        #     "assets/PixelMood4/Pixel Mood/Chars/Heros/Sprite sheet female hero.png").convert_alpha()

        # player_sprite = player_spritesheet.subsurface(
        #     (0, 0, SPRITE_SIZE, SPRITE_SIZE))
        # original_size = player_sprite.get_size()

        # player_sprite = pg.transform.scale(
        #     player_sprite, (original_size[0]*SPRITE_SCALE, original_size[1]*SPRITE_SCALE))

        self.spritesheet = Spritesheet(
            "assets/PixelMood4/Pixel Mood/Chars/Heros/Sprite sheet female hero.png")

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
