import math
import random
import z3
from z3 import Or
from src.common.constants import STRAIGHT_ROAD


def toNum(val):
    val = str(val)
    if val[-1] == '?':
        val = val[:-1]
    return float(val)


def solveChangeLane(end, lane, direction, laneCount, width, targetLane, roadType):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    tag = 1
    if targetLane < lane:
        tag = -1

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(speed >= endSpeed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [tag * (w2X - w1X) > 0] + \
                          [tag * (w3X - w2X) > 0] + \
                          [tag * (w4X - w3X) > 0] + \
                          [tag * (w5X - w4X) > 0] + \
                          [z3.And(w1X > (lane - 1) * width + 1, w1X < lane * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y > 2 * width] + \
                          [w3Y - w2Y > width] + \
                          [w4Y - w3Y > width] + \
                          [w5Y - w4Y > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [tag * (w2X - w1X) > 0] + \
                          [tag * (w3X - w2X) > 0] + \
                          [tag * (w4X - w3X) > 0] + \
                          [tag * (w5X - w4X) > 0] + \
                          [z3.And(w1X > (lane - 1) * width + 1, w1X < lane * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y > 2 * width] + \
                          [w3Y - w2Y > width] + \
                          [w4Y - w3Y > width] + \
                          [w5Y - w4Y > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
    if direction == 2:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5Y == endY] + \
                          [tag * (w2Y - w1Y) < 0] + \
                          [tag * (w3Y - w2Y) < 0] + \
                          [tag * (w4Y - w3Y) < 0] + \
                          [tag * (w5Y - w4Y) < 0] + \
                          [z3.And(w1Y > (- lane) * width + 1, w1Y < (- lane + 1) * width - 1)] + \
                          [w5X == endX] + \
                          [w2X - w1X > 2 * width] + \
                          [w3X - w2X > width] + \
                          [w4X - w3X > width] + \
                          [w5X - w4X > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
        else:
            positionExp = [w5Y == endY] + \
                          [tag * (w2Y - w1Y) < 0] + \
                          [tag * (w3Y - w2Y) < 0] + \
                          [tag * (w4Y - w3Y) < 0] + \
                          [tag * (w5Y - w4Y) < 0] + \
                          [z3.And(w1Y > (- lane) * width + 1, w1Y < (- lane + 1) * width) - 1] + \
                          [w5X == endX] + \
                          [w2X - w1X > 2 * width] + \
                          [w3X - w2X > width] + \
                          [w4X - w3X > width] + \
                          [w5X - w4X > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
    if direction == 3:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [tag * (w2X - w1X) < 0] + \
                          [tag * (w3X - w2X) < 0] + \
                          [tag * (w4X - w3X) < 0] + \
                          [tag * (w5X - w4X) < 0] + \
                          [z3.And(w1X > (- lane) * width + 1, w1X < (- lane + 1) * width - 1)] + \
                          [w5Y == endY] + \
                          [w1Y - w2Y > 2 * width] + \
                          [w2Y - w3Y > width] + \
                          [w3Y - w4Y > width] + \
                          [w4Y - w5Y > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [tag * (w2X - w1X) < 0] + \
                          [tag * (w3X - w2X) < 0] + \
                          [tag * (w4X - w3X) < 0] + \
                          [tag * (w5X - w4X) < 0] + \
                          [z3.And(w1X > (- lane) * width + 1, w1X < (- lane + 1) * width - 1)] + \
                          [w5Y == endY] + \
                          [w1Y - w2Y > 2 * width] + \
                          [w2Y - w3Y > width] + \
                          [w3Y - w4Y > width] + \
                          [w4Y - w5Y > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
    if direction == 4:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5Y == endY] + \
                          [tag * (w2Y - w1Y) > 0] + \
                          [tag * (w3Y - w2Y) > 0] + \
                          [tag * (w4Y - w3Y) > 0] + \
                          [tag * (w5Y - w4Y) > 0] + \
                          [z3.And(w1Y > (lane - 1) * width + 1, w1Y < lane * width - 1)] + \
                          [w5X == endX] + \
                          [w1X - w2X > 2 * width] + \
                          [w2X - w3X > width] + \
                          [w3X - w4X > width] + \
                          [w4X - w5X > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
        else:
            positionExp = [w5Y == endY] + \
                          [tag * (w2Y - w1Y) > 0] + \
                          [tag * (w3Y - w2Y) > 0] + \
                          [tag * (w4Y - w3Y) > 0] + \
                          [tag * (w5Y - w4Y) > 0] + \
                          [z3.And(w1Y > (lane - 1) * width + 1, w1Y < lane * width - 1)] + \
                          [w5X == endX] + \
                          [w1X - w2X > 2 * width] + \
                          [w2X - w3X > width] + \
                          [w3X - w4X > width] + \
                          [w4X - w5X > 2 * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 0.5, w2X == model[w2X] + 0.5,
                      w3X == model[w3X] + 0.5, w4X == model[w4X] + 0.5,
                      w1Y == model[w1Y] + 0.5, w2Y == model[w2Y] + 0.5,
                      w3Y == model[w3Y] + 0.5, w4Y == model[w4Y] + 0.5))

    return res[random.randint(0, len(res) - 1)]


def solveDriveInto(end, direction, laneCount, width, roadType):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(endSpeed <= speed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == (laneCount + 1) * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y - w5Y == - 2 * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == (laneCount + 1) * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y - w5Y == - 2 * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
    if direction == 2:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X - w5X == - 2 * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == - (laneCount + 1) * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X - w5Y == - 2 * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == - width - laneCount * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 3:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == - (laneCount + 1) * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y - w5Y == 2 * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == - width - laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y - w5Y == 2 * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 4:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X - w5Y == 2 * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == (laneCount + 1) * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X - w5Y == 2 * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == (laneCount + 1) * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w2X == model[w2X] + 0.2, w3X == model[w3X] + 0.2,
                      w4X == model[w4X] + 0.2, w5X == model[w5X] + 0.2,
                      w2Y == model[w2Y] + 0.2, w3Y == model[w3Y] + 0.2,
                      w4Y == model[w4Y] + 0.2, w5Y == model[w5Y] + 0.2))

    return res[random.randint(0, len(res) - 1)]


def solveDriveOff(end, lane, direction, laneCount, width, roadType):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(endSpeed <= speed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X > (lane - 1) * width + 1] + \
                          [w1X < lane * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == - 2 * laneCount * width] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) > 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X > (lane - 1) * width + 1] + \
                          [w1X < lane * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == - 3 * laneCount * width] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) > 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0]
    if direction == 2:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == - 2 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y > (- lane) * width + 1] + \
                          [w1Y < (- lane + 1) * width - 1] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) > 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == - 3 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y > (- lane) * width + 1] + \
                          [w1Y < (- lane + 1) * width - 1] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) > 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0]
    if direction == 3:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X > (- lane) * width + 1] + \
                          [w1X < (- lane + 1) * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == 2 * laneCount * width] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) < 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X > (- lane) * width + 1] + \
                          [w1X < (- lane + 1) * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == 3 * laneCount * width] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) < 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0]
    if direction == 4:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == 2 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y > (lane - 1) * width + 1] + \
                          [w1Y < lane * width - 1] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) < 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == 3 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y > (lane - 1) * width + 1] + \
                          [w1Y < lane * width - 1] + \
                          [w4Y - w1Y - (w5Y - w1Y) * (w4X - w1X) / (w5X - w1X) < 0] + \
                          [w3Y - w1Y - (w4Y - w1Y) * (w3X - w1X) / (w4X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w2X == model[w2X] + 0.5, w3X == model[w3X] + 0.5,
                      w4X == model[w4X] + 0.5, w5X == model[w5X] + 0.5,
                      w2Y == model[w2Y] + 0.5, w3Y == model[w3Y] + 0.5,
                      w4Y == model[w4Y] + 0.5, w5Y == model[w5Y] + 0.5))

    return res[random.randint(0, len(res) - 1)]


