from __future__ import annotations

from apdev_mbta_data.ImmutableVector2 import ImmutableVector2

from apdev_led_visualiser.SoftwareLEDLine import SoftwareLEDLine

class SoftwareLEDLineFactory(object):
    def createAllLines(self:SoftwareLEDLineFactory, line_anchors:tuple[ImmutableVector2], grid_scale:int):
        lines:list[SoftwareLEDLine] = []
        
        lineAnchorCount = len(line_anchors)
        for i in range(lineAnchorCount):
            if (i+1 >= lineAnchorCount):
                break
            ledLine = SoftwareLEDLine()
            lines.append(ledLine)
            ledLine.gridStartPosition = line_anchors[i]
            ledLine.gridEndPosition = line_anchors[i+1]
            ledLine.gridScale = grid_scale
        return lines