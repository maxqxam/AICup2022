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
                Type = MapType.UNKNOWN.value
                self.everyTile.append(Tile((i, c), Type, Type))
                self.everyTileAsPos.append((i, c))

    def updateTiles(self, visibleTiles: list) -> None:

        for i in range(0, len(self.everyTile)):
            for c in visibleTiles:
                if tuple(self.everyTile[i].pos) == tuple(c.coordinates):
                    if c.type.value in permanentTypes:
                        self.everyTile[i].Type = c.type.value
                        if c.type == MapType.TREASURY:
                            if c.data != -1:
                                self.everyTile[i].tempType = MapType.AGENT.value

                    elif c.type.value in temporaryTypes:
                        self.everyTile[i].tempType = c.type.value

                    # if c.data!=-1:
                    #     self.everyTile[i].tempType = MapType.AGENT.value

    def flushTiles(self):
        for i in range(0, len(self.everyTile)):
            self.everyTile[i].tempType = MapType.UNKNOWN.value

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
    def __init__(self, currentPos: tuple[int, int], parentPos: tuple[int, int], layer: int):
        self.cPos = currentPos
        self.pPos = parentPos
        self.layer = layer

    def __str__(self):
        return "[ " + str(self.cPos) + " , " + str(self.pPos) + " , " + str(self.layer) + " ]"


# BFS algorithm
# If the result list is empty it means the algorithm could not find the answer
# Either way, the second element in the list is your next turn
def getShortestPath(everyTile: list, src: tuple[int, int], dst: tuple[int, int]) -> list:
    # layer 0
    # layer 1
    validTiles: list = [i.pos for i in everyTile if (i.Type not in blockingTypes and
                                                     i.tempType not in blockingTypes)]
    result: list = []
    stack: list = [Step(src, src, 0)]  # initial layer
    stackPos: list = [src]

    if src == dst:
        return [stack[0], stack[0]]

    ATL_init = get_connected_nodes_soft(validTiles, src)  # first layer

    for i in ATL_init:
        stack.append(Step(i, src, 1))
        if i == dst:
            return [stack[len(stack) - 1], stack[0]]
        stackPos.append(i)

    end: int = len(stack)
    breaker: bool = False

    i = 0
    while True:  # other layers
        if i >= end: break
        ATL_iter = get_connected_nodes_soft(validTiles, stack[i].cPos)
        for c in ATL_iter:
            if c not in stackPos:
                stack.append(Step(c, stack[i].cPos, stack[i].layer + 1))
                stackPos.append(c)
                end += 1
                if c == dst:
                    breaker = True
                    break

        i += 1
        if breaker: break

    if breaker:  # Collecting the path
        trackPos = dst
        for i in list(range(0, end))[::-1]:
            if stack[i].cPos == trackPos:
                result.append(stack[i])
                trackPos = stack[i].pPos

    return result


firstIteration: bool = True
brain: Brain = Brain()


def getFurthestOptionFromTail(options: list, p_tail: list) -> tuple[int, int]:
    aveDist: float = 0.0
    maxAveDist: float = 0.0
    maxAveDistIndexList: list = []

    for i in range(0, len(options)):
        aveDist = getAverageDistance(options[i], p_tail)
        if i == 0 or aveDist > maxAveDist:
            maxAveDist = aveDist

    for i in range(0, len(options)):
        aveDist = getAverageDistance(options[i], p_tail)
        if aveDist == maxAveDist:
            maxAveDistIndexList.append(i)

    return options[random.choice(maxAveDistIndexList)]


def get_connected_nodes_soft(validTiles: list, pos: tuple[int, int]) -> list:
    list_coordinates = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]

    return [i for i in list_coordinates if i in validTiles]


def get_connected_nodes_hard(everyTile: list, pos: tuple[int, int]) -> list:
    list_coordinates = [(pos[0], pos[1] + 1), (pos[0], pos[1] - 1), (pos[0] - 1, pos[1]), (pos[0] + 1, pos[1])]

    # return list_coordinates
    return [i.pos for i in everyTile if i.pos in list_coordinates and (i.Type not in blockingTypes
                                                                       and i.tempType not in blockingTypes)]


def getAverageDistance(point: tuple[int, int], pointList: list) -> float or None:
    distSum: int = 0
    distCounter: int = 0

    for i in range(0, len(pointList)):
        distCounter += 1
        p2 = pointList[i]
        dist = abs(point[0] - p2[0]) + abs(point[1] - p2[1])
        distSum += dist

    if distCounter == 0: return 0

    return distSum / distCounter


def getStepTowards(source: tuple[int,int], destination:tuple[int,int]) -> Action:
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
TAIL_MAX_SIZE: int = 5


def find_closest_type(everyTile: list, selfPos: tuple[int, int], targetType: MapType) -> tuple[int, int] | None:
    closets_target = None
    closets_target_dist: float = 0
    first_iteration: bool = True

    for i in everyTile:
        if i.Type == targetType.value or i.tempType == targetType.value:
            dist = getAverageDistance(selfPos, [i.pos])
            if first_iteration or dist < closets_target_dist:
                closets_target = i.pos
                closets_target_dist = dist

            first_iteration = False

    if closets_target is not None: return tuple(closets_target)

    return None


def Update(self: GameState) -> None:
    if Brain.firstIteration:
        brain.initTiles((self.map.height, self.map.width))
        Brain.firstIteration = False

    brain.updateTiles(self.map.grid)

    tail.append(list(self.location))

    if len(tail) > TAIL_MAX_SIZE:
        tail.pop(0)


def Dispose(self: GameState) -> None:
    brain.flushTiles()


def Patrol(self: GameState) -> tuple[int, int]:
    choices = get_connected_nodes_hard(brain.everyTile, (self.location[0], self.location[1]))

    if len(choices) != 0:
        goal = getFurthestOptionFromTail(choices, tail)
    else:
        goal = self.location

    return goal


def goTo(self: GameState, dstPos: tuple[int, int]) -> tuple[int, int]:
    pathList = getShortestPath(brain.everyTile, self.location, dstPos)

    if len(pathList) != 0:
        return pathList[len(pathList) - 2].cPos

    return self.location


def BadassEquation(self: GameState) -> float:
    up = self.wallet * self.rounds
    down = (self.rounds - self.current_round) * 10 + self.map.gold_count
    return up / down


def percent(All: float | int, Some: float | int) -> float:
    if All == 0: return 0
    return Some * (100 / All)

def HorrificEquation(self: GameState) -> float:


    wallet = self.wallet # This is different at every call
    total_rounds = self.rounds # This is a constant
    remaining_rounds = self.rounds - self.current_round # this is different at every call
    map_gold_count = self.map.gold_count # This is a constant

    if wallet > map_gold_count * 2: # This caps the maximum value of wallet
        wallet = map_gold_count * 2



    up = total_rounds * wallet
    down = remaining_rounds * map_gold_count

    Some = up / down

    All = total_rounds * 2 # code to calculate the maximum possible value of (up / down)

    return percent(All, Some)


def getAction(self: GameState) -> Action:
    Update(self)

    goal = Patrol(self)

    if HorrificEquation(self) > 50:
        x = find_closest_type(brain.everyTile, self.location, MapType.TREASURY)
        if x is not None:
            goal = goTo(self, x)
    else:
        x = find_closest_type(brain.everyTile, self.location, MapType.GOLD)
        if x is not None:
            goal = goTo(self, x)

    self.debug_log += "closest_gold : " + str(x) + "\n"

    self.debug_log += "" + brain.getVisiblePlacesString() + "\n"
    Dispose(self)

    return getStepTowards(self.location, goal)
