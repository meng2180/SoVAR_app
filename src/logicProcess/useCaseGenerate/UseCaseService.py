import random

from logicProcess.useCaseGenerate.Solver import solveFollowLane, solveRetrograde, solveTurnRight, solveTurnLeft, \
    solveTurnAround, solveStop, solveChangeLane, solveGoAcross, solveDriveOff, solveDriveInto, solveHalfU, solveMove
from src.common.constants import T_ROAD, GO_ACROSS, STRAIGHT_ROAD, FOLLOW_LANE, TURN_LEFT, \
    RETROGRADE, CHANGE_LANE, STOP, TURN_AROUND, TURN_RIGHT, DRIVE_INTO, DRIVE_OFF, ERROR, HALF_U, V1, V2, CAR_LENGTH, \
    CAR_WIDTH
from logicProcess.useCaseGenerate.CalculateUtil import calculateTime, getDist, isFan, findFollowLaneTurnAroundDistrict, \
    findGoAcrossGoAcrossDistrict, findGoAcrossTurnAroundDistrict, findGoAcrossTurnLeftDistrict, \
    findGoAcrossTurnRightDistrict, renderWaypointsIdle, mapWaypointsToMap, findTurnLeftTurnRightDistrict

from logicProcess.useCaseGenerate.MapService import searchMapInfo


def generate(crashInfo):
    adjustCrashInfo(crashInfo)

    if crashInfo.carCount == 1:
        return calculateForSingle(crashInfo)
    return calculateForTwo(crashInfo)


def adjustCrashInfo(crashInfo):
    if len(searchMapInfo(crashInfo.roadType, crashInfo.laneCount)) == 0:
        crashInfo.laneCount = 2
    if crashInfo.v1Lane > crashInfo.laneCount:
        crashInfo.v1Lane = crashInfo.laneCount

    if crashInfo.v1TargetLane > crashInfo.laneCount:
        crashInfo.v1TargetLane = crashInfo.laneCount

    if crashInfo.v2Lane > crashInfo.laneCount:
        crashInfo.v2Lane = crashInfo.laneCount
    if crashInfo.v2TargetLane > crashInfo.laneCount:
        crashInfo.v2TargetLane = crashInfo.laneCount


def calculateForSingle(crashInfo):
    laneCount = crashInfo.laneCount
    roadType = crashInfo.roadType

    crashInfo.v1Direction = 1
    crashInfo.v1Lane = laneCount - crashInfo.v1Lane + 1
    crashInfo.v1TargetLane = laneCount - crashInfo.v1TargetLane + 1

    if crashInfo.roadType == T_ROAD:
        if crashInfo.v1Action in [GO_ACROSS, RETROGRADE]:
            crashInfo.v1Direction = 2

    if roadType == STRAIGHT_ROAD:
        if crashInfo.v1Action == GO_ACROSS:
            crashInfo.v1Action = FOLLOW_LANE

        if crashInfo.v1Action == TURN_LEFT:
            crashInfo.v1Action = RETROGRADE

        if crashInfo.v1Action == TURN_RIGHT:
            crashInfo.v1Action = DRIVE_OFF

    if crashInfo.v1Action == CHANGE_LANE and crashInfo.v1Lane == crashInfo.v1TargetLane:
        crashInfo.v1Action = FOLLOW_LANE

    mapInfo = searchMapInfo(roadType, laneCount)
    width = mapInfo[4]

    crashPoint = findCrashPointForSingle(crashInfo, width)
    if crashPoint == ERROR:
        return ERROR, False, True

    waypointList = generateWaypointsForSingle(crashInfo, width, crashPoint)
    mapWaypointsToMap(waypointList, mapInfo)

    return waypointList, False, True


