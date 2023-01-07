from enum import Enum
import pygame as pg
from settings import SCREEN_SIZE, SPRITE_SCALE, SPRITE_SIZE
from spritesheet import Spritesheet, Spritesheets
from utils import Direction
from weapons.sword import Sword


class PlayerStatus(Enum):
    IDLE = "idle"
    WALK = "walk"
    ATTACK = "attack"


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        s = Spritesheets()

        self.spritesheet = s.spritesheet
        self.weapon_spritesheet = s.weapon_spritesheet
        # self.spritesheet = Spritesheet()
        # self.spritesheet.load_from_json("config/player.sprites.json")
        # self.weapon_spritesheet = Spritesheet()
        # self.weapon_spritesheet.load_from_json("config/dungeon.sprites.json")
        self.image: pg.surface.Surface = self.spritesheet.get_surface(
            "idle_up")
        self.rect: pg.rect.Rect = self.image.get_rect()
        self.rect = self.rect.inflate(0.8, 0.8)
        self.rect.left = x
        self.rect.top = y
        self.pos: pg.math.Vector2 = pg.math.Vector2(x, y)
        self.look_dir: Direction = Direction.UP
        self.dir: pg.math.Vector2 = pg.math.Vector2()
        self.v: float = 1.0
        self.status: PlayerStatus = PlayerStatus.IDLE
        # self.sword_image = self.weapon_spritesheet.get_surface("sword")
        # self.sword_rect = self.sword_image.get_rect()
        # self.sword_rect.left = x + 10
        # self.sword_rect.top = y + 10
        self.weapon = Sword()
        self.weapon.add(self.groups())
        self.weapon.x = x+10
        self.weapon.y = y+10
        self.attacking = False
        # animations
        # self.movement_animations = {
        #     "walk_up": self.spritesheet.animations["walk_up"],
        #     "walk_down": self.spritesheet.animations["walk_down"],
        #     "walk_left": self.spritesheet.animations["walk_left"],
        #     "walk_right": self.spritesheet.animations["walk_right"]
        # }
        self.animations = {
            "movement": None
        }

        self.timers = {}

    @property
    def status_name(self):
        return f"{self.status.value}_{self.look_dir.value}"

    def update_direction(self):
        old_look_dir = self.look_dir
        if self.dir.x == 1:
            self.look_dir = Direction.RIGHT
        elif self.dir.x == -1:
            self.look_dir = Direction.LEFT
        elif self.dir.y == -1:
            self.look_dir = Direction.UP
        elif self.dir.y == 1:
            self.look_dir = Direction.DOWN
        return old_look_dir != self.look_dir

    def get_desired_position(self, dt) -> pg.math.Vector2:

        ret = pg.math.Vector2()
        ret.x += self.dir.x * self.v * dt
        ret.y += self.dir.y * self.v * dt
        if ret.x != 0 and ret.y != 0:
            print(self.dir, ret.x, ret.y)
        return ret

    def get_desired_rect(self, dt) -> pg.rect.Rect:
        desired_pos = self.get_desired_position(dt)
        desired_rect = self.rect.copy()
        desired_rect.left += round(desired_pos.x)
        desired_rect.top += round(desired_pos.y)
        return desired_rect

    def move(self, dx, dy, dt):

        self.pos.x += dx * self.v * dt
        self.pos.y += dy * self.v * dt
        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

    def update_x(self, dt):
        self.pos.x += self.dir.x * self.v * dt
        # self.pos.y += dy * self.v * dt
        self.rect.left = self.pos.x
        # self.rect.centery = self.pos.y

    def update_y(self, dt):
        # self.pos.x += dx * self.v * dt
        self.pos.y += self.dir.y * self.v * dt
        # self.rect.centerx = self.pos.x
        self.rect.top = self.pos.y

    def set(self, x, y):
        self.pos.x = x
        self.pos.y = y
        self.rect.left = self.pos.x
        self.rect.top = self.pos.y

    def update_timers(self, dt):
        for timer in self.timers:
            self.timers[timer] -= dt

        for timer in list(self.timers.keys()):
            if self.timers[timer] <= 0:
                getattr(self, f"on_{timer}_timer_expire")()
                del self.timers[timer]

    def on_attack_timer_expire(self):
        print("Attacco finito")
        self.attacking = False

    def update(self, dt: float):
        self.update_animations(dt)
        if not self.attacking:
            self.update_position(dt)
            dx, dy = 0, 0
            match self.look_dir:
                case Direction.UP: dy = -(self.rect.h//2+20)
                case Direction.DOWN: dy = self.rect.h//2+20
                case Direction.LEFT: dx = -(20+self.rect.w//2)
                case Direction.RIGHT: dx = 20+self.rect.w//2
            self.weapon.set(self.pos.x + dx, self.pos.y + dy)
        self.update_timers(dt)


    def attack(self):
        # self.status = PlayerStatus.ATTACK
        if not self.attacking:
            self.timers["attack"] = 200
            print("attack start")
            self.attacking = True

    def update_position(self, dt: float):
        if self.dir.magnitude_squared() > 0:
            if self.status == PlayerStatus.IDLE:
                self.status = PlayerStatus.WALK
                # self.move(self.dir.x, self.dir.y, dt)
                changed_dir = self.update_direction()
                # type: ignore
                self.animations["movement"] = self.spritesheet.animations[self.status_name]
                self.animations["movement"].reset()
            else:
                # self.move(self.dir.x, self.dir.y, dt)
                changed_dir = self.update_direction()
                if changed_dir:
                    self.animations["movement"] = self.spritesheet.animations[self.status_name]

            movement_animation = self.animations["movement"]
            if movement_animation:
                sprite_name = movement_animation()
                # print(f"{sprite_name=}")
                self.image = self.spritesheet.get_surface(sprite_name)
        else:
            self.status = PlayerStatus.IDLE
            self.image = self.spritesheet.get_surface(
                "idle_" + self.look_dir.value)

    def update_animations(self, dt: float):
        for name, animation in self.animations.items():
            if animation is None:
                continue
            animation.update(dt)
