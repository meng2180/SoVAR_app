import math


def getRoadById(root, id):
    for road in root.findall('./road'):
        if road.get('id') == id:
            return road
    raise Exception("地图文件错误!")


def isTJunction(roadInfoList):
    if len(roadInfoList) != 3:
        return False

    roadVector = []

    for roadInfo in roadInfoList:
        if not isStraightRoad(roadInfo):
            return False

        planVeiw = roadInfo.findall('./planView')[0]
        geometry = planVeiw.findall('./geometry')

        start = [float(geometry[0].get('x')), float(geometry[0].get('y'))]
        end = [float(geometry[-1].get('x')), float(geometry[-1].get('y'))]

        roadVector.append([end[0] - start[0], end[1] - start[1]])


    verticalCount = 0
    parallelCount = 0

    angles = [getVectorAngle(roadVector[0], roadVector[1]),
              getVectorAngle(roadVector[0], roadVector[2]),
              getVectorAngle(roadVector[1], roadVector[2])]
    for angle in angles:
        if isVertical(angle):
            verticalCount += 1
        if isParallel(angle):
            parallelCount += 1

    if verticalCount == 2 and parallelCount == 1:
        return True

    return False


def isStraightRoad(roadInfo):
    planVeiw = roadInfo.findall('./planView')[0]
    geometry = planVeiw.findall('./geometry')

    if len(geometry) == 1 and len(geometry[0].findall('./line')) == 0:
        return False

    start = [float(geometry[0].get('x')), float(geometry[0].get('y'))]
    end = [float(geometry[-1].get('x')), float(geometry[-1].get('y'))]

    for i in range(1, len(geometry) - 1):
        x = float(geometry[i].get('x'))
        y = float(geometry[i].get('y'))
        if (math.fabs((start[1] - end[1]) * x - (start[0] - end[0]) * y + start[0] * end[1] - start[1] * end[0]) / math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2)) > 0.2:
            return False

    return True


def isVertical(angle):
    return 80 <= angle <= 100


def isParallel(angle):
    return 0 <= angle <= 10 or 170 <= angle <= 180


def getVectorAngle(v1, v2):
    dotProduct = v1[0] * v2[0] + v1[1] * v2[1]

    magnitudeV1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    magnitudeV2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    cosAngle = dotProduct / (magnitudeV1 * magnitudeV2)

    angleRadians = math.acos(cosAngle)

    angleDegrees = math.degrees(angleRadians)

    return angleDegrees


def isAllDoubleDirectionAndNRoad(roadInfoList, n):
    for roadInfo in roadInfoList:
        lanes = roadInfo.findall('./lanes')[0]
        laneSection = lanes.findall('./laneSection')[0]

        left = laneSection.findall('./left')
        if len(left) == 0:
            return False

        leftLanes = left[0].findall('./lane')
        if len(leftLanes) != n:
            return False

        right = laneSection.findall('./right')
        if len(right) == 0:
            return False

        rightLanes = right[0].findall('./lane')
        if len(rightLanes) != n:
            return False
    return True


def isAllWidthSatisfied(roadInfoList):
    widthList = []
    for roadInfo in roadInfoList:
        laneList = getAllLanes(roadInfo)
        for lane in laneList:
            widthList.append(getLaneWidth(lane))

    avgWidth = sum(widthList) / len(widthList)
    for width in widthList:
        if math.fabs(width - avgWidth) > 1:
            return False

    return True


def getLaneWidth(lane):
    return float(lane.findall('./width')[0].get('a'))


def getWidth(roadInfo):
    totalWidth = 0.0
    laneList = getAllLanes(roadInfo)
    for lane in laneList:
        totalWidth += getLaneWidth(lane)

    return totalWidth / len(laneList)


def getAllLanes(roadInfo):
    laneList = []
    lanes = roadInfo.findall('./lanes')[0]
    laneSection = lanes.findall('./laneSection')[0]

    lefts = laneSection.findall('./left')
    if len(lefts) > 0:
        left = lefts[0]
        leftLane = left.findall('./lane')
        for lane in leftLane:
            laneList.append(lane)

    rights = laneSection.findall('./right')
    if len(rights) > 0:
        right = rights[0]
        rightLane = right.findall('./lane')
        for lane in rightLane:
            laneList.append(lane)

    return laneList


def getJunctionRoads(junction, root):
    roadIdList = []

    for connection in junction.findall('./connection'):
        incomingRoadId = connection.get('incomingRoad')
        if incomingRoadId not in roadIdList:
            roadIdList.append(incomingRoadId)

        connectingRoadId = connection.get('connectingRoad')
        nextRoad = getRoadById(root, connectingRoadId)
        link = nextRoad.findall('./link')[0]
        predecessor = link.findall('./predecessor')[0]
        elementType = predecessor.get('elementType')
        if elementType is not None and elementType == 'road':
            roadId = predecessor.get('elementId')
            if roadId is not None and roadId not in roadIdList:
                roadIdList.append(roadId)

        successor = link.findall('./successor')[0]
        elementType = successor.get('elementType')
        if elementType is not None and elementType == 'road':
            roadId = successor.get('elementId')
            if roadId is not None and roadId not in roadIdList:
                roadIdList.append(roadId)

    return roadIdList


def isCrossing(roadInfoList):
    if len(roadInfoList) != 4:
        return False

    roadVector = []
    for roadInfo in roadInfoList:
        if not isStraightRoad(roadInfo):
            return False

        planVeiw = roadInfo.findall('./planView')[0]
        geometry = planVeiw.findall('./geometry')
        start = [float(geometry[0].get('x')), float(geometry[0].get('y'))]
        end = [float(geometry[-1].get('x')), float(geometry[-1].get('y'))]
        roadVector.append([end[0] - start[0], end[1] - start[1]])

    verticalCount, parallelCount = 0, 0
    angles = [getVectorAngle(roadVector[0], roadVector[1]),
              getVectorAngle(roadVector[0], roadVector[2]),
              getVectorAngle(roadVector[0], roadVector[3]),
              getVectorAngle(roadVector[1], roadVector[2]),
              getVectorAngle(roadVector[1], roadVector[3]),
              getVectorAngle(roadVector[2], roadVector[3])]
    for angle in angles:
        if isVertical(angle):
            verticalCount += 1
        if isParallel(angle):
            parallelCount += 1

    return verticalCount == 4 and parallelCount == 2