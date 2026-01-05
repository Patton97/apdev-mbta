from __future__ import annotations
from dataclasses import dataclass

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

@dataclass(frozen=True)
class ImmutableLineMetadata(object):
    id:str
    stops:tuple[ImmutableStopMetadata]