def solveFollowLane(end, direction, width):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(speed >= endSpeed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        positionExp = [w1X == w5X] + \
                      [w2X == w5X] + \
                      [w3X == w5X] + \
                      [w4X == w5X] + \
                      [w5X == endX] + \
                      [w2Y - w1Y > 0] + \
                      [w3Y - w2Y > 0] + \
                      [w4Y - w3Y > 0] + \
                      [z3.And(w5Y == endY, w5Y - w4Y > 0, w5Y - w1Y > 4 * width)]
    if direction == 2:
        positionExp = [w1Y == w5Y] + \
                      [w2Y == w5Y] + \
                      [w3Y == w5Y] + \
                      [w4Y == w5Y] + \
                      [w5Y == endY] + \
                      [w2X - w1X > 0] + \
                      [w3X - w2X > 0] + \
                      [w4X - w3X > 0] + \
                      [z3.And(w5X == endX, w5X - w4X > 0, w5X - w1X > 4 * width)]
    if direction == 3:
        positionExp = [w1X == w5X] + \
                      [w2X == w5X] + \
                      [w3X == w5X] + \
                      [w4X == w5X] + \
                      [w5X == endX] + \
                      [w1Y - w2Y > 0] + \
                      [w2Y - w3Y > 0] + \
                      [w3Y - w4Y > 0] + \
                      [z3.And(w5Y == endY, w4Y - w5Y > 0, w1Y - w5Y > 4 * width)]
    if direction == 4:
        positionExp = [w1Y == w5Y] + \
                      [w2Y == w5Y] + \
                      [w3Y == w5Y] + \
                      [w4Y == w5Y] + \
                      [w5Y == endY] + \
                      [w1X - w2X > 0] + \
                      [w2X - w3X > 0] + \
                      [w3X - w4X > 0] + \
                      [z3.And(w5X == endX, w4X - w5X > 0, w1X - w5X > 4 * width)]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()
        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 2, w2X == model[w2X] + 2,
                      w3X == model[w3X] + 2, w4X == model[w4X] + 2,
                      w1Y == model[w1Y] + 2, w2Y == model[w2Y] + 2,
                      w3Y == model[w3Y] + 2, w4Y == model[w4Y] + 2))

    return res[random.randint(0, len(res) - 1)]


