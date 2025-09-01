import requests
import json

import apdev_mbta_api_wrapper
from apdev_mbta_api_wrapper import GetStopsParams

params = GetStopsParams()
params.sort = 'name'
params.routeTypes = [0,1]

with requests.Session() as s:
    response = apdev_mbta_api_wrapper.getStops(s, params)

jsonAsObj = json.loads(response.content)

# TODO: Should add a step here where we convert the json into a custom data object

for item in jsonAsObj["data"]:
    print(item["attributes"]["description"])