def findCrashPointForSingle(crashInfo, width):
    lastAction = crashInfo.v1Action
    curLane = crashInfo.v1Lane
    targetLane = crashInfo.v1TargetLane
    roadType = crashInfo.roadType
    laneCount = crashInfo.laneCount

    if lastAction in [CHANGE_LANE, FOLLOW_LANE, STOP]:
        if lastAction != CHANGE_LANE:
            targetLane = curLane
        length = round(random.uniform(width * (targetLane - 1) + 1, width * targetLane - 1), 1)
        if roadType == STRAIGHT_ROAD:
            return [[length, 0], [(laneCount + 1) * width, 0]]
        else:
            return [[length, - laneCount * width - 10], [width * (laneCount + 1), - laneCount * width - 10]]

    if lastAction == GO_ACROSS:
        length = round(random.uniform((curLane - 1) * width + 1, curLane * width - 1), 1)
        return [[laneCount * width + 10, - length], [laneCount * width + 10, - width]]

    if lastAction == RETROGRADE:
        length = round(random.uniform(width * (targetLane - 1) + 1, width * targetLane - 1), 1)
        if roadType == STRAIGHT_ROAD:
            return [[- length, 0], [- (laneCount + 1) * width, 0]]
        else:
            return [[width * laneCount + 10, length], [width * laneCount + 10, width * (laneCount + 1)]]

    if lastAction == TURN_AROUND:
        length = round(random.uniform(width * (targetLane - 1) + 1, width * targetLane - 1), 1)
        if roadType == STRAIGHT_ROAD:
            return [[- length, - 2 * width], [- (laneCount + 1) * width, - 2 * width]]
        else:
            return [[- length, - laneCount * width - 10], [- laneCount * width - width, - laneCount * width - 10]]

    if lastAction == TURN_LEFT:
        length = round(random.uniform((targetLane - 1) * width + 1, targetLane * width - 1), 1)
        return [[- laneCount * width - 10, length], [- laneCount * width - 10, (laneCount + 1) * width]]

    if lastAction == TURN_RIGHT:
        length = round(random.uniform((targetLane - 1) * width + 1, targetLane * width - 1), 1)
        return [[width * laneCount + 10, - length], [width * laneCount + 10, - laneCount * width - width]]

    if lastAction == DRIVE_INTO:
        length = round(random.uniform(width * (targetLane - 1) + 1, width * targetLane - 1), 1)
        if roadType == STRAIGHT_ROAD:
            return [[length, 0], [(laneCount + 1) * width, 0]]
        else:
            return [[length, - laneCount * width - 10], [width * (laneCount + 1), - laneCount * width - 10]]

    if lastAction == DRIVE_OFF:
        if roadType == STRAIGHT_ROAD:
            return [[laneCount * width + width, 0], [laneCount * width + width, - 10]]
        else:
            return [[laneCount * width + width, - laneCount * width - 10], [laneCount * width + width, - laneCount * width - 20]]

    return ERROR


def generateWaypointsForSingle(crashInfo, width, crashPoint):
    waypointList = []

    end = [crashPoint[0][0], crashPoint[0][1], crashInfo.v1Speed]
    waypoints = solveAction(crashInfo.v1Action, crashInfo.v1Direction, crashInfo.v1Lane, crashInfo.v1TargetLane, crashInfo.roadType, crashInfo.laneCount, end, width)
    waypointList.append(waypoints)

    costTime = calculateTime(waypointList[0])
    if costTime == 0:
        costTime = 5

    pedestrainSpeed = 3.6 * getDist(crashPoint[0], crashPoint[1]) / costTime
    waypointList.append([[crashPoint[1][0], crashPoint[1][1], pedestrainSpeed], [crashPoint[0][0], crashPoint[0][1], pedestrainSpeed]])

    return waypointList


