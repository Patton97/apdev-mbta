from __future__ import annotations
from dataclasses import dataclass

import json
import requests

from . import utils

class GetStopsParams(object):

    def __init__(self:GetStopsParams):
        self.sort:str = ''
        self.routeFilter:str = ''
        self.relationshipsToInclude:list[str] = ['route', 'child_stops'] # TODO decide which of these should be defaults vs injected

    def _getDictForMBTAAPI(self:GetStopsParams) -> dict[str, str]:
        return {
            'sort':  self.sort,
            'filter[route]' : self.routeFilter,
            'include' : ','.join(map(str, self.relationshipsToInclude))
        }

@dataclass(frozen=True)
class ImmutableStop(object):
    id:str
    name:str
    route_id:str
    child_stop_ids:tuple[str]

def getStops(session:requests.Session, params:GetStopsParams) -> list[ImmutableStop]:
    response = session.get(
        utils.MBTA_API_DOMAIN + '/stops',
        params = params._getDictForMBTAAPI(),
        headers = utils.getDefaultHeaders()
    )
    responseJsonObj= json.loads(response.content)
    return __parseGetStopsResponseContent(responseJsonObj)

def __parseGetStopsResponseContent(jsonObj:dict) -> list[ImmutableStop]:
    results = []

    for item in jsonObj["data"]:
        if item["type"] != "stop":
            continue

        stop = ImmutableStop(
            id=item["id"],
            name=item["attributes"]["name"],
            route_id=item['relationships']['route']['data']['id'],
            child_stop_ids=tuple(map(lambda child_stop_data : child_stop_data['id'], item['relationships']['child_stops']['data']))
        )
        results.append(stop)

    return results