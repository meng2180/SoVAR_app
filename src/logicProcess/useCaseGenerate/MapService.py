import os
from xml.etree import ElementTree
import json
import random

from logicProcess.useCaseGenerate.Solver import solveIntersection
from src.common.constants import T_ROAD, CROSSING, ROOT_PATH
from logicProcess.useCaseGenerate.MapUtil import getRoadById, isTJunction, isAllDoubleDirectionAndNRoad, getVectorAngle, \
    isParallel, \
    getWidth, isStraightRoad, getJunctionRoads, isCrossing, isVertical, isAllWidthSatisfied
from utils.FileUtil import readFile, writeFile


MAP_INFO_FILE_PATH = os.path.join(ROOT_PATH, "resource/mapInfo.txt")

MAP_FILE_PATH = os.path.join(ROOT_PATH, "resource/map.txt")

MAP_LIST_FILE_PATH = os.path.join(ROOT_PATH, "resource/mapList.txt")


def getMapList():
    return json.loads(readFile(MAP_LIST_FILE_PATH))


def saveMapList(mapList):
    writeFile(MAP_LIST_FILE_PATH, str(mapList).replace("'", "\""))


def getMap():
    return readFile(MAP_FILE_PATH)


def saveMap(mapName):
    writeFile(MAP_FILE_PATH, mapName)
    parseMap(os.path.join(ROOT_PATH, "resource/maps/" + mapName + ".xodr"))


def parseMap(filePath):
    root = ElementTree.parse(filePath).getroot()

    tRoads = findTRoad(root)
    straightRoads = findStraightRoad(root)
    crossings = findCrossing(root)

    content = "{ \"T\" : " + str(tRoads) + ", \"straight\":" + str(straightRoads) + ", \"crossing\":" + str(crossings) + "}"
    writeFile(MAP_INFO_FILE_PATH, content)


def searchMapInfo(roadType, laneCount):
    content = readFile(MAP_INFO_FILE_PATH)
    mapInfo = json.loads(content)

    roadInfo = mapInfo["straight"]
    if roadType == T_ROAD:
        roadInfo = mapInfo["T"]
    if roadType == CROSSING:
        roadInfo = mapInfo["crossing"]

    if len(roadInfo[laneCount - 1]) == 0:
        return []

    return roadInfo[laneCount - 1][random.randint(0, len(roadInfo[laneCount - 1]) - 1)]


def findTRoad(root):
    tRoads = [[], [], [], [], [], []]
    for junction in root.findall('./junction'):
        roadIdList = getJunctionRoads(junction, root)
        roadInfoList = []
        for roadId in roadIdList:
            roadInfoList.append(getRoadById(root, roadId))

        if isTJunction(roadInfoList) and isAllWidthSatisfied(roadInfoList):
            for n in range(len(tRoads)):
                if isAllDoubleDirectionAndNRoad(roadInfoList, n + 1):
                    tRoads[n].append(findTRoadInfo(roadInfoList))
                    break

    if len(tRoads[1]) == 0:
        raise Exception("There are no eligible T roads in the map!")

    return tRoads


def findTRoadInfo(roadInfoList):
    roadPoint, roadVector = [], []
    for roadInfo in roadInfoList:
        geometry = roadInfo.findall('./planView')[0].findall('./geometry')
        start = [float(geometry[0].get('x')), float(geometry[0].get('y'))]
        end = [float(geometry[-1].get('x')), float(geometry[-1].get('y'))]

        roadPoint.append([start, end])
        roadVector.append([end[0] - start[0], end[1] - start[1]])

    mainRoadIndex, otherRoadIndex = 0, 1
    if isParallel(getVectorAngle(roadVector[0], roadVector[1])):
        mainRoadIndex = 2
        otherRoadIndex = 0
    elif isParallel(getVectorAngle(roadVector[0], roadVector[2])):
        mainRoadIndex = 1
        otherRoadIndex = 0

    oPoint = solveIntersection(roadPoint[mainRoadIndex], roadPoint[otherRoadIndex])
    vector = [oPoint[0] - roadPoint[mainRoadIndex][0][0], oPoint[1] - roadPoint[mainRoadIndex][0][1]]
    vectorX = vector[1]
    vectorY = - vector[0]
    width = getWidth(roadInfoList[mainRoadIndex])

    return [oPoint[0], oPoint[1], vectorX, vectorY, width]


def findStraightRoad(root):
    straightRoads = [[], [], [], [], [], []]
    for road in root.findall('./road'):
        if float(road.get('length')) > 100 and isStraightRoad(road) and isAllWidthSatisfied([road]):
            for n in range(len(straightRoads)):
                if isAllDoubleDirectionAndNRoad([road], n + 1):
                    straightRoads[n].append(findStraightRoadInfo(road))
                    break

    if len(straightRoads[1]) == 0:
        raise Exception("There are no eligible straight roads in the map!")

    return straightRoads


def findStraightRoadInfo(roadInfo):
    geometry = roadInfo.findall('./planView')[0].findall('./geometry')
    start = [float(geometry[0].get('x')), float(geometry[0].get('y'))]
    end = [float(geometry[-1].get('x')), float(geometry[-1].get('y'))]

    oPoint = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
    vector = [end[0] - start[0], end[1] - start[1]]
    vectorX = vector[1]
    vectorY = - vector[0]
    width = getWidth(roadInfo)

    return [oPoint[0], oPoint[1], vectorX, vectorY, width]


def findCrossing(root):
    crossings = [[], [], [], [], [], []]

    for junction in root.findall('./junction'):
        roadIdList = getJunctionRoads(junction, root)
        roadInfoList = []
        for roadId in roadIdList:
            roadInfoList.append(getRoadById(root, roadId))

        if isCrossing(roadInfoList) and isAllWidthSatisfied(roadInfoList):
            for n in range(len(crossings)):
                if isAllDoubleDirectionAndNRoad(roadInfoList, n + 1):
                    crossings[n].append(findCrossingInfo(roadInfoList))
                    break

    if len(crossings[1]) == 0:
        raise Exception("There are no eligible crossings in the map!")

    return crossings


def findCrossingInfo(roadInfoList):
    roadPoint, roadVector = [], []
    for roadInfo in roadInfoList:
        geometry = roadInfo.findall('./planView')[0].findall('./geometry')
        start = [float(geometry[0].get('x')), float(geometry[0].get('y'))]
        end = [float(geometry[-1].get('x')), float(geometry[-1].get('y'))]

        roadPoint.append([start, end])
        roadVector.append([end[0] - start[0], end[1] - start[1]])

    mainRoadIndex = 0
    if isVertical(getVectorAngle(roadVector[0], roadVector[1])):
        otherRoadIndex = 1
    elif isVertical(getVectorAngle(roadVector[0], roadVector[2])):
        otherRoadIndex = 2
    else:
        otherRoadIndex = 3

    oPoint = solveIntersection(roadPoint[mainRoadIndex], roadPoint[otherRoadIndex])
    vector = [oPoint[0] - roadPoint[mainRoadIndex][0][0], oPoint[1] - roadPoint[mainRoadIndex][0][1]]
    vectorX = vector[1]
    vectorY = - vector[0]
    width = getWidth(roadInfoList[mainRoadIndex])

    return [oPoint[0], oPoint[1], vectorX, vectorY, width]