def calculateForTwo(crashInfo):
    laneCount = crashInfo.laneCount
    roadType = crashInfo.roadType

    crashInfo.v1Lane = laneCount - crashInfo.v1Lane + 1
    crashInfo.v2Lane = laneCount - crashInfo.v2Lane + 1

    crashInfo.v1TargetLane = laneCount - crashInfo.v1TargetLane + 1
    crashInfo.v2TargetLane = laneCount - crashInfo.v2TargetLane + 1

    if roadType == T_ROAD:
        if crashInfo.v1Direction > 2:
            fan = [0, 3, 4, 1, 2]
            crashInfo.v1Direction = fan[crashInfo.v1Direction]
            crashInfo.v2Direction = fan[crashInfo.v2Direction]

        curV1D = crashInfo.v1Direction
        curV2D = crashInfo.v2Direction

        if curV1D == 1:
            if crashInfo.v1Action == TURN_LEFT:
                if curV2D == 1:
                    if crashInfo.v2Action == TURN_RIGHT:
                        crashInfo.v1Direction = 1
                        crashInfo.v2Direction = 1
                    else:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 4
                if curV2D == 2:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 1
                if curV2D == 3:
                    crashInfo.v1Direction = 4
                    crashInfo.v2Direction = 2
            elif crashInfo.v1Action == TURN_RIGHT:
                if curV2D == 1:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 1
                        crashInfo.v2Direction = 1
                    else:
                        crashInfo.v1Direction = 2
                        crashInfo.v2Direction = 2
                if curV2D == 3:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 2
                        crashInfo.v2Direction = 4
            else:
                if curV2D == 1:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 4
                    elif crashInfo.v2Action == TURN_RIGHT:
                        crashInfo.v1Direction = 2
                        crashInfo.v2Direction = 2
                if curV2D == 2:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 1
                if curV2D == 3:
                    crashInfo.v1Direction = 2
                    crashInfo.v2Direction = 4
                if curV2D == 4:
                    if crashInfo.v2Action in [TURN_LEFT, TURN_RIGHT]:
                        crashInfo.v1Direction = 2
                        crashInfo.v2Direction = 1
        if curV1D == 2:
            if crashInfo.v1Action == TURN_LEFT:
                if curV2D == 1:
                    crashInfo.v1Direction = 1
                    crashInfo.v2Direction = 4
                if curV2D == 2:
                    if crashInfo.v2Action in [TURN_LEFT, TURN_RIGHT]:
                        crashInfo.v1Direction = 1
                        crashInfo.v2Direction = 1
                    else:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 4
                if curV2D == 3:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 1
                    else:
                        crashInfo.v1Direction = 1
                        crashInfo.v2Direction = 2
                if curV2D == 4:
                    crashInfo.v1Direction = 4
                    crashInfo.v2Direction = 2
            elif crashInfo.v1Action == TURN_RIGHT:
                if curV2D == 2:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 1
                        crashInfo.v2Direction = 1
                if curV2D == 3:
                    crashInfo.v1Direction = 1
                    crashInfo.v2Direction = 2
            else:
                if curV2D == 2:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 4
                        crashInfo.v2Direction = 4
                if curV2D == 3:
                    if crashInfo.v2Action == TURN_LEFT:
                        crashInfo.v1Direction = 1
                        crashInfo.v2Direction = 4
                    else:
                        crashInfo.v2Direction = 1
    elif roadType == STRAIGHT_ROAD:
        if crashInfo.v1Direction == 2:
            crashInfo.v1Direction = 1
        if crashInfo.v1Direction == 4:
            crashInfo.v1Direction = 3

        if crashInfo.v2Direction == 2:
            crashInfo.v2Direction = 1
        if crashInfo.v2Direction == 4:
            crashInfo.v2Direction = 3

    if crashInfo.v1Lane == crashInfo.v2Lane and crashInfo.v1Direction == crashInfo.v2Direction:
        if crashInfo.v1Action == CHANGE_LANE:
            crashInfo.v1Action = FOLLOW_LANE

        if crashInfo.v2Action == CHANGE_LANE:
            crashInfo.v2Action = FOLLOW_LANE

    if crashInfo.v1Action == TURN_AROUND and crashInfo.v1Direction == crashInfo.v2Direction:
        crashInfo.v1Action = HALF_U
        if crashInfo.v1Lane < crashInfo.v2Lane:
            crashInfo.v1Lane = laneCount
            crashInfo.v2Lane = 1

    if crashInfo.v2Action == TURN_AROUND and crashInfo.v1Direction == crashInfo.v2Direction:
        crashInfo.v2Action = HALF_U
        if crashInfo.v2Lane < crashInfo.v1Lane:
            crashInfo.v2Lane = laneCount
            crashInfo.v1Lane = 1

    if roadType == STRAIGHT_ROAD:
        if crashInfo.v1Action == GO_ACROSS:
            crashInfo.v1Action = FOLLOW_LANE

        if crashInfo.v2Action == GO_ACROSS:
            crashInfo.v2Action = FOLLOW_LANE

        if crashInfo.v1Action == TURN_LEFT:
            if crashInfo.v1Direction != crashInfo.v2Direction:
                crashInfo.v1Action = RETROGRADE
            else:
                crashInfo.v1Action = HALF_U
                if crashInfo.v1Lane < crashInfo.v2Lane:
                    crashInfo.v1Lane = laneCount
                    crashInfo.v2Lane = 1

        if crashInfo.v2Action == TURN_LEFT:
            if crashInfo.v1Direction != crashInfo.v2Direction:
                crashInfo.v2Action = RETROGRADE
            else:
                crashInfo.v2Action = HALF_U
                if crashInfo.v2Lane < crashInfo.v1Lane:
                    crashInfo.v2Lane = laneCount
                    crashInfo.v1Lane = 1

    if crashInfo.v1Action == RETROGRADE:
        fan = [0, 3, 4, 1, 2]
        crashInfo.v2Direction = fan[crashInfo.v1Direction]

    if crashInfo.v2Action == RETROGRADE:
        fan = [0, 3, 4, 1, 2]
        crashInfo.v1Direction = fan[crashInfo.v2Direction]

    if isFan(crashInfo.v1Direction, crashInfo.v2Direction):
        if crashInfo.v1Action == CHANGE_LANE:
            if crashInfo.v2Action != TURN_LEFT:
                crashInfo.v1Action = RETROGRADE
            else:
                crashInfo.v1Action = GO_ACROSS

        if crashInfo.v2Action == CHANGE_LANE:
            if crashInfo.v1Action != TURN_LEFT:
                crashInfo.v2Action = RETROGRADE
            else:
                crashInfo.v2Action = GO_ACROSS

    if roadType != STRAIGHT_ROAD:
        if (crashInfo.v1Action == STOP or crashInfo.v1Action == FOLLOW_LANE) and crashInfo.v2Action == GO_ACROSS:
            crashInfo.v2Action = FOLLOW_LANE

        if (crashInfo.v2Action == STOP or crashInfo.v2Action == FOLLOW_LANE) and crashInfo.v1Action == GO_ACROSS:
            crashInfo.v1Action = FOLLOW_LANE

        if crashInfo.v1Direction != crashInfo.v2Direction:
            if crashInfo.v1Action in [FOLLOW_LANE, STOP, CHANGE_LANE, DRIVE_INTO, DRIVE_OFF] and crashInfo.v2Action != RETROGRADE:
                crashInfo.v1Action = GO_ACROSS

            if crashInfo.v2Action in [FOLLOW_LANE, STOP, CHANGE_LANE, DRIVE_INTO, DRIVE_OFF] and crashInfo.v1Action != RETROGRADE:
                crashInfo.v2Action = GO_ACROSS

        if crashInfo.v1Direction == crashInfo.v2Direction:
            if crashInfo.v1Action in [TURN_LEFT, TURN_RIGHT]:
                if crashInfo.v2Action == FOLLOW_LANE:
                    crashInfo.v2Action = GO_ACROSS

            if crashInfo.v2Action in [TURN_LEFT, TURN_RIGHT]:
                if crashInfo.v1Action == FOLLOW_LANE:
                    crashInfo.v1Action = GO_ACROSS

    mapInfo = searchMapInfo(roadType, laneCount)
    width = mapInfo[4]

    crashPoint = findCrashPointForTwo(crashInfo, width)
    if crashPoint == ERROR:
        return ERROR, False, False

    waypointList = generateWaypointsForTwo(crashInfo, width, crashPoint)

    mapWaypointsToMap(waypointList, mapInfo)

    return waypointList, isFan(crashInfo.v1Direction, crashInfo.v2Direction), False


