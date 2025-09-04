from __future__ import annotations

import requests

MBTA_API_DOMAIN = 'https://api-v3.mbta.com'

def getDefaultHeaders():
    return {
        'accept': 'application/vnd.api+json',
    }

def getVehicles(session:requests.Session, params:GetVehiclesParams):
    return session.get(
        MBTA_API_DOMAIN + '/vehicles',
        params = params.getDictForMBTAAPI(),
        headers = getDefaultHeaders()
    )

class GetVehiclesParams(object):
    sort = ''
    def getDictForMBTAAPI(self:GetVehiclesParams):
        return {
            'sort':  self.sort,
        }


def getStops(session:requests.Session, params:GetStopsParams):
    return session.get(
        MBTA_API_DOMAIN + '/stops',
        params = params.getDictForMBTAAPI(),
        headers = getDefaultHeaders()
    )

class GetStopsParams(object):
    sort = ''
    routeTypes = []
    def getDictForMBTAAPI(self:GetStopsParams):
        return {
            'sort':  self.sort,
            'filter[route_type]' : ','.join(map(str, self.routeTypes)),
        }

from dataclasses import dataclass

@dataclass(frozen=True)
class ImmutableMBTAEntity:
    id:str
    name:str

@dataclass(frozen=True)
class ImmutableStation(ImmutableMBTAEntity):
    stops:list[ImmutableStop]

@dataclass(frozen=True)
class ImmutableStop(ImmutableMBTAEntity):
    idk = True

def parseResultsJson(jsonObj:dict)->list:
    results = []

    #process stations after stops
    stationsToProcess = []

    stopsKeyedByStationID:dict[str,list[ImmutableStop]] = {}

    for item in jsonObj["data"]:
        if item["type"] != "stop":
            continue

        stop = ImmutableStop(item["id"], item["attributes"]["description"])
        results.append(stop)

        stationStopList = stopsKeyedByStationID.get(__getParentStationID(item), None)
        if stationStopList == None:
            stationStopList = stopsKeyedByStationID[__getParentStationID(item)] = []

        stationStopList.append(stop)

    for station in jsonObj["included"]:
        results.append(ImmutableStation(station["id"], station["attributes"]["name"], stopsKeyedByStationID[station["id"]]))

    return results

def __getParentStationID(jsonItem):
    return jsonItem["relationships"]["parent_station"]["data"]["id"]