from __future__ import annotations

import json

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata

from apdev_pygame_engine.ImmutableVector2 import ImmutableVector2

class LinesMetadataJsonReader(object):
    def read_from_file(self:LinesMetadataJsonReader, file_path:str) -> list[ImmutableLineMetadata]:
        with open(file_path) as f:
            return self.read_from_json(json.load(f))

    def read_from_json(self:LinesMetadataJsonReader, json_obj:dict) -> list[ImmutableLineMetadata]:
        lines:list[ImmutableLineMetadata] = []

        for line_json_obj in json_obj["lines"]:
            lines.append(self.__parse_line_metadata(line_json_obj))

        return lines
    
    def __parse_line_metadata(self:LinesMetadataJsonReader, line_json_obj:dict) -> ImmutableLineMetadata:
        line_id:str = line_json_obj["line_id"]

        primary_colour = line_json_obj["primary_colour"]
        secondary_colour = line_json_obj["secondary_colour"]

        line_anchors:list[ImmutableVector2] = []
        for line_anchor in  line_json_obj["line_anchors"]:
            line_anchors.append(ImmutableVector2(line_anchor["x"], line_anchor["y"]))

        return ImmutableLineMetadata(line_id, primary_colour, secondary_colour, line_anchors)