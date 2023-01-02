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

        self.image: pg.surface.Surface = player_sprite
        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.look_dir: pg.math.Vector2 = pg.math.Vector2()


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


pg.init()
screen = pg.display.set_mode(SCREEN_SIZE)
clock = pg.time.Clock()

player = Player(50, 50)

running = True

dt = 0


def handle_input():
  keys = pg.key.get_pressed()  # recupero tutti i tasti premuti (List[bool])

  look_dir = pg.math.Vector2()

  if keys[pg.K_a]:
    look_dir.x = -1
  if keys[pg.K_s]:
    look_dir.y = 1
  if keys[pg.K_d]:
    look_dir.x = 1
  if keys[pg.K_w]:
    look_dir.y = -1

  
  player.look_dir = look_dir
  player.move(look_dir.x,look_dir.y)

while running:
    dt = clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    handle_input()

    screen.fill("black")

    # show sprite
    screen.blit(player.image, player.rect)
    
    pg.display.update()
    


pg.quit()
