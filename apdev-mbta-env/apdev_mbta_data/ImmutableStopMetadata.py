from __future__ import annotations
from dataclasses import dataclass

from enum import Enum

from apdev_mbta_data.LabelPlacement import LabelPlacement

@dataclass(frozen=True)
class ImmutableStopMetadata(object):
    id:str
    name:str
    standardised_location_x:int
    standardised_location_y:int
    label_placement:LabelPlacement