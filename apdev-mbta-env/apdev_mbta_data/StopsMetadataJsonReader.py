from __future__ import annotations

import json

from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

from apdev_pygame_engine.labels.LabelPlacement import LabelPlacement

class StopsMetadataJsonReader(object):
    def read_from_file(self:StopsMetadataJsonReader, file_path:str) -> list[ImmutableStopMetadata]:
        with open(file_path) as f:
            return self.read_from_json(json.load(f))

    def read_from_json(self:StopsMetadataJsonReader, json_obj:dict) -> list[ImmutableStopMetadata]:
        stops:list[ImmutableStopMetadata] = []

        for stop_json_obj in json_obj["stops"]:
            stops.append(self.__parse_stop_metadata(stop_json_obj))

        return stops
    
    def __parse_stop_metadata(self:StopsMetadataJsonReader, stop_json_obj:dict) -> ImmutableStopMetadata:
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