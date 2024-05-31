from dataclasses import dataclass

from .block import Block
from .utils import AutoId


@dataclass
class Comment(AutoId, short_name="Comment"):
    block: Block
    x: int
    y: int
    width: int
    height: int
    minimized: bool
    text:str

    def as_tuple(self):
        return (self.item_id, {
          "blockId": self.block.item_id,
          "x": self.x,
          "y": self.y,
          "width": self.width,
          "height": self.height,
          "minimized": self.minimized,
          "text": self.text
        })
