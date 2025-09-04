import requests
import json

import APDevMBTAAPIWrapper.apdev_mbta_api_wrapper as apdev_mbta_api_wrapper

def runAPITest():
    params = apdev_mbta_api_wrapper.GetStopsParams()
    params.sort = 'name'
    params.routeTypes = [0,1]

    #with requests.Session() as s:
    #    response = apdev_mbta_api_wrapper.getStops(s, params)

    #resultsJsonObj = json.loads(response.content)
    with open('cachedResponse.json') as f:
        results = apdev_mbta_api_wrapper.parseResultsJson(json.load(f))
        
    for result in results:
        print(str(type(result)) +" | " +result.id + " | " + result.name)

runAPITest()


from APDevLEDVisualiser.LEDVisualiser import LEDVisualiser
from APDevLEDVisualiser.LEDPin import LEDPin
from GreenLinePinFactory import GreenLinePinFactory
import pygame 

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

canvas = LEDVisualiser()
canvas.setScreenSize(SCREEN_WIDTH,SCREEN_HEIGHT)

factory = GreenLinePinFactory()
pins:list[LEDPin] = factory.createAllPins(pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), pygame.Vector2(50,50), 25)

for pin in pins:
    canvas.addToCanvas(pin)

#canvas.start()