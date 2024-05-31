from dataclasses import dataclass
from enum import StrEnum

from scratch_project.utils import from_dict

from .asset import Costume, Sound
from .block import Block
from .broadcast import Broadcast
from .comment import Comment
from .variable import ListVariable, Variable


@dataclass
class Target:
    is_stage: bool
    name: str
    variables: list[Variable]
    lists: list[ListVariable]
    broadcasts: list[Broadcast]
    blocks: list[Block]
    comments: list[Comment]
    current_costume: str
    costumes: list[Costume]
    sounds: list[Sound]
    volume: float

    def to_dict(self):
        return {
            "isStage": self.is_stage,
            "name": self.name,
            "variables": from_dict(self.variables),
            "lists": from_dict(self.lists),
            "broadcasts": from_dict(self.broadcasts),
            "blocks": from_dict(self.blocks),
            "comments": from_dict(self.comments),
            "currentCostume": self.current_costume,
            "costumes": from_dict(self.costumes),
            "sounds": from_dict(self.sounds),
            "volume": self.volume
        }


class VideoState(StrEnum):
    on = "on"
    off = "off"
    on_filpped = "on-flipped"


@dataclass
class Stage(Target):
    tempo: int
    "in BPM"
    viedo_state: VideoState
    video_transparency: int
    text_to_speech_languge: str

    def to_dict(self):
        result = super().to_dict()
        result["tempo"] = self.tempo
        result["videoState"] = self.viedo_state._value_
        result["videoTransparency"] = self.video_transparency
        result["textToSpeechLanguage"] = self.text_to_speech_languge
        return result


class RotationStyle(StrEnum):
    all_around = "all around"
    left_right = "left-right"
    no_rotation = "don't rotate"


@dataclass
class Sprite(Target):
    visible: bool
    x: int = 0
    y: int = 0
    size: int = 100
    "in %"
    direction: int = 90
    "clockwise from up in degrees"
    draggable: bool = False
    rotation_style: RotationStyle = RotationStyle.all_around

    def to_dict(self):
        result = super().to_dict()
        result["visible"] = self.visible
        result["x"] = self.x
        result["y"] = self.y
        result["size"] = self.size
        result["direction"] = self.direction
        result["draggable"] = self.draggable
        result["rotationStyle"] = self.rotation_style._value_
        return result