def solveGoAcross(end, direction, laneCount, width):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(speed >= endSpeed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        positionExp = [w1X == w5X] + \
                      [w2X == w5X] + \
                      [w3X == w5X] + \
                      [w4X == w5X] + \
                      [w5X == endX] + \
                      [w5Y - w1Y == 6 * laneCount * width] + \
                      [w2Y - w1Y > 0] + \
                      [w3Y - w2Y > 0] + \
                      [w4Y - w3Y > 0] + \
                      [z3.And(w5Y == endY, w5Y - w4Y > 0)]
    if direction == 2:
        positionExp = [w1Y == w5Y] + \
                      [w2Y == w5Y] + \
                      [w3Y == w5Y] + \
                      [w4Y == w5Y] + \
                      [w5Y == endY] + \
                      [w5X - w1X == 6 * laneCount * width] + \
                      [w2X - w1X > 0] + \
                      [w3X - w2X > 0] + \
                      [w4X - w3X > 0] + \
                      [z3.And(w5X == endX, w5X - w4X > 0)]
    if direction == 3:
        positionExp = [w1X == w5X] + \
                      [w2X == w5X] + \
                      [w3X == w5X] + \
                      [w4X == w5X] + \
                      [w5X == endX] + \
                      [w1Y - w5Y == 6 * laneCount * width] + \
                      [w1Y - w2Y > 0] + \
                      [w2Y - w3Y > 0] + \
                      [w3Y - w4Y > 0] + \
                      [z3.And(w5Y == endY, w4Y - w5Y > 0)]
    if direction == 4:
        positionExp = [w1Y == w5Y] + \
                      [w2Y == w5Y] + \
                      [w3Y == w5Y] + \
                      [w4Y == w5Y] + \
                      [w5Y == endY] + \
                      [w1X - w5X == 6 * laneCount * width] + \
                      [w1X - w2X > 0] + \
                      [w2X - w3X > 0] + \
                      [w3X - w4X > 0] + \
                      [z3.And(w5X == endX, w4X - w5X > 0)]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()
        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 2, w2X == model[w2X] + 2,
                      w3X == model[w3X] + 2, w4X == model[w4X] + 2,
                      w1Y == model[w1Y] + 2, w2Y == model[w2Y] + 2,
                      w3Y == model[w3Y] + 2, w4Y == model[w4Y] + 2))

    return res[random.randint(0, len(res) - 1)]


