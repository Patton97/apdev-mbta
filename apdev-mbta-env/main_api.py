import requests

from apddev_mbta_api_wrapper import routes as mbta_routes, stops as mbta_stops, vehicles as mbta_vehicles

__stopsKeyedByID:dict[str,mbta_stops.ImmutableStop] = {}
__vehiclesAndCurrentStops:list[tuple[mbta_vehicles.ImmutableVehicle, mbta_stops.ImmutableStop]] = []

def __getAllRoutes(session: requests.Session) -> list[mbta_routes.ImmutableRoute]:
    getRoutesParams = mbta_routes.GetRoutesParams()
    getRoutesParams.routeTypes = [mbta_routes.RouteType.LIGHT_RAIL, mbta_routes.RouteType.UNDERGROUND]
    return mbta_routes.getRoutes(session, getRoutesParams)
    
def __getStopsForRoute(session: requests.Session, route_id:str) -> list[mbta_stops.ImmutableStop]:
    params = mbta_stops.GetStopsParams()
    params.routeFilter = route_id
    return mbta_stops.getStops(session, params)
    
def __getAllMetroStyleVehicles(session: requests.Session) -> list[mbta_vehicles.ImmutableVehicle]:
    params = mbta_vehicles.GetVehiclesParams()
    params.routeTypes = [mbta_routes.RouteType.LIGHT_RAIL, mbta_routes.RouteType.UNDERGROUND]
    return mbta_vehicles.getVehicles(session, params)

def refreshCachedInfo():
    with requests.Session() as session:
        routes:list[mbta_routes.ImmutableRoute] = __getAllRoutes(session)

        for i in range(len(routes)):
            stops:list[mbta_stops.ImmutableStop] = __getStopsForRoute(session, routes[i].id)
            routes[i] = mbta_routes.ImmutableRoute(id=routes[i].id, stops=stops)
        
        vehicles = __getAllMetroStyleVehicles(session)

    stopsKeyedByID:dict[str,mbta_stops.ImmutableStop] = {}
    for route in routes:
        for stop in route.stops:
            stopsKeyedByID[stop.id] = stop
            for child_stop_id in stop.child_stop_ids:
                stopsKeyedByID[child_stop_id] = stop
    
    global __stopsKeyedByID
    __stopsKeyedByID = stopsKeyedByID
    
    vehiclesStoppedAtStops:list[tuple[mbta_vehicles.ImmutableVehicle, mbta_stops.ImmutableStop]] = []
    for vehicle in vehicles:
        stop = stopsKeyedByID.get(vehicle.stop_id, None)
        vehiclesStoppedAtStops.append((vehicle, stop))

    global __vehiclesAndCurrentStops
    __vehiclesAndCurrentStops = vehiclesStoppedAtStops

def getCachedStopsKeyedByID() -> dict[str,mbta_stops.ImmutableStop]:
    return __stopsKeyedByID

def getCachedVehiclesAndCurrentStops() -> list[tuple[mbta_vehicles.ImmutableVehicle, mbta_stops.ImmutableStop]]:
    return __vehiclesAndCurrentStops