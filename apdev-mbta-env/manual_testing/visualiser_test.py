import pygame 

from apdev_led_visualiser.LEDVisualiser import LEDVisualiser

from apdev_led_visualiser_mbta.StopLEDPinFactory import StopLEDPinFactory
from apdev_led_visualiser.LEDLineFactory import LEDLineFactory
from apdev_led_visualiser.LEDPinDecorator import LEDPinDecorator, ImmutableLEDPinDecoratorConfig
from apdev_led_visualiser.LEDLineDecorator import LEDLineDecorator, ImmutableLEDLineDecoratorConfig
from apdev_led_visualiser.LEDPin import LEDPin
from apdev_led_visualiser.LEDPinController import LEDPinController
from apdev_led_visualiser.LEDLine import LEDLine
from apdev_led_visualiser.FlashingPinAnimFactory import FlashingPinAnimFactory

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata
from apdev_mbta_data.APDevMBTADataReader import APDevMBTADataReader

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_MARGIN = pygame.Vector2(50, 50)
GRID_SCALE = 25

LED_PIN_ON_RADIUS = 10
LED_PIN_OFF_RADIUS = 8

LED_OFF_COLOUR = 'black'

LED_PIN_FLASH_ANIM_OFF_TIME_IN_MILLISECONDS = 1000
LED_PIN_FLASH_ANIM_ON_TIME_IN_MILLISECONDS = 2000

def runVisualiserTest():
    canvas = LEDVisualiser()
    canvas.setScreenSize(SCREEN_WIDTH, SCREEN_HEIGHT, newIsFullscreen=False)

    reader = APDevMBTADataReader()
    lines:list[ImmutableLineMetadata] = reader.read_from_file("/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/example_file.json") 

    for i in range(len(lines)):
        __addSceneObjectsForLine(lines[i], canvas)

    canvas.start()

def __addSceneObjectsForLine(lineMetadata:ImmutableLineMetadata, canvas:LEDVisualiser):
    __addSplinesForLine(lineMetadata, canvas)
    __addPinsForStops(lineMetadata,canvas)

def __addSplinesForLine(lineMetadata:ImmutableLineMetadata, canvas:LEDVisualiser):
    factory = LEDLineFactory()
    lines:list[LEDLine] = factory.createAllLines(lineMetadata.line_anchors, GRID_SCALE)
    
    decoratorConfig = ImmutableLEDLineDecoratorConfig(lineMetadata.secondary_colour)
    decorator = LEDLineDecorator(decoratorConfig)
    decorator.decorateAll(lines)

    for line in lines:
        canvas.addToCanvas(line)

def __addPinsForStops(lineMetadata:ImmutableLineMetadata, canvas:LEDVisualiser):
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
        canvas.addToCanvas(pin)