def solveHalfU(end, lane, direction, laneCount, width, roadType):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(endSpeed <= speed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X > (lane - 1) * width + 1] + \
                          [w1X < lane * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == - width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X > (lane - 1) * width + 1] + \
                          [w1X < lane * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == - width - laneCount * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
    if direction == 2:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == - width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y > - laneCount * width + 1] + \
                          [w1Y < - (laneCount - 1) * width - 1] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == - width - laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y > (- lane) * width + 1] + \
                          [w1Y < (- lane + 1) * width - 1] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 3:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X > - lane * width + 1] + \
                          [w1X < - (lane - 1) * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X > (- lane) * width + 1] + \
                          [w1X < (- lane + 1) * width - 1] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == (laneCount + 1) * width] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 4:
        if roadType == STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y < lane * width - 1] + \
                          [w1Y > (lane - 1) * width + 1] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == (laneCount + 1) * width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y < lane * width - 1] + \
                          [w1Y > (lane - 1) * width + 1] + \
                          [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                          [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w2X == model[w2X] + 0.2, w3X == model[w3X] + 0.2,
                      w4X == model[w4X] + 0.2, w5X == model[w5X] + 0.2,
                      w2Y == model[w2Y] + 0.2, w3Y == model[w3Y] + 0.2,
                      w4Y == model[w4Y] + 0.2, w5Y == model[w5Y] + 0.2))

    return res[random.randint(0, len(res) - 1)]


def solveMove(waypoint, dist):
    x1, y1, x2, y2 = waypoint[-2][0], waypoint[-2][1], waypoint[-1][0], waypoint[-1][1]

    x = z3.Real("x")
    y = z3.Real("y")
    k = z3.Real("k")

    exp = [k * (x2 - x1) == x - x1] + \
          [k * (y2 - y1) == y - y1] + \
          [k > 1] + \
          [(x - x2) ** 2 + (y - y2) ** 2 == dist ** 2]

    solver = z3.Solver()
    solver.add(exp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=2)

    if solver.check() == z3.sat:
        model = solver.model()
        return [toNum(model.evaluate(x)), toNum(model.evaluate(y)), waypoint[-1][2]]

    return [0, 0]


