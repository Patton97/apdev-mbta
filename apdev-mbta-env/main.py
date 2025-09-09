import requests

from .apddev_mbta_api_wrapper import routes as mbta_routes, stops as mbta_stops

def runAPITest():    
    params = mbta_routes.GetRoutesParams()
    params.routeTypes = [0,1]

    with requests.Session() as s:
        routes:list[mbta_stops.ImmutableStop] = mbta_routes.getRoutes(s, params)

    for i in range(len(routes)):
        params = mbta_stops.GetStopsParams()
        params.routeFilter = routes[i].id

        with requests.Session() as s:
            stops = mbta_stops.getStops(s, params)

        routes[i] = mbta_routes.ImmutableRoute(id=routes[i].id, stops=stops)

    for route in routes:
        print(route.id + " | " + ', '.join(map(lambda stop : stop.id, route.stops)))
        
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