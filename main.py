import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # load sprite
        player_spritesheet = pg.image.load(
            "assets/PixelMood4/Pixel Mood/Chars/Heros/Sprite sheet female hero.png").convert_alpha()

        player_sprite = player_spritesheet.subsurface((0, 0, 16, 16))
        original_size = player_sprite.get_size()

        player_sprite = pg.transform.scale(
            player_sprite, (original_size[0]*SPRITE_SCALE, original_size[1]*SPRITE_SCALE))

        self.image : pg.surface.Surface = player_sprite
        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

player = Player(50, 50)

running = True


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("black")

    

    # show sprite
    screen.blit(player.image, player.rect)

    pg.display.flip()


pg.quit()
