from __future__ import annotations
from dataclasses import dataclass

from apdev_led_visualiser.LabelPlacement import LabelPlacement

@dataclass(frozen=True)
class ImmutableStopMetadata(object):
    id:str
    name:str
    standardised_location_x:int
    standardised_location_y:int
    label_placement:LabelPlacement
    primary_colour:str
    secondary_colour:str