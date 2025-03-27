class ReconstructRequest:
    def __init__(self, waypointList, isFan, isSingle, weatherList, selectedMap):
        self.waypointList = waypointList
        self.isFan = isFan
        self.isSingle = isSingle
        self.weatherList = weatherList
        self.selectedMap = selectedMap