def solveRetrograde(end, lane, direction, laneCount, width, roadType):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(speed >= endSpeed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w1X - w2X > 0] + \
                          [w2X - w3X > 0] + \
                          [w3X - w4X > 0] + \
                          [w4X - w5X > 0] + \
                          [z3.And(w1X > (lane - 1) * width + 1, w1X < lane * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y > 0] + \
                          [w3Y - w2Y > 0] + \
                          [w4Y - w3Y > 0] + \
                          [w5Y - w4Y > 0] + \
                          [w5Y - w1Y > 2 * laneCount * width]
        else:
            positionExp = [w5X == endX] + \
                          [w1X - w2X > 0] + \
                          [w2X - w3X > 0] + \
                          [w3X - w4X > 0] + \
                          [w4X - w5X > 0] + \
                          [z3.And(w1X > (lane - 1) * width + 1, w1X < lane * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y > 0] + \
                          [w3Y - w2Y > 0] + \
                          [w4Y - w3Y > 0] + \
                          [w5Y - w4Y > 0] + \
                          [w5Y - w1Y > 2 * laneCount * width]
    if direction == 2:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X - w1X > 0] + \
                          [w3X - w2X > 0] + \
                          [w4X - w3X > 0] + \
                          [w5X - w4X > 0] + \
                          [w5X - w1X > 2 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y > 0] + \
                          [w3Y - w2Y > 0] + \
                          [w4Y - w3Y > 0] + \
                          [w5Y - w4Y > 0] + \
                          [w1Y > (- lane) * width + 1] + \
                          [w1Y < (- lane + 1) * width - 1]
        else:
            positionExp = [w5X == endX] + \
                          [w2X - w1X > 0] + \
                          [w3X - w2X > 0] + \
                          [w4X - w3X > 0] + \
                          [w5X - w4X > 0] + \
                          [w5X - w1X > 2 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y > 0] + \
                          [w3Y - w2Y > 0] + \
                          [w4Y - w3Y > 0] + \
                          [w5Y - w4Y > 0] + \
                          [w1Y > - lane * width + 1] + \
                          [w1Y < (- lane + 1) * width - 1]
    if direction == 3:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w1X - w2X < 0] + \
                          [w2X - w3X < 0] + \
                          [w3X - w4X < 0] + \
                          [w4X - w5X < 0] + \
                          [z3.And(w1X > (- lane) * width + 1, w1X < (- lane + 1) * width - 1)] + \
                          [w5Y == endY] + \
                          [w1Y - w2Y > 0] + \
                          [w2Y - w3Y > 0] + \
                          [w3Y - w4Y > 0] + \
                          [w4Y - w5Y > 0] + \
                          [w1Y - w5Y > 2 * laneCount * width]

        else:
            positionExp = [w5X == endX] + \
                          [w1X - w2X < 0] + \
                          [w2X - w3X < 0] + \
                          [w3X - w4X < 0] + \
                          [w4X - w5X < 0] + \
                          [z3.And(w1X > - lane * width + 1, w1X < (- lane + 1) * width - 1)] + \
                          [w5Y == endY] + \
                          [w1Y - w2Y > 0] + \
                          [w2Y - w3Y > 0] + \
                          [w3Y - w4Y > 0] + \
                          [w4Y - w5Y > 0] + \
                          [w1Y - w5Y > 2 * laneCount * width]
    if direction == 4:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w1X - w2X > 0] + \
                          [w2X - w3X > 0] + \
                          [w3X - w4X > 0] + \
                          [w4X - w5X > 0] + \
                          [w1X - w5X > 2 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y < 0] + \
                          [w3Y - w2Y < 0] + \
                          [w4Y - w3Y < 0] + \
                          [w5Y - w4Y < 0] + \
                          [w1Y > (lane - 1) * width + 1] + \
                          [w1Y < lane * width - 1]
        else:
            positionExp = [w5X == endX] + \
                          [w1X - w2X > 0] + \
                          [w2X - w3X > 0] + \
                          [w3X - w4X > 0] + \
                          [w4X - w5X > 0] + \
                          [w1X - w5X > 2 * laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y - w1Y < 0] + \
                          [w3Y - w2Y < 0] + \
                          [w4Y - w3Y < 0] + \
                          [w5Y - w4Y < 0] + \
                          [w1Y > (lane - 1) * width + 1] + \
                          [w1Y < lane * width - 1]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 0.5, w2X == model[w2X] + 0.5,
                      w3X == model[w3X] + 0.5, w4X == model[w4X] + 0.5,
                      w1Y == model[w1Y] + 0.5, w2Y == model[w2Y] + 0.5,
                      w3Y == model[w3Y] + 0.5, w4Y == model[w4Y] + 0.5))

    return res[random.randint(0, len(res) - 1)]


