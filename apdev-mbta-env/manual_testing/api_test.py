import main_api

def runAPITest():
    main_api.refreshCachedInfo()

    for vehicle, stop in main_api.getCachedVehiclesAndCurrentStops():
        if stop is None:
            print('WARNING! Vehicle is stopped at an unknown stop: ' + vehicle.stop_id)
        else:
            print('[' + vehicle.id + '] is ' + str(vehicle.vehicle_stop_status) + ' @ ' + stop.name + ' on ' + vehicle.route_id)