def findCrashPointForTwo(crashInfo, width):
    lastAction1 = crashInfo.v1Action
    curLane1 = crashInfo.v1Lane
    targetLane1 = crashInfo.v1TargetLane
    direction1 = crashInfo.v1Direction

    lastAction2 = crashInfo.v2Action
    curLane2 = crashInfo.v2Lane
    targetLane2 = crashInfo.v2TargetLane
    direction2 = crashInfo.v2Direction

    roadType = crashInfo.roadType
    laneCount = crashInfo.laneCount

    if lastAction1 == CHANGE_LANE:
        if lastAction2 in [CHANGE_LANE, FOLLOW_LANE, RETROGRADE, STOP, DRIVE_INTO, HALF_U]:
            destLane = targetLane1
            if direction1 != direction2 and lastAction2 != RETROGRADE:
                return ERROR
            if lastAction2 == CHANGE_LANE and destLane != targetLane2:
                targetLane2 = destLane
            if lastAction2 in [FOLLOW_LANE, STOP] and destLane != curLane2:
                destLane = curLane2
                targetLane1 = curLane2

            length = round(random.uniform(width * (destLane - 1) + 1, width * destLane - 1), 1)
            if roadType == STRAIGHT_ROAD:
                if direction1 == 1:
                    return [length, 0]
                if direction1 == 2:
                    return [0, - length]
                if direction1 == 3:
                    return [- length, 0]
                if direction1 == 4:
                    return [0, length]
            else:
                if direction1 == 1:
                    return [length, - width * laneCount]
                if direction1 == 4:
                    return [width * laneCount, length]
                if direction1 == 3:
                    return [- length, width * laneCount]
                if direction1 == 2:
                    return [- width * laneCount, - length]

        if lastAction2 == TURN_AROUND:
            if not isFan(direction1, direction2):
                return ERROR

            if targetLane1 > targetLane2:
                targetLane1 = targetLane2

            return findFollowLaneTurnAroundDistrict(direction1, targetLane1, targetLane2, laneCount, width)

        return ERROR


    if lastAction1 == FOLLOW_LANE:
        if lastAction2 in [CHANGE_LANE, FOLLOW_LANE, RETROGRADE, STOP, DRIVE_INTO, HALF_U]:
            destLane = curLane1
            if direction1 != direction2 and lastAction2 != RETROGRADE:
                return ERROR
            if lastAction2 == CHANGE_LANE and destLane != targetLane2:
                targetLane2 = destLane

            length = round(random.uniform(width * (destLane - 1) + 1, width * destLane - 1), 1)
            if roadType == STRAIGHT_ROAD:
                if direction1 == 1:
                    return [length, 0]
                if direction1 == 2:
                    return [0, - length]
                if direction1 == 3:
                    return [- length, 0]
                if direction1 == 4:
                    return [0, length]
            else:
                if direction1 == 1:
                    return [length, - width * laneCount]
                if direction1 == 4:
                    return [width * laneCount, length]
                if direction1 == 3:
                    return [- length, width * laneCount]
                if direction1 == 2:
                    return [- width * laneCount, - length]

        if lastAction2 == TURN_AROUND:
            if not isFan(direction1, direction2):
                return ERROR

            if curLane1 > targetLane2:
                targetLane2 = curLane1

            return findFollowLaneTurnAroundDistrict(direction1, curLane1, targetLane2, laneCount, width)

        return ERROR


    if lastAction1 == GO_ACROSS:
        destLane = curLane1
        if lastAction2 in [RETROGRADE, STOP]:
            if lastAction2 == RETROGRADE:
                if not isFan(direction1, direction2):
                    return ERROR

            if lastAction2 == STOP:
                if direction1 != direction2:
                    return ERROR

            length = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
            if direction1 == 1:
                return [length, laneCount * width]
            if direction1 == 2:
                return [laneCount * width, - length]
            if direction1 == 3:
                return [- length, - width * laneCount]
            if direction1 == 4:
                return [- width * laneCount, length]

        if lastAction2 == GO_ACROSS:
            if isFan(direction1, direction2) or direction1 == direction2:
                return ERROR

            return findGoAcrossGoAcrossDistrict(direction1, curLane1, direction2, curLane2, laneCount, width)

        if lastAction2 == TURN_AROUND:
            if not isFan(direction1, direction2):
                return ERROR

            if curLane1 > targetLane2:
                targetLane2 = curLane1

            return findGoAcrossTurnAroundDistrict(direction1, curLane1, targetLane2, laneCount, width)

        if lastAction2 == TURN_LEFT:
            newDirections = [0, 4, 1, 2, 3]
            if direction1 == newDirections[direction2] and curLane1 > lastAction2[1]:
                targetLane2 = curLane1
            if direction1 == direction2 and curLane1 >= curLane2:
                crashInfo.v1Lane = 1
                curLane1 = 1
                crashInfo.v2Lane = laneCount
                curLane2 = laneCount

            return findGoAcrossTurnLeftDistrict(direction1, curLane1, direction2, curLane2, targetLane2, laneCount, width)

        if lastAction2 == TURN_RIGHT:
            newDirections = [0, 2, 3, 4, 1]
            if direction1 == newDirections[direction2]:
                if curLane1 < targetLane2:
                    targetLane2 = curLane1

                return findGoAcrossTurnRightDistrict(direction1, curLane1, curLane2, laneCount, width)

            if direction1 == direction2:
                if curLane1 <= curLane2:
                    crashInfo.v1Lane = laneCount
                    curLane1 = laneCount
                    crashInfo.v2Lane = 1
                    curLane2 = 1

                destLane = targetLane2
                x = 0
                y = 0
                if direction1 == 1:
                    x = round(random.uniform((curLane1 - 1) * width + 1, curLane1 * width - 1), 1)
                    y = round(random.uniform(- destLane * width + 1, (- destLane + 1) * width - 1), 1)
                if direction1 == 2:
                    y = round(random.uniform(- curLane1 * width + 1, (- curLane1 + 1) * width - 1), 1)
                    x = round(random.uniform(- destLane * width + 1, (- destLane + 1) * width - 1), 1)
                if direction1 == 3:
                    x = round(random.uniform(- curLane1 * width + 1, (- curLane1 + 1) * width - 1), 1)
                    y = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
                if direction1 == 4:
                    y = round(random.uniform((curLane1 - 1) * width + 1, curLane1 * width - 1), 1)
                    x = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
                return [x, y]

        return ERROR


    if lastAction1 == RETROGRADE:
        if lastAction2 in [CHANGE_LANE, FOLLOW_LANE, STOP]:
            destLane = curLane2
            if lastAction2 == CHANGE_LANE:
                destLane = targetLane2
            if not isFan(direction1, direction2):
                return ERROR

            length = round(random.uniform(width * (destLane - 1) + 1, width * destLane - 1), 1)
            if roadType == STRAIGHT_ROAD:
                if direction2 == 1:
                    return [length, 0]
                if direction2 == 2:
                    return [0, - length]
                if direction2 == 3:
                    return [- length, 0]
                if direction2 == 4:
                    return [0, length]
            else:
                if direction2 == 1:
                    return [length, - width * laneCount]
                if direction2 == 4:
                    return [width * laneCount, length]
                if direction2 == 3:
                    return [- length, width * laneCount]
                if direction2 == 2:
                    return [- width * laneCount, - length]

        if lastAction2 in [GO_ACROSS, TURN_LEFT, TURN_RIGHT]:
            destLane = curLane2
            if lastAction2 == TURN_LEFT:
                destLane = lastAction2[1]
                newDirections = [0, 4, 1, 2, 3]
                if not isFan(direction1, newDirections[direction2]):
                    return ERROR
            if lastAction2 == TURN_RIGHT:
                destLane = lastAction2[1]
                newDirections = [0, 2, 3, 4, 1]
                if not isFan(direction1, newDirections[direction2]):
                    return ERROR

            length = round(random.uniform(width * (destLane - 1) + 1, width * destLane - 1), 1)
            if direction1 == 1:
                return [- length, - width * laneCount]
            if direction1 == 2:
                return [- width * laneCount, length]
            if direction1 == 3:
                return [length, laneCount * width]
            if direction1 == 4:
                return [laneCount * width, - length]

        return ERROR


    if lastAction1 == STOP:
        if lastAction2 in [FOLLOW_LANE, CHANGE_LANE, STOP, RETROGRADE, DRIVE_INTO, HALF_U]:
            if lastAction2 == RETROGRADE:
                if not isFan(direction1, direction2):
                    return ERROR
            elif direction1 != direction2:
                return ERROR
            if lastAction2 == FOLLOW_LANE and curLane1 != curLane2:
                curLane2 = curLane1
            if lastAction2 == CHANGE_LANE and curLane1 != targetLane2:
                targetLane2 = curLane1

            length = round(random.uniform((curLane1 - 1) * width + 1, curLane1 * width - 1), 1)
            if roadType == STRAIGHT_ROAD:
                if direction1 == 1:
                    return [length, 0]
                if direction1 == 2:
                    return [0, - length]
                if direction1 == 3:
                    return [- length, 0]
                if direction1 == 4:
                    return [0, length]
            else:
                if direction1 == 1:
                    return [length, - width * laneCount]
                if direction1 == 4:
                    return [width * laneCount, length]
                if direction1 == 3:
                    return [- length, width * laneCount]
                if direction1 == 2:
                    return [- width * laneCount, - length]

        if lastAction2 == DRIVE_OFF:
            if roadType == STRAIGHT_ROAD:
                if direction1 == 1:
                    return [laneCount * width + width, 0]
                if direction1 == 2:
                    return [0, - laneCount * width - width]
                if direction1 == 3:
                    return [- laneCount * width - width, 0]
                if direction1 == 4:
                    return [0, laneCount * width + width]
            else:
                if direction1 == 1:
                    return [laneCount * width + width, - laneCount * width - 10]
                if direction1 == 2:
                    return [- laneCount * width - 10, - laneCount * width - width]
                if direction1 == 3:
                    return [- laneCount * width - width, laneCount * width + 10]
                if direction1 == 4:
                    return [laneCount * width + 10, laneCount * width + width]

        return ERROR


    if lastAction1 == TURN_AROUND:
        if lastAction2 == GO_ACROSS:
            if not isFan(direction1, direction2):
                return ERROR
            if targetLane1 < curLane2:
                targetLane1 = curLane2
            return findGoAcrossTurnAroundDistrict(direction2, curLane2, targetLane1, laneCount, width)

        if lastAction2 == TURN_LEFT:
            if targetLane2 > targetLane1:
                targetLane1 = targetLane2
            newDirections = [0, 4, 1, 2, 3]
            if not isFan(direction1, newDirections[direction2]):
                return ERROR

            return findGoAcrossTurnAroundDistrict(newDirections[direction2], targetLane2, targetLane1, laneCount, width)

        if lastAction2 == TURN_RIGHT:
            if targetLane2 > targetLane1:
                targetLane1 = targetLane2
            newDirections = [0, 2, 3, 4, 1]
            if not isFan(direction1, newDirections[direction2]):
                return ERROR

            return findGoAcrossTurnAroundDistrict(newDirections[direction2], targetLane2, targetLane1, laneCount, width)

        if lastAction2 == FOLLOW_LANE:
            if not isFan(direction1, direction2):
                return ERROR

            if curLane2 > targetLane1:
                targetLane1 = curLane2

            return findFollowLaneTurnAroundDistrict(direction2, curLane2, targetLane1, laneCount, width)

        if lastAction2 == CHANGE_LANE:
            if not isFan(direction1, direction2):
                return ERROR

            if targetLane2 > targetLane1:
                targetLane2 = targetLane1

            return findFollowLaneTurnAroundDistrict(direction2, targetLane2, targetLane1, laneCount, width)

        return ERROR


    if lastAction1 == TURN_LEFT:
        if lastAction2 == GO_ACROSS:
            newDirections = [0, 4, 1, 2, 3]
            if direction2 == newDirections[direction1] and curLane2 > targetLane1:
                targetLane1 = curLane2
            if direction1 == direction2 and curLane1 <= curLane2:
                crashInfo.v1Lane = laneCount
                curLane1 = laneCount
                crashInfo.v2Lane = 1
                curLane2 = 1

            return findGoAcrossTurnLeftDistrict(direction2, curLane2, direction1, curLane1, targetLane1, laneCount, width)

        if lastAction2 == RETROGRADE:
            newDirections = [0, 4, 1, 2, 3]
            if not isFan(direction2, newDirections[direction1]):
                return ERROR

            destLane = targetLane1
            length = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
            if direction1 == 4:
                return [- length, - laneCount * width]
            if direction1 == 1:
                return [- laneCount * width, length]
            if direction1 == 2:
                return [length, laneCount * width]
            if direction1 == 3:
                return [laneCount * width, - length]

        if lastAction2 == TURN_AROUND:
            if targetLane1 > targetLane2:
                targetLane2 = targetLane1
            newDirections = [0, 4, 1, 2, 3]
            if not isFan(direction2, newDirections[direction1]):
                return ERROR

            return findGoAcrossTurnAroundDistrict(newDirections[direction1], targetLane1, targetLane2, laneCount, width)

        if lastAction2 == TURN_LEFT:
            return [0, 0]

        if lastAction2 == TURN_RIGHT:
            return findTurnLeftTurnRightDistrict(direction1, curLane1, targetLane1, direction2, curLane2, targetLane2, laneCount, width, crashInfo)

        return ERROR


    if lastAction1 == TURN_RIGHT:
        if lastAction2 == GO_ACROSS:
            newDirections = [0, 2, 3, 4, 1]
            if direction2 == newDirections[direction1]:
                if curLane2 < targetLane1:
                    targetLane1 = curLane2

                return findGoAcrossTurnRightDistrict(direction2, curLane2, curLane1, laneCount, width)

            if direction1 == direction2:
                if curLane2 <= curLane1:
                    crashInfo.v1Lane = 1
                    curLane1 = 1
                    crashInfo.v2Lane = laneCount
                    curLane2 = laneCount

                destLane = targetLane1
                x = 0
                y = 0
                if direction1 == 1:
                    x = round(random.uniform((curLane2 - 1) * width + 1, curLane2 * width - 1), 1)
                    y = round(random.uniform((- destLane) * width + 1, (- destLane + 1) * width - 1), 1)
                if direction1 == 2:
                    y = round(random.uniform((- curLane2) * width + 1, (- curLane2 + 1) * width - 1), 1)
                    x = round(random.uniform((- destLane) * width + 1, (- destLane + 1) * width - 1), 1)
                if direction1 == 3:
                    x = round(random.uniform((- curLane2) * width + 1, (- curLane2 + 1) * width - 1), 1)
                    y = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
                if direction1 == 4:
                    y = round(random.uniform((curLane2 - 1) * width + 1,  curLane2 * width - 1), 1)
                    x = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
                return [x, y]

        if lastAction2 == RETROGRADE:
            newDirections = [0, 2, 3, 4, 1]
            if not isFan(direction2, newDirections[direction1]):
                return ERROR

            destLane = targetLane1
            length = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
            if direction1 == 2:
                return [- length, - laneCount * width]
            if direction1 == 3:
                return [- laneCount * width, length]
            if direction1 == 4:
                return [length, laneCount * width]
            if direction1 == 1:
                return [laneCount * width, - length]

        if lastAction2 == TURN_AROUND:
            if targetLane1 > targetLane2:
                targetLane2 = targetLane1
            newDirections = [0, 2, 3, 4, 1]
            if not isFan(direction2, newDirections[direction1]):
                return ERROR

            return findGoAcrossTurnAroundDistrict(newDirections[direction1], targetLane1, targetLane2, laneCount, width)

        if lastAction2 == TURN_LEFT:
            return findTurnLeftTurnRightDistrict(direction2, curLane2, targetLane2, direction1, curLane1, targetLane1, laneCount, width, crashInfo)

        if lastAction2 == TURN_RIGHT:
            if direction1 != direction2:
                return ERROR

            destLane = targetLane1
            length = round(random.uniform((destLane - 1) * width + 1, destLane * width - 1), 1)
            if direction1 == 1:
                return [laneCount * width, - length]
            if direction1 == 2:
                return [- length, - laneCount * width]
            if direction1 == 3:
                return [- laneCount * width, length]
            if direction1 == 4:
                return [length, laneCount * width]

        return ERROR


    if lastAction1 == DRIVE_INTO:
        if lastAction2 in [CHANGE_LANE, FOLLOW_LANE, STOP]:
            if direction1 != direction2:
                return ERROR

            destLane = curLane2
            if lastAction2 == CHANGE_LANE:
                destLane = targetLane2

            length = round(random.uniform(width * (destLane - 1) + 1, width * destLane - 1), 1)
            if roadType == STRAIGHT_ROAD:
                if direction1 == 1:
                    return [length, 0]
                if direction1 == 2:
                    return [0, - length]
                if direction1 == 3:
                    return [- length, 0]
                if direction1 == 4:
                    return [0, length]
            else:
                if direction1 == 1:
                    return [length, - laneCount * width]
                if direction1 == 4:
                    return [width * laneCount, length]
                if direction1 == 3:
                    return [- length, width * laneCount]
                if direction1 == 2:
                    return [- laneCount * width, - length]

        return ERROR


    if lastAction1 == HALF_U:
        if lastAction2 in [CHANGE_LANE, FOLLOW_LANE, STOP]:
            if direction1 != direction2:
                return ERROR

            destLane = curLane2
            if lastAction2 == CHANGE_LANE:
                destLane = targetLane2

            length = round(random.uniform(width * (destLane - 1) + 1, width * destLane - 1), 1)
            if roadType == STRAIGHT_ROAD:
                if direction1 == 1:
                    return [length, 0]
                if direction1 == 2:
                    return [0, - length]
                if direction1 == 3:
                    return [- length, 0]
                if direction1 == 4:
                    return [0, length]
            else:
                if direction1 == 1:
                    return [length, - laneCount * width]
                if direction1 == 4:
                    return [width * laneCount, length]
                if direction1 == 3:
                    return [- length, width * laneCount]
                if direction1 == 2:
                    return [- laneCount * width, - length]

        return ERROR


    if lastAction1 == DRIVE_OFF:
        if lastAction2 != STOP:
            return ERROR

        if roadType == STRAIGHT_ROAD:
            if direction1 == 1:
                return [laneCount * width + width, 0]
            if direction1 == 2:
                return [0, - laneCount * width - width]
            if direction1 == 3:
                return [- laneCount * width - width, 0]
            if direction1 == 4:
                return [0, laneCount * width + width]
        else:
            if direction1 == 1:
                return [laneCount * width + width, - laneCount * width - 10]
            if direction1 == 2:
                return [- laneCount * width - 10, - laneCount * width - width]
            if direction1 == 3:
                return [- laneCount * width - width, laneCount * width + 10]
            if direction1 == 4:
                return [laneCount * width + 10, laneCount * width + width]

    return ERROR


