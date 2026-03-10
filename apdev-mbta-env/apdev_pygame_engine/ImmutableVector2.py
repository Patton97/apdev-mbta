from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutableVector2(object):
    x:int
    y:int