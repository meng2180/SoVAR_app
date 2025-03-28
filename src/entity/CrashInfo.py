import json

from logicProcess.useCaseGenerate.MapService import searchMapInfo
from src.common.constants import CROSSING, T_ROAD, STRAIGHT_ROAD, ACTION_SELECTOR, FOLLOW_LANE, STOP, WEATHER_SELECTOR, \
    SUNNY, MAX_LANE_COUNT


def transformDirection(direction):
    if direction.startswith('north'):
        return 1
    if direction.startswith('east'):
        return 2
    if direction.startswith('south'):
        return 3
    if direction.startswith('west'):
        return 4
    return 1


class CrashInfo:
    weather = []
    roadType = None
    carCount = None
    laneCount = None
    v1Direction = None
    v1Lane = None
    v1Action = None
    v1TargetLane = None
    v1Speed = None
    v2Direction = None
    v2Lane = None
    v2Action = None
    v2TargetLane = None
    v2Speed = None
    striker = None
    impactPart = None

    def __init__(self, result):
        if result is None:
            return

        self.v1Speed = 20
        self.v2Speed = 20

        info = json.loads(result)

        weathers = info["weather"]
        if weathers is None or len(weathers) == 0:
            self.weather.append(SUNNY)
        else:
            for weather in weathers:
                if weather in WEATHER_SELECTOR:
                    self.weather.append(weather)

        if info["T"] == "yes":
            self.roadType = T_ROAD
        elif info["intersection"] == "yes":
            self.roadType = CROSSING
        else:
            self.roadType = STRAIGHT_ROAD

        self.carCount = info["carCount"]
        if self.carCount is None or self.carCount < 1 or self.carCount > 2:
            self.carCount = 1

        self.laneCount = info["laneCount"]
        if self.laneCount is None or self.laneCount > MAX_LANE_COUNT or len(searchMapInfo(self.roadType, self.laneCount)) == 0:
            self.laneCount = 2

        self.striker = info["striker"]
        self.impactPart = info["impactPart"]

        v1 = info["carInformation"]["V1"]
        if v1 is not None:
            self.v1Direction = transformDirection(v1["direction"])

            self.v1Lane = v1["laneNumber"]
            if self.v1Lane is None or self.v1Lane < 1:
                self.v1Lane = 1
            if self.v1Lane > self.laneCount:
                self.v1Lane = self.laneCount

            if v1["behaviors"] is None or len(v1["behaviors"]) == 0:
                self.v1Action = FOLLOW_LANE
                self.v1TargetLane = self.v1Lane
            else:
                if len(v1["behaviors"]) > 1 and v1["behaviors"][-1] == [STOP]:
                    v1["behaviors"].pop()

                v1LastAction = v1["behaviors"][-1]
                if len(v1LastAction) == 0:
                    self.v1Action = FOLLOW_LANE
                    self.v1TargetLane = self.v1Lane
                else:
                    self.v1Action = v1LastAction[0]
                    if self.v1Action not in ACTION_SELECTOR:
                        self.v1Action = FOLLOW_LANE
                        self.v1TargetLane = self.v1Lane
                    elif len(v1LastAction) == 1:
                        self.v1TargetLane = self.v1Lane
                    else:
                        self.v1TargetLane = v1LastAction[1]
                        if self.v1TargetLane < 1:
                            self.v1TargetLane = 1
                        if self.v1TargetLane > self.laneCount:
                            self.v1TargetLane = self.laneCount
        else:
            self.v1Direction = 1
            self.v1Lane = 1
            self.v1Action = FOLLOW_LANE
            self.v1TargetLane = 1

        if self.carCount == 1:
            return

        v2 = info["carInformation"]["V2"]
        if v2 is not None:
            self.v2Direction = transformDirection(v2["direction"])

            self.v2Lane = v2["laneNumber"]
            if self.v2Lane is None or self.v2Lane < 1:
                self.v2Lane = 1
            if self.v2Lane > self.laneCount:
                self.v2Lane = self.laneCount

            if v2["behaviors"] is None or len(v2["behaviors"]) == 0:
                self.v2Action = FOLLOW_LANE
                self.v2TargetLane = self.v1Lane
            else:
                if len(v2["behaviors"]) > 1 and v2["behaviors"][-1] == [STOP]:
                    v2["behaviors"].pop()

                v2LastAction = v2["behaviors"][-1]
                if len(v2LastAction) == 0:
                    self.v2Action = FOLLOW_LANE
                    self.v2TargetLane = self.v2Lane
                else:
                    self.v2Action = v2LastAction[0]
                    if self.v2Action not in ACTION_SELECTOR:
                        self.v2Action = FOLLOW_LANE
                        self.v2TargetLane = self.v2Lane
                    elif len(v2LastAction) == 1:
                        self.v2TargetLane = self.v2Lane
                    else:
                        self.v2TargetLane = v2LastAction[1]
                        if self.v2TargetLane < 1:
                            self.v2TargetLane = 1
                        if self.v2TargetLane > self.laneCount:
                            self.v2TargetLane = self.laneCount
        else:
            self.v2Direction = 1
            self.v2Lane = 1
            self.v2Action = FOLLOW_LANE
            self.v2TargetLane = 1