def generateWaypointsForTwo(crashInfo, width, crashPoint):
    if crashInfo.v1Action == FOLLOW_LANE and crashInfo.v2Action == FOLLOW_LANE and crashInfo.v1Direction == crashInfo.v2Direction:
        if crashInfo.striker == V1 and crashInfo.v1Speed <= crashInfo.v2Speed:
            crashInfo.v1Speed = crashInfo.v2Speed + 20
        if crashInfo.striker == V2 and crashInfo.v2Speed <= crashInfo.v1Speed:
            crashInfo.v2Speed = crashInfo.v1Speed + 20

    end1 = [crashPoint[0], crashPoint[1], crashInfo.v1Speed]
    waypoints1 = solveAction(crashInfo.v1Action, crashInfo.v1Direction, crashInfo.v1Lane, crashInfo.v1TargetLane, crashInfo.roadType, crashInfo.laneCount, end1, width)

    end2 = [crashPoint[0], crashPoint[1], crashInfo.v2Speed]
    waypoints2 = solveAction(crashInfo.v2Action, crashInfo.v2Direction, crashInfo.v2Lane, crashInfo.v2TargetLane, crashInfo.roadType, crashInfo.laneCount, end2, width)

    if crashInfo.v1Action != STOP and crashInfo.v2Action != STOP:
        adjustTrajectory(waypoints1, waypoints2, crashInfo)

    return [waypoints1, waypoints2]