def solveSpin(x, y, vectorX, vectorY):
    if vectorY == 0:
        return [x, y]

    dist2 = x * x + y * y
    newX, newY = z3.Real("newX"), z3.Real("newY")
    exp = [newX * newX + newY * newY == dist2] + \
          [vectorY * (x * newY - y * newX) > 0] + \
          [vectorX * dist2 == ((newX * x) + (newY * y)) * math.sqrt(vectorX * vectorX + vectorY * vectorY)]

    solver = z3.Solver()
    solver.add(exp)
    z3.set_option(rational_to_decimal=True, precision=2)

    if solver.check() == z3.sat:
        model = solver.model()
        newX, newY = toNum(model.evaluate(newX)), toNum(model.evaluate(newY))
        return newX, newY

    return 0, 0


def solveStop(end):
    return [[end[0], end[1], 0]]


def solveTurnAround(end, lane, direction, laneCount, width, roadType):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(endSpeed <= speed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w3X == 0] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [z3.And(w1X > (lane - 1) * width + 1, w1X < lane * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w3Y == - laneCount * width] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == - width - laneCount * width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w3X == 0] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [z3.And(w1X > (lane - 1) * width + 1, w1X < lane * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w3Y == 0] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [w1Y == - width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
    if direction == 2:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w3X == - laneCount * width] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == - width - laneCount * width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w3Y == 0] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [z3.And(w1Y > (- lane) * width + 1, w1Y < (- lane + 1) * width - 1)] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w3X == 0] + \
                          [w4X < w3X] + \
                          [w5X < w4X] + \
                          [w1X == - width] + \
                          [w5Y == endY] + \
                          [w2Y > w1Y] + \
                          [w3Y > w2Y] + \
                          [w3Y == 0] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [z3.And(w1Y > (- lane) * width + 1, w1Y < (- lane + 1) * width - 1)] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0]
    if direction == 3:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w3X == 0] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [z3.And(w1X > (- lane) * width + 1, w1X < (- lane + 1) * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w3Y == laneCount * width] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == laneCount * width + width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X > w1X] + \
                          [w3X > w2X] + \
                          [w3X == 0] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [z3.And(w1X > (- lane) * width + 1, w1X < (- lane + 1) * width - 1)] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w3Y == 0] + \
                          [w4Y > w3Y] + \
                          [w5Y > w4Y] + \
                          [w1Y == width] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
    if direction == 4:
        if roadType != STRAIGHT_ROAD:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w3X == laneCount * width] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == laneCount * width + width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w3Y == 0] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [z3.And(w1Y > (lane - 1) * width + 1, w1Y < lane * width - 1)] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]
        else:
            positionExp = [w5X == endX] + \
                          [w2X < w1X] + \
                          [w3X < w2X] + \
                          [w3X == 0] + \
                          [w4X > w3X] + \
                          [w5X > w4X] + \
                          [w1X == width] + \
                          [w5Y == endY] + \
                          [w2Y < w1Y] + \
                          [w3Y < w2Y] + \
                          [w3Y == 0] + \
                          [w4Y < w3Y] + \
                          [w5Y < w4Y] + \
                          [z3.And(w1Y > (lane - 1) * width + 1, w1Y < lane * width - 1)] + \
                          [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                          [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)


    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 0.5, w2X == model[w2X] + 0.5,
                      w3X == model[w3X] + 0.5, w4X == model[w4X] + 0.5,
                      w1Y == model[w1Y] + 0.5, w2Y == model[w2Y] + 0.5,
                      w3Y == model[w3Y] + 0.5, w4Y == model[w4Y] + 0.5))

    return res[random.randint(0, len(res) - 1)]


