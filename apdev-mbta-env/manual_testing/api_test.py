import requests

from apddev_mbta_api_wrapper import routes as mbta_routes, stops as mbta_stops, vehicles as mbta_vehicles

def __getAllRoutes(session: requests.Session) -> list[mbta_routes.ImmutableRoute]:
    getRoutesParams = mbta_routes.GetRoutesParams()
    getRoutesParams.routeTypes = [mbta_routes.RouteType.LIGHT_RAIL, mbta_routes.RouteType.UNDERGROUND]

    return mbta_routes.getRoutes(session, getRoutesParams)
    
def __getStopsForRoute(session: requests.Session, route_id:str) -> list[mbta_stops.ImmutableStop]:
    params = mbta_stops.GetStopsParams()
    params.routeFilter = route_id
    return mbta_stops.getStops(session, params)
    
def __getAllMetros(session: requests.Session) -> list[mbta_vehicles.ImmutableVehicle]:
    params = mbta_vehicles.GetVehiclesParams()
    params.routeTypes = [mbta_routes.RouteType.LIGHT_RAIL, mbta_routes.RouteType.UNDERGROUND]
    return mbta_vehicles.getVehicles(session, params)

def runAPITest():
    with requests.Session() as session:
        routes:list[mbta_routes.ImmutableRoute] = __getAllRoutes(session)

        for i in range(len(routes)):
            stops:list[mbta_stops.ImmutableStop] = __getStopsForRoute(session, routes[i].id)
            routes[i] = mbta_routes.ImmutableRoute(id=routes[i].id, stops=stops)
        
        vehicles = __getAllMetros(session)

    stopsKeyedByID:dict[str,mbta_stops.ImmutableStop] = {}
    for route in routes:
        for stop in route.stops:
            stopsKeyedByID[stop.id] = stop
            for child_stop_id in stop.child_stop_ids:
                stopsKeyedByID[child_stop_id] = stop

    for vehicle in vehicles:
        stop = stopsKeyedByID.get(vehicle.stop_id, None)
        if stop is not None:
            print('[' + vehicle.id + '] is ' + str(vehicle.vehicle_stop_status) + ' @ ' + stopsKeyedByID[vehicle.stop_id].name + ' on ' + vehicle.route_id)
        else:
            print('WARNING! Vehicle is stopped at an unknown stop: ' + vehicle.stop_id)