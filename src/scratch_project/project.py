from dataclasses import dataclass

from .extension import Extension
from .meta import Meta
from .monitor import Monitor
from .target import Target


@dataclass
class Project:
    targets: list[Target]
    monitors: list[Monitor]
    extensions: list[Extension]
    meta: Meta

    def to_dict(self):
        return {
            "targets": [target.to_dict() for target in self.targets],
            "monitors": [monitor.to_dict() for monitor in self.monitors],
            "extensions":
                [extension.to_dict() for extension in self.extensions],
            "meta": self.meta.to_dict()
        }
