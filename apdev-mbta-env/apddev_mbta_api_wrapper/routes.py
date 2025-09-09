from __future__ import annotations
from dataclasses import dataclass

import json
import requests

import utils, stops as mbta_stops

@dataclass(frozen=True)
class ImmutableRoute(object):
    id:str
    stops:list[mbta_stops.ImmutableStop]

def getRoutes(session:requests.Session, params:GetRoutesParams) -> list[ImmutableRoute]:
    response = session.get(
        utils.MBTA_API_DOMAIN + '/routes',
        params = params.getDictForMBTAAPI(),
        headers = utils.getDefaultHeaders()
    )
    responseJsonObj = json.load(response.content)
    return __parseGetRoutesResponseContent(responseJsonObj)

class GetRoutesParams(object):
    sort:str = ''
    routeTypes = []
    def getDictForMBTAAPI(self:GetRoutesParams) -> dict[str, str]:
        return {
            'sort':  self.sort,
            'filter[type]' : ','.join(map(str, self.routeTypes)),
        }

def __parseGetRoutesResponseContent(response:dict) -> list[ImmutableRoute]:
    routes:list[ImmutableRoute] = []
    for routeAsJsonObj in response['data']:
        routes.append(ImmutableRoute(routeAsJsonObj['id'], []))
    return routes