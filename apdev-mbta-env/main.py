import requests

from apddev_mbta_api_wrapper import routes as mbta_routes, stops as mbta_stops, vehicles as mbta_vehicles

def runAPITest():
    getRoutesParams = mbta_routes.GetRoutesParams()
    getRoutesParams.routeTypes = [0, 1]

    with requests.Session() as s:
        routes:list[mbta_stops.ImmutableStop] = mbta_routes.getRoutes(s, getRoutesParams)

    for i in range(len(routes)):
        params = mbta_stops.GetStopsParams()
        params.routeFilter = routes[i].id

        with requests.Session() as s:
            stops = mbta_stops.getStops(s, params)

        routes[i] = mbta_routes.ImmutableRoute(id=routes[i].id, stops=stops)
    
    params = mbta_vehicles.GetVehiclesParams()
    params.routeTypes = [0,1]

    with requests.Session() as s:
        vehicles:list[mbta_vehicles.ImmutableVehicle] = mbta_vehicles.getVehicles(s, params)

    stopsKeyedByID:dict[str,mbta_stops.ImmutableStop] = {}
    for stop in stops:
        stopsKeyedByID[stop.id] = stop
        for child_stop_id in stop.child_stop_ids:
            stopsKeyedByID[child_stop_id] = stop
            print(stop.name + ' | ' + child_stop_id)

    for vehicle in vehicles:
        #if vehicle.vehicle_stop_status != mbta_vehicles.VehicleStopStatus.STOPPED_AT:
            #continue
        # TODO: The vehicles are stopped at stops, but I'm just storing stations.
        if vehicle.stop_id in stopsKeyedByID:
            print('[' + vehicle.id + '] is ' + str(vehicle.vehicle_stop_status) + ' @ ' + stopsKeyedByID[vehicle.stop_id].name + ' on ' + vehicle.route_id)
        else:
            print('WARNING! Vehicle is stopped at an unknown stop: ' + vehicle.stop_id)
        
#runAPITest()


import pygame 

from apdev_led_visualiser.SoftwareLEDPin import SoftwareLEDPin
from apdev_led_visualiser.SoftwareLEDPinController import SoftwareLEDPinController

from apdev_led_visualiser.LEDVisualiser import LEDVisualiser

from GreenLinePinFactory import GreenLinePinFactory

def runVisualiser():
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    canvas = LEDVisualiser()
    canvas.setScreenSize(SCREEN_WIDTH,SCREEN_HEIGHT)

    factory = GreenLinePinFactory()
    pinsKeyedByStationID:dict[str, SoftwareLEDPin] = factory.createAllPins(pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT), pygame.Vector2(50,50), 25)

    controllersKeyedByStationID:dict[str,SoftwareLEDPinController] = dict[str,SoftwareLEDPinController]()
    for key in pinsKeyedByStationID:
        controllersKeyedByStationID[key] = SoftwareLEDPinController(pinsKeyedByStationID[key])
        canvas.addLEDController(key, controllersKeyedByStationID[key])

    for pin in pinsKeyedByStationID.values():
        canvas.addToCanvas(pin)

    canvas.start()

runVisualiser()
    