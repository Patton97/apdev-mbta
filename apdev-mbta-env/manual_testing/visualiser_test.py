from apdev_mbta_data.LinesMetadataJsonReader import APDevMBTADataReader
from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata

import main_visualiser

def runVisualiserTest():
    reader = APDevMBTADataReader()
    filePath:str = "/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/example_file.json"
    lines:list[ImmutableLineMetadata] = reader.read_from_file(filePath)
    main_visualiser.startVisualiser(lines)