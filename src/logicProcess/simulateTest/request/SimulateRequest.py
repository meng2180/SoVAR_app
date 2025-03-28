class SimulateRequest:
    def __init__(self, waypointList, isFan, isSingle, weatherList, selectedMapName, selectedMap, egoCar):
        self.waypointList = waypointList
        self.isFan = isFan
        self.isSingle = isSingle
        self.weatherList = weatherList
        self.selectedMapName = selectedMapName
        self.selectedMap = selectedMap
        self.egoCar = egoCar