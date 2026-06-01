import board
import neopixel
from time import sleep

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata

from apdev_led.ILEDPinController import ILEDPinController

from apdev_led_neopixel.NeoPixelLEDPinFactory import NeoPixelLEDPinFactory
from apdev_led_neopixel.NeoPixelLEDPin import NeoPixelLEDPin
from apdev_led_neopixel.NeoPixelLEDPinController import NeoPixelLEDPinController

NUM_PIXELS = 50
BRIGHTNESS = 0.05
GPIO_DATA_PIN = board.D21

__strip:neopixel.NeoPixel = neopixel.NeoPixel(GPIO_DATA_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False, pixel_order=neopixel.RGB)
__pins:list[NeoPixelLEDPin] = []
__controllersKeyedByStopID:dict[str, ILEDPinController] = {}

def startPixels(lines:list[ImmutableLineMetadata]):
    for i in range(len(lines)):
        __addPinsForStops(lines[i], __strip)

    global __pins
    while True:
        for pin in __pins:
            if pin.getIsFlashing():
                pin._isLit = not pin._isLit
            else:
                pin._isLit = False
            pin.renderTick()
        __strip.show()
        sleep(0.5)

def getAllLEDPinControllers():
    global __controllersKeyedByStopID
    return __controllersKeyedByStopID.values()

def getLEDPinController(stopID:str) -> ILEDPinController:
    global __controllersKeyedByStopID
    return __controllersKeyedByStopID.get(stopID, None)

def __addPinsForStops(lineMetadata:ImmutableLineMetadata, strip:neopixel.NeoPixel):
    pinFactory = NeoPixelLEDPinFactory()
    pinsKeyedByStationID:dict[str, NeoPixelLEDPin] = pinFactory.createAllPins(
        lineMetadata.stops,
        strip
    )

    for id, pin in pinsKeyedByStationID.items():
        global __controllersKeyedByStopID
        __controllersKeyedByStopID[id] = NeoPixelLEDPinController(pin)
        __controllersKeyedByStopID[id].set_is_lit(True)
        __pins.append(pin)