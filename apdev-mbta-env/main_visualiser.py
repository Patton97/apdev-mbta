import pygame 

from apdev_led_visualiser.LEDVisualiser import LEDVisualiser

from apdev_led.ILEDPinController import ILEDPinController

from apdev_led_visualiser.LEDPinController import LEDPinController
from apdev_led_visualiser.LEDLineFactory import LEDLineFactory
from apdev_led_visualiser.LEDPinDecorator import LEDPinDecorator, ImmutableLEDPinDecoratorConfig
from apdev_led_visualiser.LEDLineDecorator import LEDLineDecorator, ImmutableLEDLineDecoratorConfig
from apdev_led_visualiser.LEDPin import LEDPin
from apdev_led_visualiser.LEDLine import LEDLine
from apdev_led_visualiser.FlashingPinAnimFactory import FlashingPinAnimFactory

from apdev_led_visualiser_mbta.StopLEDPinFactory import StopLEDPinFactory

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_MARGIN = pygame.Vector2(50, 50)
GRID_SCALE = 25

LED_PIN_ON_RADIUS = 10
LED_PIN_OFF_RADIUS = 8

LED_OFF_COLOUR = 'black'

LED_PIN_FLASH_ANIM_OFF_TIME_IN_MILLISECONDS = 1000
LED_PIN_FLASH_ANIM_ON_TIME_IN_MILLISECONDS = 2000

__visualiser:LEDVisualiser
__controllersKeyedByStopID:dict[str, ILEDPinController] = {}

def startVisualiser(lines:list[ImmutableLineMetadata]):
    pygame.init()

    global __visualiser
    __visualiser = LEDVisualiser()
    __visualiser.setScreenSize(SCREEN_WIDTH, SCREEN_HEIGHT, newIsFullscreen=False)

    for i in range(len(lines)):
        __addSceneObjectsForLine(lines[i], __visualiser)

    __visualiser.start()

def getAllLEDPinControllers() -> list[ILEDPinController]:
    global __controllersKeyedByStopID
    return __controllersKeyedByStopID.values()

def getLEDPinController(stopID:str) -> ILEDPinController:
    global __controllersKeyedByStopID
    return __controllersKeyedByStopID.get(stopID, None)

def stopVisualiser():
    __visualiser.stop()

def __addSceneObjectsForLine(lineMetadata:ImmutableLineMetadata, visualiser:LEDVisualiser):
    __addSplinesForLine(lineMetadata, visualiser)
    __addPinsForStops(lineMetadata, visualiser)

def __addSplinesForLine(lineMetadata:ImmutableLineMetadata, visualiser:LEDVisualiser):
    factory = LEDLineFactory()
    lines:list[LEDLine] = factory.createAllLines(lineMetadata.line_anchors, GRID_SCALE)
    
    decoratorConfig = ImmutableLEDLineDecoratorConfig(lineMetadata.secondary_colour)
    decorator = LEDLineDecorator(decoratorConfig)
    decorator.decorateAll(lines)

    for line in lines:
        visualiser.addToCanvas(line)

def __addPinsForStops(lineMetadata:ImmutableLineMetadata, visualiser:LEDVisualiser):
    pinFactory = StopLEDPinFactory()
    pinsKeyedByStationID:dict[str, LEDPin] = pinFactory.createAllPins(
        lineMetadata.stops,
        GRID_SCALE
    )

    pinDecorator = LEDPinDecorator()
    flashingAnimComponentFactory = FlashingPinAnimFactory(
        LED_PIN_FLASH_ANIM_OFF_TIME_IN_MILLISECONDS,
        LED_PIN_FLASH_ANIM_ON_TIME_IN_MILLISECONDS
    )
    for stop in lineMetadata.stops:
        pin = pinsKeyedByStationID[stop.id]

        global __controllersKeyedByStopID
        __controllersKeyedByStopID[stop.id] = LEDPinController(pin)
        decoratorConfig = ImmutableLEDPinDecoratorConfig(
            lineMetadata.primary_colour,
            LED_OFF_COLOUR,
            LED_PIN_ON_RADIUS,
            LED_PIN_OFF_RADIUS,
            flashingAnimComponentFactory,
            stop.label_placement,
            stop.name
        )
        pinDecorator.decorate(pin, decoratorConfig)

    for pin in pinsKeyedByStationID.values():
        visualiser.addToCanvas(pin)