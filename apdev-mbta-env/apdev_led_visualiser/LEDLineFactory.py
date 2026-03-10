from __future__ import annotations

from .ImmutableVector2 import ImmutableVector2

from .LEDLine import LEDLine

class LEDLineFactory(object):
    def createAllLines(self:LEDLineFactory, line_anchors:tuple[ImmutableVector2], grid_scale:int):
        lines:list[LEDLine] = []
        
        lineAnchorCount = len(line_anchors)
        for i in range(lineAnchorCount):
            if (i+1 >= lineAnchorCount):
                break
            ledLine = LEDLine()
            lines.append(ledLine)
            ledLine.setGridStartPosition(line_anchors[i])
            ledLine.setGridEndPosition(line_anchors[i+1])
            ledLine.setGridScale(grid_scale)
        return lines