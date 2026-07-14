import asyncio
import threading

import main_api
import main_visualiser

from apddev_mbta_api_wrapper.stops import ImmutableStop
from apddev_mbta_api_wrapper.vehicles import ImmutableVehicle

from apdev_mbta_data.LinesMetadataJsonReader import LinesMetadataJsonReader
from apdev_mbta_data.StopsMetadataJsonReader import StopsMetadataJsonReader

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata
from apdev_mbta_data.ImmutableStopMetadata import ImmutableStopMetadata

# this has to be a minute otherwise we just get rejected by the API
# perhaps we can lower it if we lower the number of requests done in a single cache refresh
API_POLL_COOLDOWN_IN_SECONDS:int = 60

lineMetadataKeyedByRouteId:dict[str, ImmutableLineMetadata] = {}
__allPossibleColoursSorted = []

def __updatePins(vehiclesAndCurrentStops:list[tuple[ImmutableVehicle, ImmutableStop]]):
    for pinController in main_visualiser.getAllLEDPinControllers():
        pinController.set_is_lit(False)

    coloursToSetByStopId:dict[str,list[str]] = {}
    for vehicle, stop in vehiclesAndCurrentStops:
        if stop is None:
            continue

        coloursToSet = coloursToSetByStopId.get(stop.id, None)
        if coloursToSet is None:
            coloursToSet = coloursToSetByStopId[stop.id] = []
    
        global lineMetadataKeyedByRouteId
        lineMetadata = lineMetadataKeyedByRouteId.get(vehicle.route_id, None)
        if lineMetadata is not None:
            coloursToSet.append(lineMetadata.primary_colour)

    for stopId, coloursToSet in coloursToSetByStopId.items():
        # ensure all stops show colours in a consistent order
        global __allPossibleColoursSorted
        coloursToSet = sorted(coloursToSet, key = __allPossibleColoursSorted.index)

        pinController = main_visualiser.getLEDPinController(stopId)
        if pinController is not None:
            pinController.set_is_lit(True)
            pinController.set_colours(coloursToSet)

async def __apiLoop():
    while True:
        main_api.refreshCachedInfo()
        __updatePins(main_api.getCachedVehiclesAndCurrentStops())
        await asyncio.sleep(API_POLL_COOLDOWN_IN_SECONDS)

        try:
            main_api.refreshCachedInfo()
        except:
            continue

        __updatePins([stop for _, stop in main_api.getCachedVehiclesAndCurrentStops()])
        

def __startApiLoop():
    asyncio.run(__apiLoop())

threading.Thread(target=__startApiLoop, daemon=True).start()

# TODO AP: Make this an arg/envvar/something
metadataFolder:str = "/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/"

reader = LinesMetadataJsonReader()
linesFilePath:str = metadataFolder + "lines.json"
lines:list[ImmutableLineMetadata] = reader.read_from_file(linesFilePath)

for line in lines:
    lineMetadataKeyedByRouteId[line.id] = line
    __allPossibleColoursSorted.append(line.primary_colour)

reader = StopsMetadataJsonReader()
stopsFilePath:str = metadataFolder + "stops.json"
stops:list[ImmutableStopMetadata] = reader.read_from_file(stopsFilePath)

main_visualiser.startVisualiser(lines, stops)
