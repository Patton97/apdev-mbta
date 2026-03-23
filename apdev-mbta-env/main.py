import asyncio
import threading

import main_visualiser

from apddev_mbta_api_wrapper.stops import ImmutableStop
from apddev_mbta_api_wrapper.vehicles import ImmutableVehicle

from apdev_mbta_data.LinesMetadataJsonReader import LinesMetadataJsonReader
from apdev_mbta_data.StopsMetadataJsonReader import StopsMetadataJsonReader

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata
from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

API_POLL_COOLDOWN_IN_SECONDS:int = 10

lineMetadataKeyedByRouteId:dict[str, ImmutableLineMetadata] = {}

def __updatePins(stopsWithVehicles:list[tuple[ImmutableVehicle, ImmutableStop]]):
    for pinController in main_visualiser.getAllLEDPinControllers():
        pinController.set_is_lit(False)

    coloursToSetByStopId:dict[str,list[str]] = {}
    for vehicle, stop in stopsWithVehicles:
        coloursToSet = coloursToSetByStopId.get(stop.id, None)
        if coloursToSet is None:
            coloursToSet = coloursToSetByStopId[stop.id] = []
    
        global lineMetadataKeyedByRouteId
        lineMetadata = lineMetadataKeyedByRouteId.get(vehicle.route_id, None)
        if lineMetadata is not None:
            coloursToSet.append(lineMetadata.primary_colour)

    for stopId, coloursToSet in coloursToSetByStopId.items():
        pinController = main_visualiser.getLEDPinController(stopId)
        if pinController is not None:
            pinController.set_is_lit(True)
            pinController.set_colours(coloursToSet)

async def __apiLoop():
    while True:
        main_api.refreshCachedInfo()
        __updatePins(main_api.getCachedVehiclesAndCurrentStops())
        await asyncio.sleep(API_POLL_COOLDOWN_IN_SECONDS)

def __startApiLoop():
    asyncio.run(__apiLoop())
    
import main_api

threading.Thread(target=__startApiLoop, daemon=True).start()

metadataFolder:str = "/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/"

reader = LinesMetadataJsonReader()
linesFilePath:str = metadataFolder + "lines.json"
lines:list[ImmutableLineMetadata] = reader.read_from_file(linesFilePath)
for line in lines:
    lineMetadataKeyedByRouteId[line.id] = line

reader = StopsMetadataJsonReader()
stopsFilePath:str = metadataFolder + "green-D-stops.json"
stops:list[ImmutableStopMetadata] = reader.read_from_file(stopsFilePath)

main_visualiser.startVisualiser(lines, stops)