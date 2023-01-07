from typing import Tuple
import pygame as pg


class Camera(pg.sprite.Group):
    def __init__(self, player, screen_width, screen_height):
        super().__init__()
        self.player = player
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.old_center = self.player.rect.center

    def world_to_screen(self, pos: Tuple[int, int]):
        return (pos[0]-self.camera.x, pos[1]-self.camera.y)

    @property
    def x(self):
        return self.camera.x

    @property
    def y(self):
        return self.camera.y

    def update(self):
        # Center the camera on the player
        self.center(self.player.rect.center)

    def center(self, center):
        center_x = center[0]
        center_y = center[1]
        # print(abs((center[0] -self.old_center[0])**2  - (self.old_center[1] - center[1])**2))
        if abs((center[0] - self.old_center[0])**2 - (self.old_center[1] - center[1])**2) > 100:
            # Keep the center of the camera within the boundaries of the game world
            # max(center[0], self.screen_width // 2)
            center_x = 0.5*center[0] + 0.5*self.old_center[0]
            # center_x = min(center_x, self.player.image.width -
            #    self.screen_width // 2)
            # max(center[1], self.screen_height // 2)
            center_y = 0.5*center[1] + 0.5*self.old_center[1]
            # center_y = min(center_y, self.player.image.height -
            #    self.screen_height // 2)
            self.old_center = center
        self.camera = pg.rect.Rect(center_x - self.screen_width // 2, center_y -
                                   self.screen_height // 2, self.screen_width, self.screen_height)
