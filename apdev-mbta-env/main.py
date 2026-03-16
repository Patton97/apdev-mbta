import asyncio
import threading

import main_visualiser

from apddev_mbta_api_wrapper.stops import ImmutableStop

API_POLL_COOLDOWN_IN_SECONDS:int = 10

def __updatePins(stopsWithVehicles:list[ImmutableStop]):
    for pinController in main_visualiser.getAllLEDPinControllers():
        pinController.set_is_lit(False)

    for stop in stopsWithVehicles:
        pinController = main_visualiser.getLEDPinController(stop.id)

        if pinController is not None:
            pinController.set_is_lit(True)

async def __apiLoop():
    while True:
        main_api.refreshCachedInfo()
        __updatePins([stop for _, stop in main_api.getCachedVehiclesAndCurrentStops()])
        await asyncio.sleep(API_POLL_COOLDOWN_IN_SECONDS)

def __startApiLoop():
    asyncio.run(__apiLoop())
    
import main_api

threading.Thread(target=__startApiLoop, daemon=True).start()

from apdev_mbta_data.APDevMBTADataReader import APDevMBTADataReader
from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata

reader = APDevMBTADataReader()
filePath:str = "/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/example_file.json"
lines:list[ImmutableLineMetadata] = reader.read_from_file(filePath)
main_visualiser.startVisualiser(lines)