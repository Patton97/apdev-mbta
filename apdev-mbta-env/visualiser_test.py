import pygame 

from apdev_led_visualiser.LEDVisualiser import LEDVisualiser
from apdev_led_visualiser.SoftwareLEDPinFactory import SoftwareLEDPinFactory
from apdev_led_visualiser.SoftwareLEDLineFactory import SoftwareLEDLineFactory
from apdev_led_visualiser.SoftwareLEDPinDecorator import SoftwareLEDPinDecorator, ImmutableSoftwareLEDPinDecoratorConfig
from apdev_led_visualiser.SoftwareLEDLineDecorator import SoftwareLEDLineDecorator, ImmutableSoftwareLEDLineDecoratorConfig
from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin
from apdev_led_visualiser.SoftwareLEDPinController import SoftwareLEDPinController
from apdev_led_visualiser.SoftwareLEDLine import SoftwareLEDLine

from apdev_mbta_data.ImmutableLineMetadata import ImmutableLineMetadata
from apdev_mbta_data.APDevMBTADataReader import APDevMBTADataReader

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_MARGIN = pygame.Vector2(50, 50)
GRID_SCALE = 25

LED_PIN_ON_RADIUS = 10
LED_PIN_OFF_RADIUS = 8

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
    factory = SoftwareLEDLineFactory()
    lines:list[SoftwareLEDLine] = factory.createAllLines(lineMetadata.line_anchors, GRID_SCALE)
    
    decoratorConfig = ImmutableSoftwareLEDLineDecoratorConfig(lineMetadata.secondary_colour)
    decorator = SoftwareLEDLineDecorator(decoratorConfig)
    decorator.decorateAll(lines)

    for line in lines:
        canvas.addToCanvas(line)

def __addPinsForStops(lineMetadata:ImmutableLineMetadata, canvas:LEDVisualiser):
    pinFactory = SoftwareLEDPinFactory()
    pinsKeyedByStationID:dict[str, SoftwareLEDPin] = pinFactory.createAllPins(
        lineMetadata.stops,
        SCREEN_MARGIN,
        GRID_SCALE
    )

    pinDecoratorConfig = ImmutableSoftwareLEDPinDecoratorConfig(
        lineMetadata.primary_colour,
        'black',
        LED_PIN_ON_RADIUS,
        LED_PIN_OFF_RADIUS
    )

    pinDecorator = SoftwareLEDPinDecorator(pinDecoratorConfig)
    pinDecorator.decorateAll(pinsKeyedByStationID.values())

    controllersKeyedByStationID:dict[str,SoftwareLEDPinController] = dict[str,SoftwareLEDPinController]()
    for key in pinsKeyedByStationID:
        controllersKeyedByStationID[key] = SoftwareLEDPinController(pinsKeyedByStationID[key])
        canvas.addLEDController(key, controllersKeyedByStationID[key])

    for pin in pinsKeyedByStationID.values():
        canvas.addToCanvas(pin)