import random
import math

from common.constants import ERROR
from logicProcess.useCaseGenerate.Solver import solveSpin


def getDist(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)


def calculateTime(waypointList):
    time = 0
    for i in range(1, len(waypointList)):
        time += getDist(waypointList[i - 1], waypointList[i]) * 3.6 / waypointList[i][2]
    return time


def isFan(direction1, direction2):
    fanDirection = [0, 3, 4, 1, 2]
    return direction2 == fanDirection[direction1]


def renderWaypointsIdle(waypoints, direction, idle):
    if idle == 0:
        return

    x = waypoints[0][0]
    y = waypoints[0][1]
    speed = waypoints[0][2]
    start = None
    deta = idle * speed / 3.6
    if direction == 1:
        start = [x, y - deta, speed]
    elif direction == 2:
        start = [x - deta, y, speed]
    elif direction == 3:
        start = [x, y + deta, speed]
    elif direction == 4:
        start = [x + deta, y, speed]
    waypoints.insert(0, start)


def mapWaypointsToMap(waypointList, mapInfo):
    for i in range(len(waypointList)):
        for j in range(len(waypointList[i])):
            waypointList[i][j][0], waypointList[i][j][1] = solveSpin(waypointList[i][j][0], waypointList[i][j][1], mapInfo[2], mapInfo[3])
            waypointList[i][j][0] += mapInfo[0]
            waypointList[i][j][1] += mapInfo[1]


def findGoAcrossGoAcrossDistrict(direction1, lane1, direction2, lane2, laneCount, width):
    xL = laneCount * width
    xR = laneCount * width
    yD = laneCount * width
    yU = laneCount * width

    if direction1 == 1:
        xL = (lane1 - 1) * width
        xR = lane1 * width
    if direction1 == 2:
        yD = - lane1 * width
        yU = (- lane1 + 1) * width
    if direction1 == 3:
        xL = - lane1 * width
        xR = (- lane1 + 1) * width
    if direction1 == 4:
        yD = (lane1 - 1) * width
        yU = lane1 * width

    if direction2 == 1:
        xL = (lane2 - 1) * width
        xR = lane2 * width
    if direction2 == 2:
        yD = - lane2 * width
        yU = (- lane2 + 1) * width
    if direction2 == 3:
        xL = - lane2 * width
        xR = (- lane2 + 1) * width
    if direction2 == 4:
        yD = (lane2 - 1) * width
        yU = lane2 * width

    x = round(random.uniform(xL + 1, xR - 1), 1)
    y = round(random.uniform(yD + 1, yU - 1), 1)
    return [x, y]


def findGoAcrossTurnAroundDistrict(direction1, lane1, destLane2, laneCount, width):
    bi = round(1.0 * lane1 ** 4 / (destLane2 ** 4), 2)
    xL = (lane1 - 1) * width + 1
    xR = lane1 * width - 1
    x = round(random.uniform(xL, xR), 1)
    y = destLane2 * width * bi

    if direction1 == 3:
        x = - x
        y = - width * laneCount - y
    if direction1 == 4:
        temp = x
        x = - width * laneCount - y
        y = temp
    if direction1 == 1:
        x = x
        y = laneCount * width + y
    if direction1 == 2:
        temp = x
        x = laneCount * width + y
        y = - temp

    return [x, y]


def findFollowLaneTurnAroundDistrict(direction1, lane1, destLane2, laneCount, width):
    bi = round(1.0 * lane1 ** 4 / (destLane2 ** 4), 2)
    xL = (lane1 - 1) * width + 1
    xR = lane1 * width - 1
    x = round(random.uniform(xL, xR), 1)
    y = destLane2 * width * bi

    if direction1 == 3:
        x = - x
        y = - y
    if direction1 == 4:
        temp = x
        x = - y
        y = temp
    if direction1 == 1:
        x = x
        y = y
    if direction1 == 2:
        temp = x
        x = y
        y = - temp

    return [x, y]


