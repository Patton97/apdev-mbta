import requests
import json

import apdev_mbta_api_wrapper

params = apdev_mbta_api_wrapper.GetStopsParams()
params.sort = 'name'
params.routeTypes = [0,1]

with requests.Session() as s:
    response = apdev_mbta_api_wrapper.getStops(s, params)

resultsJsonObj = json.loads(response.content)
results = apdev_mbta_api_wrapper.parseResultsJson(resultsJsonObj)

for result in results:
    print(result.name)