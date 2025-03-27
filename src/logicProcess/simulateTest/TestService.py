import random
from common.constants import SUNNY, RAINY, FOGGY, SNOWY, WINDY, CLOUDY, DUSK, NIGHT
from src.common.constants import V2
from logicProcess.simulateTest import lgsvl
from logicProcess.simulateTest.lgsvl import Vector, Transform
import math
import time
from environs import Env


def setWeather(sim, weatherList):
    if len(weatherList) == 0:
        weatherList.apend(SUNNY)

    rain, fog, wetness, cloudiness, damage = 0, 0, 0, 0, 0
    for weather in weatherList:
        if weather == SUNNY:
            sim.set_time_of_day(12)
        if weather == RAINY:
            rain = round(random.uniform(0.2, 0.8), 2)
        if weather == FOGGY:
            fog = round(random.uniform(0.2, 0.8), 2)
        if weather == SNOWY:
            damage = 0.05
        if weather == WINDY:
            fog = round(random.uniform(0.2, 0.5), 2)
            damage = 0.05
        if weather == CLOUDY:
            cloudiness = round(random.uniform(0.2, 0.8), 2)
        if weather == DUSK:
            sim.set_time_of_day(18)
        if weather == NIGHT:
            sim.set_time_of_day(21)

    sim.weather = lgsvl.WeatherState(rain=rain, fog=fog, wetness=wetness, cloudiness=cloudiness, damage=damage)


def getVehicleWaypoints(waypoints, position, rotation):
    npcWaypoints = []
    if len(waypoints) <= 1:
        npcWaypoints.append(lgsvl.DriveWaypoint(position, 0, angle=rotation, idle=0))
        return npcWaypoints

    for i in range(1, len(waypoints)):
        transformFormer = Vector(waypoints[i - 1][0], 10.2, waypoints[i - 1][1])
        transform = Vector(waypoints[i][0], 10.2, waypoints[i][1])

        rotationVector = transform - transformFormer
        newRotation = lgsvl.Vector(0, math.degrees(math.atan2(rotationVector.x, rotationVector.z)), 0)
        npcWaypoints.append(lgsvl.DriveWaypoint(transform, waypoints[i][2], angle=newRotation, idle=0))

    return npcWaypoints


