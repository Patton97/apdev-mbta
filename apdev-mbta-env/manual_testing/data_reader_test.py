import json
import requests 

from apdev_mbta_data.APDevMBTADataReader import APDevMBTADataReader

from apddev_mbta_api_wrapper import stops as mbta_stops

def runDataReaderTest():
    reader:APDevMBTADataReader = APDevMBTADataReader()
    lines = reader.read_from_file("/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/example_file.json")
    print(lines.count())

def runDataWriterTest():
    stops:list[mbta_stops.ImmutableStop] = []
    with requests.Session() as s:
        params:mbta_stops.GetStopsParams = mbta_stops.GetStopsParams()
        params.routeFilter = "Green-D"
        stops = mbta_stops.getStops(s, params)

    root_json_obj = {}
    lines_json_obj = []
    root_json_obj["lines"] = lines_json_obj

    green_d_line_json_obj = {}
    lines_json_obj.append(green_d_line_json_obj)
    green_d_line_json_obj["line_id"] = "Green-D"
    
    stops_json_obj = []
    green_d_line_json_obj["stops"] = stops_json_obj
    for stop in stops:
        stop_json_obj = {}
        stops_json_obj.append(stop_json_obj)
        stop_json_obj["stop_id"] = stop.id
        stop_json_obj["name"] = stop.name

    with open('/home/andrewpattondev/Projects/apdev-mbta/apdev-mbta-env/apdev_mbta_data/myCoolData.json', 'w', encoding='utf-8') as f:
        json.dump(root_json_obj, f, ensure_ascii=False, indent=4)