from enum import StrEnum
from typing import Optional, Any

from PyScratch.utils import AutoId


class MonitorMode(StrEnum):
    deafult = "deafult"
    large = "large"
    slider = "slider"
    list = "list"


class Monitor(AutoId):
    mode: MonitorMode
    opcode: str
    params: dict[str, str]
    sprite_name: str
    value: Any
    width: int
    height: int
    x: int
    y: int
    visible: bool
    slider_min: Optional[int]
    slider_max: Optional[int]
    is_discrete: Optional[int]

    def to_dict(self):
        result = {
            "id": self.item_id,
            "mode": self.mode._value_,
            "opcode": self.opcode,
            "params": self.params,
            "spriteName": self.sprite_name,
            "value": self.value,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "visible": self.visible,
        }
        if self.mode != MonitorMode.list:
            result["sliderMin"] = self.slider_min
            result["sliderMax"] = self.slider_max
            result["isDiscrete"] = self.is_discrete
        return result