def reconstructTest(reconstructRequest):
    env = Env()
    sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"),
                          env.int("LGSVL__SIMULATOR_PORT", 8181))
    if sim.current_scene == reconstructRequest.selectedMap:
        sim.reset()
    else:
        sim.load(reconstructRequest.selectedMap)

    setWeather(sim, reconstructRequest.weatherList)

    waypointList = reconstructRequest.waypointList

    if reconstructRequest.isSingle:
        position1_former = Vector(waypointList[0][0][0], 10.2, waypointList[0][0][1])
        position2_former = Vector(waypointList[1][0][0], 10.2, waypointList[1][0][1])
        rotation1 = None
        rotation2 = None

        position2 = Vector(waypointList[1][1][0], 10.2, waypointList[1][1][1])
        rotation_vector2 = position2 - position2_former
        rotation2 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)

        if len(waypointList[0]) <= 1:
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)) - 90, 0)
        else:
            position1 = Vector(waypointList[0][1][0], 10.2, waypointList[0][1][1])
            rotation_vector1 = position1 - position1_former
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)

        w1 = getVehicleWaypoints(waypointList[0], position1_former, rotation1)
        w2 = getVehicleWaypoints(waypointList[1], position2_former, rotation2)

        state1 = lgsvl.AgentState()
        state1.transform = Transform(position1_former, rotation1)
        npc1 = sim.add_agent("SUV", lgsvl.AgentType.NPC, state1)

        state2 = lgsvl.AgentState()
        state2.transform = Transform(position2_former, rotation2)
        npc2 = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, state2)

        npc1.follow(w1)
        npc2.follow(w2)
    else:
        position1_former = Vector(waypointList[0][0][0], 10.2, waypointList[0][0][1])
        position2_former = Vector(waypointList[1][0][0], 10.2, waypointList[1][0][1])
        rotation1 = None
        rotation2 = None

        if len(waypointList[0]) <= 1:
            position2 = Vector(waypointList[1][1][0], 10.2, waypointList[1][1][1])
            rotation_vector2 = position2 - position2_former
            rotation2 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)
            if reconstructRequest.isFan:
                rotation1 = lgsvl.Vector(0, 180 + math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)
            else:
                rotation1 = rotation2
        elif len(waypointList[1]) <= 1:
            position1 = Vector(waypointList[0][1][0], 10.2, waypointList[0][1][1])
            rotation_vector1 = position1 - position1_former
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)
            if reconstructRequest.isFan:
                rotation2 = lgsvl.Vector(0, 180 + math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)
            else:
                rotation2 = rotation1
        else:
            position1 = Vector(waypointList[0][1][0], 10.2, waypointList[0][1][1])
            position2 = Vector(waypointList[1][1][0], 10.2, waypointList[1][1][1])
            rotation_vector1 = position1 - position1_former
            rotation_vector2 = position2 - position2_former
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)
            rotation2 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)

        w1 = getVehicleWaypoints(waypointList[0], position1_former, rotation1)
        w2 = getVehicleWaypoints(waypointList[1], position2_former, rotation2)

        state1 = lgsvl.AgentState()
        state1.transform = Transform(position1_former, rotation1)
        npc1 = sim.add_agent("SUV", lgsvl.AgentType.NPC, state1)

        state2 = lgsvl.AgentState()
        state2.transform = Transform(position2_former, rotation2)
        npc2 = sim.add_agent("Sedan", lgsvl.AgentType.NPC, state2)

        npc1.follow(w1)
        npc2.follow(w2)


    cameraPosition = Vector(waypointList[0][-1][0], 100, waypointList[0][-1][1])
    cameraRotation = Vector(90, 0, 0)
    camera = Transform(cameraPosition, cameraRotation)

    sim.set_sim_camera(camera)
    sim.run(30)


def on_collision(agent1, agent2, contact):
    raise Exception


