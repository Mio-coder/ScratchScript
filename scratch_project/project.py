from dataclasses import dataclass

from .meta import Meta
from .monitor import Monitor
from .target import Target


@dataclass
class Project:
    targets: list[Target]
    monitors: list[Monitor]
    extensions: list[str]
    meta: Meta

    def to_dict(self):
        return {
            "targets": [target.to_dict() for target in self.targets],
            "monitors": [monitor.to_dict() for monitor in self.monitors],
            "extensions": self.extensions,
            "meta": self.meta.to_dict()
        }
