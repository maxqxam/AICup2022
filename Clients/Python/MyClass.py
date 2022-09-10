import random
from main import GameState
from main import Action
from main import MapType



def getFurthestOptionFromTail(options: list, p_tail: list) -> tuple[int, int]:
    aveDist: float = 0.0
    maxAveDist: float = 0.0
    maxAveDistIndex: int = 0

    for i in range(0, len(options)):
        aveDist = getAverageDistance(options[i], p_tail)
        if i == 0 or aveDist > maxAveDist:
            maxAveDist = aveDist
            maxAveDistIndex = i

    return options[maxAveDistIndex]

def get_connected_nodes(self:GameState, coordinates):
    i, j = coordinates
    list_coordinates = [[i, j + 1], [i, j - 1], [i - 1, j], [i + 1, j]]

    forbidden_types = [MapType.WALL.value,MapType.OUT_OF_MAP.value,MapType.AGENT.value]

    awesome_result =  [list(i.coordinates) for i in self.map.grid if list(i.coordinates) in
            list_coordinates and i.type not in forbidden_types]

    if len(awesome_result)==0: return list_coordinates

    return awesome_result

def getAverageDistance(point: tuple[int, int], pointList: list) -> float:
    distSum: int = 0
    distCounter: int = 0

    for i in range(0, len(pointList)):
        distCounter += 1
        p2 = pointList[i]
        dist = abs(point[0] - p2[0]) + abs(point[1] - p2[1])
        distSum += dist

    if distCounter == 0: return 0

    return distSum / distCounter

def getStepTowards(source, destination) -> Action:
    if source[0] < destination[0]:
        return Action.MOVE_DOWN
    if source[0] > destination[0]:
        return Action.MOVE_UP

    if source[1] < destination[1]:
        return Action.MOVE_RIGHT
    if source[1] > destination[1]:
        return Action.MOVE_LEFT

    return Action.STAY



tail: list = []
TAIL_MAX_SIZE: int = 10


def getAction(self: GameState) -> Action:
    tail.append(list(self.location))

    if len(tail) > TAIL_MAX_SIZE:
        tail.pop(0)

    choices = get_connected_nodes(self,(self.location[0],self.location[1]))
    goal = getFurthestOptionFromTail(choices,tail)

    return getStepTowards(self.location, goal)
