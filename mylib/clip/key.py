from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import List

from pure_protobuf.dataclasses_ import message, field


@message
@dataclass
class ClipKey:
    video_ids: List[int] = field(1, default_factory=list)
    annotation_ids: List[int] = field(2, default_factory=list)

    def serialize(self) -> str:
        return base64.b64encode(self.dumps()).decode('utf-8')

    @staticmethod
    def deserialize(s: str) -> ClipKey:
        return ClipKey.loads(base64.b64decode(s))
