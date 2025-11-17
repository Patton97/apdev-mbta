from __future__ import annotations
from dataclasses import dataclass

import json

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata
from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata
from apdev_mbta_data.LabelPlacement import LabelPlacement

class APDevMBTADataReader(object):
    def read_from_file(self:APDevMBTADataReader, file_path:str) -> list[ImmutableLineMetadata]:
        with open(file_path) as f:
            return self.read_from_json(json.load(f))

    def read_from_json(self:APDevMBTADataReader, json_obj:dict) -> list[ImmutableLineMetadata]:
        lines:list[ImmutableLineMetadata] = []

        for line_json_obj in json_obj["lines"]:
            lines.append(self.__parse_line_metadata(line_json_obj))

        return lines
    
    def __parse_line_metadata(self:APDevMBTADataReader, line_json_obj:dict) -> ImmutableLineMetadata:
        line_id:str = line_json_obj["line_id"]
        stops:list[ImmutableStopMetadata] = []

        for stop_json_obj in line_json_obj["stops"]:
            stops.append(self.__parse_stop_metadata(stop_json_obj))

        return ImmutableLineMetadata(line_json_obj["line_id"], stops)
    
    def __parse_stop_metadata(self:APDevMBTADataReader, stop_json_obj:dict) -> ImmutableStopMetadata:
        label_placement = LabelPlacement.__dict__.get(stop_json_obj.get("label_placement"))
        if label_placement is None:
            label_placement = LabelPlacement.CENTRE

        return ImmutableStopMetadata(
            stop_json_obj["stop_id"],
            stop_json_obj["name"],
            stop_json_obj["standardised_location_x"],
            stop_json_obj["standardised_location_y"],
            label_placement
        )