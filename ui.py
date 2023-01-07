import pygame as pg


class UI:

  def __init__(self, player):
    self.player = player
    self.surface = pg.display.get_surface()
    self.font = pg.font.Font(None, 36)
    # Render the text to a surface

  def draw(self):
    text_surface = self.font.render(
        f"({self.player.pos.x},{self.player.pos.y})", True, (255, 255, 255))

    # Draw the text to the screen
    self.surface.blit(text_surface, (100, 100))
