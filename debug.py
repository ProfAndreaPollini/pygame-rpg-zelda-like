import pygame as pg
from typing import Tuple

from camera import Camera


class DebugLayer:

  def __init__(self, camera: Camera):
    self.camera = camera
    self.screen = pg.display.get_surface()

  def draw_rect_outline(self, rect: pg.rect.Rect, color: Tuple[int, int, int] = (0, 0, 255), width: int = 2):
    rect.left -= self.camera.x
    rect.top -= self.camera.y
    # print(desired_rect)
    pg.draw.rect(self.screen, color, rect, width)

  def draw_surface(self, surface: pg.surface.Surface, rect: pg.rect.Rect):
    self.screen.blit(surface, rect.copy(
    ).move(-self.camera.x, -self.camera.y))
