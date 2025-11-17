import pygame 

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin
from apdev_led_visualiser.SoftwareLEDPinController import SoftwareLEDPinController

from apdev_led_visualiser.LEDVisualiser import LEDVisualiser

from GreenLinePinFactory import GreenLinePinFactory

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata
from apdev_mbta_data.APDevMBTADataReader import APDevMBTADataReader

def runVisualiserTest():
    reader = APDevMBTADataReader()
    lines:list[ImmutableLineMetadata] = reader.read_from_file("/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/example_file.json")

    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    canvas = LEDVisualiser()
    canvas.setScreenSize(SCREEN_WIDTH, SCREEN_HEIGHT, newIsFullscreen=False)

    factory = GreenLinePinFactory()
    pinsKeyedByStationID:dict[str, SoftwareLEDPin] = factory.createAllPins(
        lines[0].stops,
        pygame.Vector2(50,50),
        25
    )

    controllersKeyedByStationID:dict[str,SoftwareLEDPinController] = dict[str,SoftwareLEDPinController]()
    for key in pinsKeyedByStationID:
        controllersKeyedByStationID[key] = SoftwareLEDPinController(pinsKeyedByStationID[key])
        canvas.addLEDController(key, controllersKeyedByStationID[key])

    for pin in pinsKeyedByStationID.values():
        canvas.addToCanvas(pin)

    canvas.start()