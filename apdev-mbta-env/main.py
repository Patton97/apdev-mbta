import asyncio
import threading

import main_api

from apddev_mbta_api_wrapper.stops import ImmutableStop

# this has to be a minute otherwise we just get rejected by the API
# perhaps we can lower it if we lower the number of requests done in a single cache refresh
API_POLL_COOLDOWN_IN_SECONDS:int = 60

def __updatePins(stopsWithVehicles:list[ImmutableStop]):
    for pinController in main_hardware.getAllLEDPinControllers():
        pinController.set_is_lit(False)

    for stop in stopsWithVehicles:
        pinController = main_hardware.getLEDPinController(stop.id)

        if pinController is not None:
            pinController.set_is_lit(True)

async def __apiLoop():
    while True:
        await asyncio.sleep(API_POLL_COOLDOWN_IN_SECONDS)

        try:
            main_api.refreshCachedInfo()
        except:
            continue

        __updatePins([stop for _, stop in main_api.getCachedVehiclesAndCurrentStops()])
        

def __startApiLoop():
    asyncio.run(__apiLoop())

threading.Thread(target=__startApiLoop, daemon=True).start()

from apdev_mbta_data.APDevMBTADataReader import APDevMBTADataReader
from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata

reader = APDevMBTADataReader()
filePath:str = "/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/example_file.json"
lines:list[ImmutableLineMetadata] = reader.read_from_file(filePath)

# import main_visualiser
# main_visualiser.startVisualiser(lines)

import main_hardware
main_hardware.startPixels(lines)