def solveTurnLeft(end, lane, direction, laneCount, width):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(endSpeed <= speed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        positionExp = [w5X == endX] + \
                      [w2X < w1X] + \
                      [w3X < w2X] + \
                      [w4X < w3X] + \
                      [w5X < w4X] + \
                      [w1X > (lane - 1) * width + 1] + \
                      [w1X < lane * width - 1] + \
                      [w5Y == endY] + \
                      [w2Y > w1Y] + \
                      [w3Y > w2Y] + \
                      [w4Y > w3Y] + \
                      [w5Y > w4Y] + \
                      [w1Y == - laneCount * width] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
    if direction == 2:
        positionExp = [w5X == endX] + \
                      [w2X > w1X] + \
                      [w3X > w2X] + \
                      [w4X > w3X] + \
                      [w5X > w4X] + \
                      [w1X == - laneCount * width] + \
                      [w5Y == endY] + \
                      [w2Y > w1Y] + \
                      [w3Y > w2Y] + \
                      [w4Y > w3Y] + \
                      [w5Y > w4Y] + \
                      [w1Y > (- lane) * width + 1] + \
                      [w1Y < (- lane + 1) * width - 1] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 3:
        positionExp = [w5X == endX] + \
                      [w2X > w1X] + \
                      [w3X > w2X] + \
                      [w4X > w3X] + \
                      [w5X > w4X] + \
                      [w1X > (- lane) * width + 1] + \
                      [w1X < (- lane + 1) * width - 1] + \
                      [w5Y == endY] + \
                      [w2Y < w1Y] + \
                      [w3Y < w2Y] + \
                      [w4Y < w3Y] + \
                      [w5Y < w4Y] + \
                      [w1Y == laneCount * width] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 4:
        positionExp = [w5X == endX] + \
                      [w2X < w1X] + \
                      [w3X < w2X] + \
                      [w4X < w3X] + \
                      [w5X < w4X] + \
                      [w1X == laneCount * width] + \
                      [w5Y == endY] + \
                      [w2Y < w1Y] + \
                      [w3Y < w2Y] + \
                      [w4Y < w3Y] + \
                      [w5Y < w4Y] + \
                      [w1Y > (lane - 1) * width + 1] + \
                      [w1Y < lane * width - 1] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)

    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 1, w2X == model[w2X] + 1,
                      w3X == model[w3X] + 1, w4X == model[w4X] + 1,
                      w1Y == model[w1Y] + 1, w2Y == model[w2Y] + 1,
                      w3Y == model[w3Y] + 1, w4Y == model[w4Y] + 1))

    return res[random.randint(0, len(res) - 1)]