def simulateTest(simulateRequest):
    env = Env()

    SIMULATOR_HOST = env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1")
    SIMULATOR_PORT = env.int("LGSVL__SIMULATOR_PORT", 8181)
    BRIDGE_HOST = env.str("LGSVL__AUTOPILOT_0_HOST", "127.0.0.1")
    BRIDGE_PORT = env.int("LGSVL__AUTOPILOT_0_PORT", 9090)

    LGSVL__AUTOPILOT_HD_MAP = env.str("LGSVL__AUTOPILOT_HD_MAP", simulateRequest.selectedMapName)
    LGSVL__AUTOPILOT_0_VEHICLE_CONFIG = env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'Lincoln2017MKZ')

    vehicle_conf = env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo6_modular)
    scene_name = env.str("LGSVL__MAP", simulateRequest.selectedMap)
    sim = lgsvl.Simulator(SIMULATOR_HOST, SIMULATOR_PORT)

    if sim.current_scene == scene_name:
        sim.reset()
    else:
        sim.load(scene_name)

    setWeather(sim, simulateRequest.weatherList)

    waypointList = simulateRequest.waypointList

    if simulateRequest.isSingle:
        position1_former = Vector(waypointList[0][0][0], 10.2, waypointList[0][0][1])
        position2_former = Vector(waypointList[1][0][0], 10.2, waypointList[1][0][1])

        position2 = Vector(waypointList[1][1][0], 10.2, waypointList[1][1][1])
        rotation_vector2 = position2 - position2_former
        rotation2 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)

        if len(waypointList[0]) <= 1:
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)) - 90, 0)
        else:
            position1 = Vector(waypointList[0][1][0], 10.2, waypointList[0][1][1])
            rotation_vector1 = position1 - position1_former
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)

        w1 = getVehicleWaypoints(waypointList[1], position2_former, rotation2)
        state1 = lgsvl.AgentState()
        state1.transform = Transform(position2_former, rotation2)
        npc = sim.add_agent("Bob", lgsvl.AgentType.PEDESTRIAN, state1)
        npc.follow(w1)

        state2 = lgsvl.AgentState()
        state2.transform = Transform(position1_former, rotation1)
        destination = [waypointList[0][-1][0], waypointList[0][-1][1]]

    else:
        position1_former = Vector(waypointList[0][0][0], 10.2, waypointList[0][0][1])
        position2_former = Vector(waypointList[1][0][0], 10.2, waypointList[1][0][1])

        if len(waypointList[0]) <= 1:
            position2 = Vector(waypointList[1][1][0], 10.2, waypointList[1][1][1])
            rotation_vector2 = position2 - position2_former
            rotation2 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)
            if simulateRequest.isFan:
                rotation1 = lgsvl.Vector(0, 180 + math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)
            else:
                rotation1 = rotation2
        elif len(waypointList[1]) <= 1:
            position1 = Vector(waypointList[0][1][0], 10.2, waypointList[0][1][1])
            rotation_vector1 = position1 - position1_former
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)
            if simulateRequest.isFan:
                rotation2 = lgsvl.Vector(0, 180 + math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)
            else:
                rotation2 = rotation1
        else:
            position1 = Vector(waypointList[0][1][0], 10.2, waypointList[0][1][1])
            position2 = Vector(waypointList[1][1][0], 10.2, waypointList[1][1][1])
            rotation_vector1 = position1 - position1_former
            rotation_vector2 = position2 - position2_former
            rotation1 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector1.x, rotation_vector1.z)), 0)
            rotation2 = lgsvl.Vector(0, math.degrees(math.atan2(rotation_vector2.x, rotation_vector2.z)), 0)

        if simulateRequest.egoCar == V2:
            w1 = getVehicleWaypoints(waypointList[0], position1_former, rotation1)
            state1 = lgsvl.AgentState()
            state1.transform = Transform(position1_former, rotation1)
            npc = sim.add_agent("SUV", lgsvl.AgentType.NPC, state1)
            npc.follow(w1)

            state2 = lgsvl.AgentState()
            state2.transform = Transform(position2_former, rotation2)
            destination = [waypointList[1][-1][0], waypointList[1][-1][1]]
        else:
            w1 = getVehicleWaypoints(waypointList[1], position2_former, rotation2)
            state1 = lgsvl.AgentState()
            state1.transform = Transform(position2_former, rotation2)
            npc = sim.add_agent("SUV", lgsvl.AgentType.NPC, state1)
            npc.follow(w1)

            state2 = lgsvl.AgentState()
            state2.transform = Transform(position1_former, rotation1)
            destination = [waypointList[0][-1][0], waypointList[0][-1][1]]

    ego = sim.add_agent(vehicle_conf, lgsvl.AgentType.EGO, state2)
    ego.connect_bridge(BRIDGE_HOST, BRIDGE_PORT)
    ego.on_collision(on_collision)

    dv = lgsvl.dreamview.Connection(sim, ego, BRIDGE_HOST)
    dv.set_hd_map(LGSVL__AUTOPILOT_HD_MAP)
    dv.set_vehicle(LGSVL__AUTOPILOT_0_VEHICLE_CONFIG)

    default_modules = [
        'Localization',
        'Transform',
        'Routing',
        'Prediction',
        'Planning',
        'Control',
        'Recorder'
    ]

    dv.disable_apollo()
    time.sleep(5)
    dv.setup_apollo(destination[0], destination[1], default_modules)

    cameraPosition = Vector(destination[0], 100, destination[1])
    cameraRotation = Vector(90, 0, 0)
    camera = Transform(cameraPosition, cameraRotation)
    sim.set_sim_camera(camera)

    sim.run(30)
