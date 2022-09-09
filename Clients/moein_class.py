import random
from main import Action
from main import GameState
from main import MapType

recent_locations: list = []
recent_moves: list = []
RECENT_MOVES_MAX_SIZE = 10


def getStepTowards(source: tuple[int, int], destination: tuple[int, int]) -> Action:
    if source[0] < destination[0]:
        return Action.MOVE_DOWN
    elif source[0] > destination[0]:
        return Action.MOVE_UP

    # -----

    if source[1] < destination[1]:
        return Action.MOVE_RIGHT
    elif source[1] > destination[1]:
        return Action.MOVE_LEFT

    return Action.STAY



def getChoicesPositions(view: GameState) -> list:
    result: list = []
    possible_choices = [[i[0],i[1]] for i in [view.location, view.location,
                                          view.location, view.location,
                                          view.location]]

    possible_choices[0][0] -= 1
    possible_choices[1][0] += 1
    possible_choices[2][1] -= 1
    possible_choices[3][1] += 1

    for i in view.map.grid:
        if i.coordinates in possible_choices:
            if i.data==MapType.WALL.value or i.data==MapType.OUT_OF_MAP.value:
                result.append(i.coordinates)


    return result



def getLeastOccurredElement(Collection: list):
    every_direction = [Action.MOVE_DOWN, Action.MOVE_UP, Action.MOVE_LEFT, Action.MOVE_RIGHT]

    minOccurrence: int = 1000 * 1000
    minOccurrenceIndex = 0

    for i in range(0, len(every_direction)):
        occurrence = Collection.count(every_direction[i])
        if occurrence < minOccurrence:
            minOccurrence = occurrence
            minOccurrenceIndex = i

    return every_direction[minOccurrenceIndex]


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


def getFurthestOptionFromTail(options: list, tail: list) -> tuple[int, int]:
    aveDist: float = 0.0
    maxAveDist: float = 0.0
    maxAveDistIndex: int = 0

    for i in range(0, len(options)):
        aveDist = getAverageDistance(options[i], tail)
        if i == 0 or aveDist > maxAveDist:
            maxAveDist = aveDist
            maxAveDistIndex = i

    return options[maxAveDistIndex]


def getAction(view: GameState) -> Action:

    choices_positions = getChoicesPositions(view)

    view.debug_log+="Possible choices : "+str(choices_positions)+"\n"

    if len(choices_positions)==0: return Action.STAY

    destination = random.choice(choices_positions)
    move = getStepTowards(
        view.location,
        tuple(destination)
    )


    return move