def solveTurnRight(end, lane, direction, laneCount, width):
    endX = end[0]
    endY = end[1]
    endSpeed = end[2]

    w1X = z3.Real("w1X")
    w2X = z3.Real("w2X")
    w3X = z3.Real("w3X")
    w4X = z3.Real("w4X")
    w5X = z3.Real("w5X")
    w1Y = z3.Real("w1Y")
    w2Y = z3.Real("w2Y")
    w3Y = z3.Real("w3Y")
    w4Y = z3.Real("w4Y")
    w5Y = z3.Real("w5Y")
    speed = z3.Real("speed")

    speedExp = [z3.And(endSpeed <= speed, speed <= endSpeed)]

    positionExp = None
    if direction == 1:
        positionExp = [w5X == endX] + \
                      [w2X > w1X] + \
                      [w3X > w2X] + \
                      [w4X > w3X] + \
                      [w5X > w4X] + \
                      [w1X > (lane - 1) * width + 1] + \
                      [w1X < lane * width - 1] + \
                      [w5Y == endY] + \
                      [w2Y > w1Y] + \
                      [w3Y > w2Y] + \
                      [w4Y > w3Y] + \
                      [w5Y > w4Y] + \
                      [w1Y == - laneCount * width] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
    if direction == 2:
        positionExp = [w5X == endX] + \
                      [w2X > w1X] + \
                      [w3X > w2X] + \
                      [w4X > w3X] + \
                      [w5X > w4X] + \
                      [w1X == - laneCount * width] + \
                      [w5Y == endY] + \
                      [w2Y < w1Y] + \
                      [w3Y < w2Y] + \
                      [w4Y < w3Y] + \
                      [w5Y < w4Y] + \
                      [w1Y > (- lane) * width + 1] + \
                      [w1Y < (- lane + 1) * width - 1] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) > 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) > 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) > 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) > 0]
    if direction == 3:
        positionExp = [w5X == endX] + \
                      [w2X < w1X] + \
                      [w3X < w2X] + \
                      [w4X < w3X] + \
                      [w5X < w4X] + \
                      [w1X > (- lane) * width + 1] + \
                      [w1X < (- lane + 1) * width - 1] + \
                      [w5Y == endY] + \
                      [w2Y < w1Y] + \
                      [w3Y < w2Y] + \
                      [w4Y < w3Y] + \
                      [w5Y < w4Y] + \
                      [w1Y == laneCount * width] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]
    if direction == 4:
        positionExp = [w5X == endX] + \
                      [w2X < w1X] + \
                      [w3X < w2X] + \
                      [w4X < w3X] + \
                      [w5X < w4X] + \
                      [w1X == laneCount * width] + \
                      [w5Y == endY] + \
                      [w2Y > w1Y] + \
                      [w3Y > w2Y] + \
                      [w4Y > w3Y] + \
                      [w5Y > w4Y] + \
                      [w1Y > (lane - 1) * width + 1] + \
                      [w1Y < lane * width - 1] + \
                      [w3Y - w1Y - (w5Y - w1Y) * (w3X - w1X) / (w5X - w1X) < 0] + \
                      [w2Y - w1Y - (w3Y - w1Y) * (w2X - w1X) / (w3X - w1X) < 0] + \
                      [w4Y - w3Y - (w5Y - w3Y) * (w4X - w3X) / (w5X - w3X) < 0] + \
                      [w3Y - w2Y - (w4Y - w2Y) * (w3X - w2X) / (w4X - w2X) < 0]

    solver = z3.Solver()
    solver.add(speedExp + positionExp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=1)


    res = []
    i = 0
    while solver.check() == z3.sat and i < 1000:
        i += 1
        model = solver.model()

        waypoints = [[toNum(model.evaluate(w1X)), toNum(model.evaluate(w1Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w2X)), toNum(model.evaluate(w2Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w3X)), toNum(model.evaluate(w3Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w4X)), toNum(model.evaluate(w4Y)), toNum(model.evaluate(speed))],
                     [toNum(model.evaluate(w5X)), toNum(model.evaluate(w5Y)), toNum(model.evaluate(speed))]]
        res.append(waypoints)

        solver.add(Or(w1X == model[w1X] + 0.2, w2X == model[w2X] + 0.2,
                      w3X == model[w3X] + 0.2, w4X == model[w4X] + 0.2,
                      w1Y == model[w1Y] + 0.2, w2Y == model[w2Y] + 0.2,
                      w3Y == model[w3Y] + 0.2, w4Y == model[w4Y] + 0.2))

    return res[random.randint(0, len(res) - 1)]


def solveIntersection(line1, line2):
    x = z3.Real("x")
    y = z3.Real("y")

    x11 = line1[0][0]
    y11 = line1[0][1]
    x12 = line1[1][0]
    y12 = line1[1][1]
    x21 = line2[0][0]
    y21 = line2[0][1]
    x22 = line2[1][0]
    y22 = line2[1][1]

    exp = [(y11 - y) * (x12 - x) == (y12 - y) * (x11 - x)] + \
          [(y21 - y) * (x22 - x) == (y22 - y) * (x21 - x)]

    solver = z3.Solver()
    solver.add(exp)
    z3.set_option(rational_to_decimal=True)
    z3.set_option(precision=2)

    if solver.check() == z3.sat:
        model = solver.model()
        x = toNum(model.evaluate(x))
        y = toNum(model.evaluate(y))
        return [x, y]

    return [0, 0]