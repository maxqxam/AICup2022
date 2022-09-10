import random
from main import GameState
from main import Action
from main import MapType

permanentTypes = [i.value for i in [MapType.WALL,MapType.EMPTY,MapType.TREASURY,MapType.FOG]]

class Tile:
    def __init__(self, pos: tuple[int, int], Type: MapType):
        self.pos: tuple[int, int] = pos
        self.Type = Type


class Brain:
    firstIteration:bool = True

    def __init__(self):
        self.everyTile = None

    def initTiles(self,  mapDimensions: tuple[int, int]) -> None:
        self.everyTile = []
        for i in range(0, mapDimensions[0]):
            for c in range(0, mapDimensions[1]):
                self.everyTile.append(Tile((i, c), MapType.UNKNOWN))

    def updateTiles(self,visibleTiles:list) -> None:

        for i in range(0,len(self.everyTile)):
            for c in visibleTiles:
                if tuple(self.everyTile[i].pos) == tuple(c.coordinates) and \
                        c.type in permanentTypes:
                    self.everyTile[i].Type = c.type

    def getVisiblePlacesString(self) -> str:
        text:str = ""

        last_row = 0

        for i in self.everyTile:
            if i.pos[0]!=last_row: text+="\n"
            last_row = i.pos[0]
            if i.Type==MapType.UNKNOWN: text+=str(i.Type)
            else: text+=str(i.Type)

        return text+"\n"


class Step:
    0


def getShortestPath() -> list:
    result:list = []

    return result



firstIteration: bool = True
brain: Brain = Brain()


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


def get_connected_nodes(self: GameState, coordinates):
    i, j = coordinates
    list_coordinates = [[i, j + 1], [i, j - 1], [i - 1, j], [i + 1, j]]

    forbidden_types = [MapType.WALL.value, MapType.OUT_OF_MAP.value, MapType.AGENT.value]

    awesome_result = [list(i.coordinates) for i in self.map.grid if list(i.coordinates) in
                      list_coordinates and i.type not in forbidden_types]

    if len(awesome_result) == 0: return list_coordinates

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

    if Brain.firstIteration:
        brain.initTiles((self.map.height,self.map.width))
        Brain.firstIteration = False

    brain.updateTiles(self.map.grid)

    if len(tail) > TAIL_MAX_SIZE:
        tail.pop(0)

    choices = get_connected_nodes(self, (self.location[0], self.location[1]))
    goal = getFurthestOptionFromTail(choices, tail)

    try:
        self.debug_log+=brain.getVisiblePlacesString()
    except Exception as e:
        self.debug_log+="ERROR"+str(e)+"\n"

    brain.firstIteration = False
    return getStepTowards(self.location, goal)
