from __future__ import annotations
from dataclasses import dataclass

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata
from apdev_mbta_data.ImmutableVector2 import ImmutableVector2

@dataclass(frozen=True)
class ImmutableLineMetadata(object):
    id:str
    primary_colour:str
    secondary_colour:str
    stops:tuple[ImmutableStopMetadata]
    line_anchors:tuple[ImmutableVector2]