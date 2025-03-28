import os

ROOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('SoVAR_app')[0], "SoVAR_app/")

FOLLOW_LANE = "follow lane"
STOP = "stop"
GO_ACROSS = "go across"
TURN_LEFT = "turn left"
TURN_RIGHT = "turn right"
RETROGRADE = "retrograde"
TURN_AROUND = "turn around"
CHANGE_LANE = "change lane"
DRIVE_INTO = "drive into"
DRIVE_OFF = "drive off"
HALF_U = "halfU"

ACTION_SELECTOR = [FOLLOW_LANE, STOP, GO_ACROSS, TURN_LEFT, TURN_RIGHT, RETROGRADE, TURN_AROUND, CHANGE_LANE, DRIVE_INTO, DRIVE_OFF]

DIRECTION_SELECTOR = ["N", "E", "S", "W"]

STRAIGHT_ROAD = "straight"
T_ROAD = "T"
CROSSING = "crossing"

ROAD_TYPE_SELECTOR = [STRAIGHT_ROAD, T_ROAD, CROSSING]

CAR_COUNT_SELECTOR = ["1", "2"]

LANE_COUNT_SELECTOR = ["1", "2", "3", "4", "5", "6"]

LANE_SELECTOR = ["1", "2", "3", "4", "5", "6"]

V1 = "V1"
V2 = "V2"

EGO_SELECTOR = [V1, V2]

ERROR = "error"

MAP_DICT = {
    "Sanfrancisco": "5d272540-f689-4355-83c7-03bf11b6865f"
}

SUNNY = "sunny"
NIGHT = "night"
RAINY = "rainy"
FOGGY = "foggy"
SNOWY = "snowy"
WINDY = "windy"
CLOUDY = "cloudy"
DUSK = "dusk"

WEATHER_SELECTOR = [SUNNY, NIGHT, RAINY, FOGGY, SNOWY, WINDY, CLOUDY, DUSK]

CAR_LENGTH = 4.5

CAR_WIDTH = 3

STRIKER_SELECTOR = [V1, V2]

IMPACT_PART_SELECTOR = ["front", "side", "end"]

MAX_LANE_COUNT = 6


