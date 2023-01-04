

from typing import List


class Animation:
  def __init__(self, name: str, sprite_names: List[str], length_ms: float, loop: bool = True, autostart: bool = True) -> None:
    self.name = name
    self.sprite_names = sprite_names
    self.length_ms = length_ms
    self.loop = loop

    self.reset()
    self.active = autostart

  def reset(self):
    "reset the animation"
    self.current = 0
    self.t = 0

  def start(self):
    self.active = True

  def update(self, dt: float):
    if not self.active:
      return

    self.t += dt

    if self.t > self.length_ms:
      if not self.loop:
        self.active = False
      else:
        self.t = 0

    self.current = (self.t/self.length_ms) * len(self.sprite_names)
