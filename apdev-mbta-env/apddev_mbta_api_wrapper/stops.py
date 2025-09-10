from __future__ import annotations
from dataclasses import dataclass

import json
import requests

from . import utils

@dataclass(frozen=True)
class ImmutableStop(object):
    id:str
    name:str
    route_id:str

def getStops(session:requests.Session, params:GetStopsParams) -> list[ImmutableStop]:
    response = session.get(
        utils.MBTA_API_DOMAIN + '/stops',
        params = params.getDictForMBTAAPI(),
        headers = utils.getDefaultHeaders()
    )
    responseJsonObj= json.loads(response.content)
    return __parseGetStopsResponseContent(responseJsonObj)

class GetStopsParams(object):
    sort:str = ''
    routeFilter:str = ''
    relationshipsToInclude:list[str] = ['route']
    def getDictForMBTAAPI(self:GetStopsParams) -> dict[str, str]:
        return {
            'sort':  self.sort,
            'filter[route]' : self.routeFilter,
            'include' : ','.join(map(str, self.relationshipsToInclude))
        }

def __parseGetStopsResponseContent(jsonObj:dict) -> list[ImmutableStop]:
    results = []

    for item in jsonObj["data"]:
        if item["type"] != "stop":
            continue

        stop = ImmutableStop(
            id=item["id"],
            name=item["attributes"]["name"],
            route_id=item['relationships']['route']['data']['id']
        )
        results.append(stop)

    return results