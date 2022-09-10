import random
from main import GameState
from main import Action
from main import MapType

permanentTypes = [i.value for i in [MapType.WALL, MapType.EMPTY, MapType.TREASURY, MapType.FOG]]
temporaryTypes = [i.value for i in [MapType.GOLD, MapType.AGENT]]
blockingTypes = [i.value for i in [MapType.WALL, MapType.AGENT, MapType.OUT_OF_MAP]]


class Tile:
    def __init__(self, pos: tuple[int, int], Type: MapType, tempType: MapType):
        self.pos: tuple[int, int] = pos
        self.Type = Type
        self.tempType = tempType


class Brain:
    firstIteration: bool = True

    def __init__(self):
        self.everyTile = None
        self.everyTileAsPos = None

    def initTiles(self, mapDimensions: tuple[int, int]) -> None:
        self.everyTile = []
        self.everyTileAsPos = []
        for i in range(0, mapDimensions[0]):
            for c in range(0, mapDimensions[1]):
                Type = MapType.UNKNOWN
                self.everyTile.append(Tile((i, c), Type, Type))
                self.everyTileAsPos.append((i, c))

    def updateTiles(self, visibleTiles: list) -> None:

        for i in range(0, len(self.everyTile)):
            for c in visibleTiles:
                if tuple(self.everyTile[i].pos) == tuple(c.coordinates):
                    if c.type in permanentTypes:
                        self.everyTile[i].Type = c.type
                    elif c.type in temporaryTypes:
                        self.everyTile[i].tempType = c.type

    def flushTiles(self):
        for i in range(0,len(self.everyTile)):
            self.everyTile[i].tempType = MapType.UNKNOWN


    def getVisiblePlacesString(self) -> str:
        text: str = ""

        last_row = 0

        for i in self.everyTile:
            if i.pos[0] != last_row: text += "\n"
            last_row = i.pos[0]
            if i.Type == MapType.UNKNOWN:
                text += str(i.Type)
            else:
                text += str(i.Type)

        return text + "\n"


class Step:
    def __init__(self, currentTile: Tile, parentTile: Tile, layer: int):
        self.cTile = currentTile
        self.pTile = parentTile
        self.layer = layer


def getShortestPath(everyTile: list, srcIndex: int, dstIndex: int) -> list:
    result: list = []

    return result


firstIteration: bool = True
brain: Brain = Brain()


def getFurthestOptionFromTail(options: list, p_tail: list) -> tuple[int, int]:
    aveDist: float = 0.0
    maxAveDist: float = 0.0
    maxAveDistIndexList:list = []

    for i in range(0, len(options)):
        aveDist = getAverageDistance(options[i], p_tail)
        if i == 0 or aveDist > maxAveDist:
            maxAveDist = aveDist

    for i in range(0, len(options)):
        aveDist = getAverageDistance(options[i], p_tail)
        if aveDist==maxAveDist:
            maxAveDistIndexList.append(i)

    return options[random.choice(maxAveDistIndexList)]


def get_connected_nodes(everyTile:list, pos: tuple[int, int]) -> list:
    list_coordinates = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]

    # return list_coordinates
    return [i.pos for i in everyTile if i.pos in list_coordinates and (i.Type not in blockingTypes
                                                                       and i.tempType not in blockingTypes)]


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

    if Brain.firstIteration:
        brain.initTiles((self.map.height, self.map.width))

    brain.updateTiles(self.map.grid)

    tail.append(list(self.location))

    if len(tail) > TAIL_MAX_SIZE:
        tail.pop(0)

    choices = get_connected_nodes(brain.everyTile,(self.location[0], self.location[1]))
    self.debug_log+="\nLength of choices : "+str(len(choices))+"\n"

    if len(choices)!=0:
        goal = getFurthestOptionFromTail(choices, tail)
    else:
        goal = self.location

    self.debug_log += brain.getVisiblePlacesString()

    brain.flushTiles()

    return getStepTowards(self.location, goal)
