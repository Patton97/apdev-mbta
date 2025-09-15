from __future__ import annotations
from dataclasses import dataclass

import json
import requests

from . import utils
from .enums import VehicleStopStatus

@dataclass(frozen=True)
class ImmutableVehicle(object):
    id:str
    name:str
    vehicle_stop_status:VehicleStopStatus = VehicleStopStatus.UNKNOWN
    route_id:str = ''
    stop_id:str = ''

def getVehicles(session:requests.Session, params:GetVehiclesParams) -> list[ImmutableVehicle]:
    response = session.get(
        utils.MBTA_API_DOMAIN + '/vehicles',
        params = params.getDictForMBTAAPI(),
        headers = utils.getDefaultHeaders()
    )
    responseJsonObj= json.loads(response.content)
    return __parseGetVehiclesResponseContent(responseJsonObj)

class GetVehiclesParams(object):
    sort:str = ''
    routeTypes:list[str] = []
    def getDictForMBTAAPI(self:GetVehiclesParams) -> dict[str, str]:
        return {
            'sort':  self.sort,
            'filter[route_type]' : ','.join(map(str, self.routeTypes)),
            'include' : 'stop'
        }

def __parseGetVehiclesResponseContent(jsonObj:dict) -> list[ImmutableVehicle]:
    results = []

    for item in jsonObj["data"]:
        if item["type"] != "vehicle":
            continue

        if item['attributes']['current_status'] != VehicleStopStatus.STOPPED_AT:
            continue
        vehicle = ImmutableVehicle(
            id=item["id"],
            name=item["attributes"]["label"],
            vehicle_stop_status=VehicleStopStatus[item['attributes']['current_status']],
            route_id=item['relationships']['route']['data']['id'],
            stop_id=item['relationships']['stop']['data']['id'],
        )
        results.append(vehicle)

    return results