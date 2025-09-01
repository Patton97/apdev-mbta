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