def adjustTrajectory(waypoints1, waypoints2, crashInfo):
    if crashInfo.striker == V2 and crashInfo.impactPart == 3:
        waypoints1.append(solveMove(waypoints1, CAR_LENGTH / 2))
    costTime1 = calculateTime(waypoints1)

    if crashInfo.striker == V1 and crashInfo.impactPart == 3:
        waypoints2.append(solveMove(waypoints2, CAR_LENGTH / 2))
    costTime2 = calculateTime(waypoints2)

    maxTime = max(costTime1, costTime2)
    idle1 = maxTime - costTime1
    idle2 = maxTime - costTime2
    if crashInfo.striker == V1:
        if crashInfo.impactPart == 2:
            idle1 += (CAR_WIDTH / 2 + CAR_LENGTH / 2) * 3.6 / crashInfo.v1Speed
        elif crashInfo.impactPart == 3:
            idle1 += (CAR_LENGTH / 2) * 3.6 / crashInfo.v1Speed
    else:
        if crashInfo.impactPart == 2:
            idle2 += (CAR_WIDTH / 2 + CAR_LENGTH / 2) * 3.6 / crashInfo.v2Speed
        elif crashInfo.impactPart == 3:
            idle2 += (CAR_LENGTH / 2) * 3.6 / crashInfo.v2Speed

    renderWaypointsIdle(waypoints1, crashInfo.v1Direction, idle1)
    renderWaypointsIdle(waypoints2, crashInfo.v2Direction, idle2)


def solveAction(action, direction, lane, targetLane, roadType, laneCount, end, width):
    if action == FOLLOW_LANE:
        return solveFollowLane(end, direction, width)

    if action == RETROGRADE:
        return solveRetrograde(end, lane, direction, laneCount, width, roadType)

    if action == TURN_RIGHT:
        return solveTurnRight(end, lane, direction, laneCount, width)

    if action == TURN_LEFT:
        return solveTurnLeft(end, lane, direction, laneCount, width)

    if action == TURN_AROUND:
        return solveTurnAround(end, lane, direction, laneCount, width, roadType)

    if action == STOP:
        return solveStop(end)

    if action == CHANGE_LANE:
        return solveChangeLane(end, lane, direction, laneCount, width, targetLane, roadType)

    if action == GO_ACROSS:
        return solveGoAcross(end, direction, laneCount, width)

    if action == DRIVE_OFF:
        return solveDriveOff(end, lane, direction, laneCount, width, roadType)

    if action == DRIVE_INTO:
        return solveDriveInto(end, direction, laneCount, width, roadType)

    if action == HALF_U:
        return solveHalfU(end, lane, direction, laneCount, width, roadType)

    return []