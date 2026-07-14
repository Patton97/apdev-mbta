from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

import json
import requests

from . import utils, stops as mbta_stops

class GetRoutesParams(object):
    def __init__(self:GetRoutesParams):
        self.sort:str = ''
        self.routeTypes:list[RouteType] = []

    def _getDictForMBTAAPI(self:GetRoutesParams) -> dict[str, str]:
        return {
            'sort':  self.sort,
            'filter[type]' : ','.join([str(int(routeType.value)) for routeType in self.routeTypes]),
        }
    
# https://github.com/google/transit/blob/master/gtfs/spec/en/reference.md#routestxt
class RouteType(Enum):
    UNKNOWN     = -1
    LIGHT_RAIL  =  0 # Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area.
    UNDERGROUND =  1 # Subway, Metro. Any underground rail system within a metropolitan area.
    RAIL        =  2 # Rail. Used for intercity or long-distance travel.
    BUS         =  3 # Bus. Used for short- and long-distance bus routes.
    FERRY       =  4 # Ferry. Used for short- and long-distance boat service.
    CABLE_TRAM  =  5 # Cable tram. Used for street-level rail cars where the cable runs beneath the vehicle (e.g., cable car in San Francisco).
    CABLE_CAR   =  6 # Aerial lift, suspended cable car (e.g., gondola lift, aerial tramway). Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables.
    FUNICULAR   =  7 # Funicular. Any rail system designed for steep inclines.
    TROLLEYBUS  = 11 # Trolleybus. Electric buses that draw power from overhead wires using poles.
    MONORAIL    = 12 # Monorail. Railway in which the track consists of a single rail or a beam.

@dataclass(frozen=True)
class ImmutableRoute(object):
    id:str
    stops:list[mbta_stops.ImmutableStop]

def getRoutes(session:requests.Session, params:GetRoutesParams) -> list[ImmutableRoute]:
    try:
        response = session.get(
            utils.MBTA_API_DOMAIN + '/routes',
            params = params._getDictForMBTAAPI(),
            headers = utils.getDefaultHeaders()
        )
        responseJsonObj = json.loads(response.content)
        return __parseGetRoutesResponseContent(responseJsonObj)
    except:
        return []

def __parseGetRoutesResponseContent(response:dict) -> list[ImmutableRoute]:
    routes:list[ImmutableRoute] = []
    for routeAsJsonObj in response['data']:
        routes.append(ImmutableRoute(routeAsJsonObj['id'], []))
    return routes