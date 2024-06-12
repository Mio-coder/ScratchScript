from dataclasses import dataclass
from typing import Optional

from PyScratch.utils import AutoId


@dataclass
class Asset(AutoId):
    asset_id: str
    "md5 hash of asset file"
    name: str
    asset_name: str
    data_format: str

    def to_dict(self) -> "dict[str, Any]":
        return {
            "assetId": self.asset_id,
            "name": self.name,
            "md5ext": self.asset_name,
            "dataFormat": self.data_format
        }

    def as_tuple(self):
        return self.item_id, self.to_dict()


@dataclass
class Costume(Asset):
    rotatation_center_x: int
    rotatation_center_y: int
    bitmap_resolution: Optional[int] = None

    def to_dict(self):
        result = super().to_dict()
        result["rotationCenterX"] = self.rotatation_center_x
        result["rotationCenterY"] = self.rotatation_center_y
        if self.bitmap_resolution is not None:
            result["bitmapResolution"] = self.bitmap_resolution
        return result


@dataclass
class Sound(Asset):
    rate: int
    "in Hz"
    sample_count: int

    def to_dict(self):
        result = super().to_dict()
        result["rate"] = self.rate
        result["sampleCount"] = self.sample_count
        return result