def findGoAcrossTurnLeftDistrict(direction1, lane1, direction2, lane2, destlane2, laneCount, width):
    xL = 0
    xR = 0
    yD = 0
    yU = 0

    if direction1 == 1:
        xL = (lane1 - 1) * width + 1
        xR = lane1 * width - 1
        if direction2 == 1:
            yD = 0
            yU = width
        if direction2 == 2:
            deta = destlane2 - lane1
            yD = (laneCount - deta - 1) * width
            yU = (laneCount - deta) * width
        if direction2 == 3:
            deta = laneCount - destlane2 - lane1
            yD = deta * width
            yU = (deta + 1) * width
        if direction2 == 4:
            yD = (lane2 - 1) * width
            yU = yD

    if direction1 == 2:
        yD = (- lane1) * width + 1
        yU = (- lane1 + 1) * width - 1
        if direction2 == 1:
            xL = (lane2 - 1) * width
            xR = xL
        if direction2 == 2:
            xL = 0
            xR = width
        if direction2 == 3:
            deta = destlane2 - lane1
            xL = (laneCount - deta - 1) * width
            xR = (laneCount - deta) * width
        if direction2 == 4:
            deta = laneCount - destlane2 - lane1
            xL = deta * width
            xR = (deta + 1) * width

    if direction1 == 3:
        xL = (- lane1) * width + 1
        xR = (- lane1 + 1) * width - 1
        if direction2 == 1:
            deta = 2 * laneCount - destlane2 - lane1
            yD = (laneCount - deta - 1) * width
            yU = (laneCount - deta) * width
        if direction2 == 2:
            yD = (- lane2 + 1) * width
            yU = yD
        if direction2 == 3:
            yD = - width
            yU = 0
        if direction2 == 4:
            deta = destlane2 - lane1
            yD = (deta - laneCount) * width
            yU = (deta - laneCount + 1) * width

    if direction1 == 4:
        yD = (lane1 - 1) * width + 1
        yU = lane1 * width - 1
        if direction2 == 1:
            deta = destlane2 - lane1
            xL = (deta - laneCount) * width
            xR = (deta - laneCount + 1) * width
        if direction2 == 2:
            deta = 2 * laneCount - destlane2 - lane1
            xL = (laneCount - deta - 1) * width
            xR = (laneCount - deta) * width
        if direction2 == 3:
            xL = (- lane2 + 1) * width
            xR = xL
        if direction2 == 4:
            xL = - width
            xR = 0

    x = round(random.uniform(xL, xR), 1)
    y = round(random.uniform(yD, yU), 1)
    return [x, y]


def findGoAcrossTurnRightDistrict(direction1, lane1, lane2, laneCount, width):
    xL = 0
    xR = 0
    yD = 0
    yU = 0

    if direction1 == 1:
        xL = (lane1 - 1) * width + 1
        xR = lane1 * width - 1
        yD = lane2 * width
        yU = yD

    if direction1 == 2:
        yD = - lane1 * width + 1
        yU = (- lane1 + 1) * width - 1
        xL = lane2 * width
        xR = xL

    if direction1 == 3:
        xL = - lane1 * width + 1
        xR = (- lane1 + 1) * width - 1
        yD = - lane2 * width
        yU = yD

    if direction1 == 4:
        yD = (lane1 - 1) * width + 1
        yU = lane1 * width - 1
        xL = - lane2 * width
        xR = xL

    x = round(random.uniform(xL, xR), 1)
    y = round(random.uniform(yD, yU), 1)
    return [x, y]


def findTurnLeftTurnRightDistrict(direction1, curLane1, targetLane1, direction2, curLane2, targetLane2, laneCount, width, crashInfo):
    if isFan(direction1, direction2):
        if targetLane1 < targetLane2:
            targetLane1 = targetLane2

        x, y = 0, 0
        if direction1 == 1:
            x = round(random.uniform(0, width / 2) - laneCount * width, 1)
            y = round((targetLane1 - 1) * width + random.uniform(0, width / 2), 1)
        if direction1 == 2:
            y = round((laneCount - 1) * width + random.uniform(0, width / 2), 1)
            x = round((targetLane1 - 1) * width + random.uniform(0, width / 2), 1)
        if direction1 == 3:
            x = round((laneCount - 1) * width + random.uniform(0, width / 2), 1)
            y = round((- targetLane1 + 1) * width - random.uniform(0, width / 2), 1)
        if direction1 == 4:
            y = round(random.uniform(0, width / 2) - laneCount * width, 1)
            x = round((- targetLane1 + 1) * width - random.uniform(0, width / 2), 1)
        return [x, y]

    if direction1 == direction2:
        if curLane1 <= curLane2:
            crashInfo.v1Lane = laneCount
            crashInfo.v2Lane = 1
        if direction1 == 1:
            return [(laneCount / 2.0) * width, - (laneCount - 1) * width]
        if direction1 == 2:
            return [- (laneCount - 1) * width, - (laneCount / 2.0) * width]
        if direction1 == 3:
            return [- (laneCount / 2.0) * width, (laneCount - 1) * width]
        if direction1 == 4:
            return [(laneCount - 1) * width, (laneCount / 2.0) * width]

    return ERROR
