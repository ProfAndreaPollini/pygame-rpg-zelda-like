from dataclasses import dataclass
from math import floor
from typing import Dict, List, Optional
import typing
import pygame as pg
from player import Player

from settings import SPRITE_SIZE, SPRITE_SCALE
from spritesheet import Spritesheet
from pytmx import TiledMap, TiledTileLayer
from pytmx.util_pygame import load_pygame, pygame_image_loader

from utils import Direction


@dataclass
class Tile:
    name: str
    walkable: bool = True


class World:

    def __init__(self, config_filename: Optional[str] = None, tile_size=(SPRITE_SIZE, SPRITE_SIZE)) -> None:
        self.tiles: List[Tile] = []
        self.size = (0, 0)
        self.tile_size = tile_size
        self.spritesheet = Spritesheet()
        self.non_walkable_sprites: pg.sprite.Group = pg.sprite.Group()

        # ) if config_filename is None else Spritesheet(config_filename)
        if config_filename is not None:
            self.spritesheet.load_from_json(config_filename)

    def collide_vertical(self, player: Player, dt: float):
        desired_pos = player.get_desired_position(dt)
        desired_rect = player.rect.copy()
        #desired_rect.centerx += round(desired_pos.x)
        desired_rect.centery += round(desired_pos.y)
        desired_rect = player.get_desired_rect(
            dt)  # recupero dove voglio andare
        # is_moving_left = desired_rect.left < player.rect.left
        is_moving_up = desired_rect.top < player.rect.top

        tol = 5+64

        if player.dir.magnitude_squared() > 0:  # se non sono fermo
            collisions = pg.sprite.spritecollide(
                player, self.non_walkable_sprites, False)
            for sprite in collisions:
                assert sprite.rect is not None
                # if desired_rect.colliderect(sprite.rect):
                print(
                    f"{is_moving_up=} {desired_rect.left} {sprite.rect.right}")
                if abs(desired_rect.top - sprite.rect.bottom) < tol and is_moving_up:
                    print(
                        f"collision up! {abs(desired_rect.top - sprite.rect.bottom)}")
                    player.rect.top = sprite.rect.bottom
                    player.pos.y = player.rect.top
                    player.dir.y = 0
                if abs(desired_rect.bottom - sprite.rect.top) < tol and not is_moving_up:
                    print(
                        f"collision down! {abs(desired_rect.bottom - sprite.rect.top)}")
                    player.rect.bottom = sprite.rect.top
                    player.pos.y = player.rect.top
                    player.dir.y = 0

    def collide_horizontal(self, player: Player, dt: float):
        desired_pos = player.get_desired_position(dt)
        desired_rect = player.rect.copy()
        desired_rect.centerx += round(desired_pos.x)
        # desired_rect.centery += round(desired_pos.y)
        # desired_rect = player.get_desired_rect(
        #    dt)  # recupero dove voglio andare

        is_moving_left = desired_rect.left < player.rect.left
        is_moving_up = desired_rect.top < player.rect.top

        tol = 5+64

        if player.dir.magnitude_squared() > 0:  # se non sono fermo
            collisions = pg.sprite.spritecollide(
                player, self.non_walkable_sprites, False)
            for sprite in collisions:
                assert sprite.rect is not None
                # if desired_rect.colliderect(sprite.rect):
                print(
                    f"{is_moving_left=} {desired_rect.left} {sprite.rect.right}")
                if abs(desired_rect.left - sprite.rect.right) < tol and is_moving_left:
                    player.rect.left = sprite.rect.right
                    player.pos.x = player.rect.left 
                    player.dir.x = 0
                if abs(desired_rect.right - sprite.rect.left) < tol and not is_moving_left:
                    player.rect.right = sprite.rect.left
                    player.pos.x = player.rect.left
                    player.dir.x = 0

    # def collide_old(self, player: Player, dt: float):
    #     desired_rect = player.rect.copy()
    #     desired_rect.centerx += floor(player.v*dt*player.dir.x)
    #     desired_rect.centery += floor(player.v*dt*player.dir.y)

    #     if player.dir.magnitude_squared() > 0:
    #         # print(player.rect,desired_rect)
    #         for sprite in self.non_walkable_sprites.sprites():
    #             if desired_rect.colliderect(sprite.rect):
    #                 print(f"{player.dir=}")
    #                 if desired_rect.left < sprite.rect.right and player.look_dir == Direction.LEFT:
    #                     player.dir.x = (sprite.rect.right -
    #                                     desired_rect.left-0)/(player.v * dt)
    #                     player.dir.y = 0
    #                 elif desired_rect.right > sprite.rect.left and player.look_dir == Direction.RIGHT:
    #                     player.dir.x = (sprite.rect.left -
    #                                     desired_rect.right+0)/(player.v * dt)
    #                     player.dir.y = 0

    #                 if desired_rect.top < sprite.rect.bottom and player.look_dir == Direction.UP:
    #                     player.dir.y = (sprite.rect.bottom -
    #                                     desired_rect.top+0)/(player.v * dt)
    #                     player.dir.x = 0
    #                 elif desired_rect.bottom > sprite.rect.top and player.look_dir == Direction.DOWN:
    #                     player.dir.y = (sprite.rect.top -
    #                                     desired_rect.bottom-0)/(player.v * dt)
    #                     player.dir.x = 0
    #                 player.dir.x = min(max(player.dir.x, -1), 1)
    #                 player.dir.y = min(max(player.dir.y, -1), 1)
    #                 print(f"{desired_rect=}")
    #                 print(f"{sprite.rect=}")
    #                 print(f"{player.dir=}")
    #                 print("-"*80)

        # collisions = pg.sprite.spritecollide(player,self.non_walkable_sprites,False)
        # pg.sprite.g
        # if len(collisions) >0:
        #     print(collisions)
        #     c = collisions[0]
        #     if typing.TYPE_CHECKING:
        #         assert c is not None
        #         assert c.rect is not None

        #     dy = 0
        #     dx = 0

        #     if player.rect.left < c.rect.right:
        #         dx = -player.rect.left + c.rect.right
        #     elif player.rect.right < c.rect.left:
        #         dx = player.rect.right - c.rect.left

        #     if dx != 0:
        #         player.move(dx,0)

        #     if dx == 0:

        #         if player.rect.bottom > c.rect.top:
        #             dy = -player.rect.bottom + c.rect.top
        #         elif player.rect.top < c.rect.bottom:
        #             dy = -player.rect.top + c.rect.bottom

        #         if dy != 0:

        #             player.move(0,dy)

        #     print(f"{dx=} {dy=}")

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
            # print(f"{row=} {col=} {name=} {s=}")
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
        print(player_object.x, player_object.y)
        print(player_object.x*SPRITE_SCALE, player_object.y*SPRITE_SCALE)
        player.set(player_object.x*SPRITE_SCALE, player_object.y*SPRITE_SCALE)
        world = World()
        world.size = (terrain.height, terrain.width)
        gids = set()

        world.tiles = []
        for i in range((terrain.width * terrain.height)):
            world.tiles.append(Tile("0"))

        tile_colliders = list(tmxdata.get_tile_colliders())
        tile_colliders_gid = set(x[0] for x in tile_colliders)

        print(f"{tile_colliders}")
        print(f"{tile_colliders_gid}")
        for x, y, gid in terrain.iter_data():
            # print(x, y, gid)
            if gid > 0:
                # non_walkable_tiles.
                world.tiles[x + y * terrain.width].name = str(gid)
                # print(f"{gid=} {tile_colliders_gid=}")
                if gid in tile_colliders_gid:
                    sprite = pg.sprite.Sprite()
                    sprite.image = pg.surface.Surface((64, 64))
                    sprite.image.fill((255, 0, 0, 128))
                    sprite.rect = sprite.image.get_rect()
                    # assert sprite.rect is not None
                    sprite.rect.topleft = (
                        x*SPRITE_SIZE * SPRITE_SCALE, y*SPRITE_SIZE * SPRITE_SCALE)
                    world.non_walkable_sprites.add(sprite)

                # print(world.tiles[x + y * terrain.width].name)

            gids.add(gid)

        # print(gids)
        for gid in list(gids):
            s = tmxdata.get_tile_image_by_gid(gid)
            if s is not None:
                world.spritesheet.add_sprite(str(gid), s)
        # print(list(tmxdata.get_tile_colliders()))
        # for gid, collider in tmxdata.get_tile_colliders():
        #     print(gid, [x.as_points for x in collider])

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
