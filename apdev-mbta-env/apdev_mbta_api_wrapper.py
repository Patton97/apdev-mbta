import requests

MBTA_API_DOMAIN = 'https://api-v3.mbta.com'

def getDefaultHeaders():
    return {
        'accept': 'application/vnd.api+json',
    }

def getVehicles(session:requests.Session):
    return session.get(
        MBTA_API_DOMAIN + '/vehicles',
        # TODO: Should make separate param obj for these
        params = {
            'sort': 'speed',
        },
        headers = getDefaultHeaders()
    )


def getStops(session:requests.Session):
    return session.get(
        MBTA_API_DOMAIN + '/stops',
        # TODO: Should make separate param obj for these
        params = {
            'sort': 'name',
            'filter[route_type]': '0,1',
        },
        headers = getDefaultHeaders()
    )