from calendar import c
from distutils.log import debug
from logging import exception
import math
from os import makedirs
from enum import Enum
import random
DEBUG = 1

def a_star_algorithm(self,map_gride,start_node, stop_node):

    open_list = set([start_node])
    closed_list = set([])
    g = {}
    g[start_node] = 0
    parents = {}
    parents[start_node] = start_node

    while len(open_list) > 0:
        n = None
        for v in open_list:
            if n == None or g[v] + h(v,stop_node,self) < g[n] + h(n,stop_node,self):
                n = v

        if n == None:
            return None
        if n == stop_node:
            reconst_path = []

            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]

            reconst_path.append(start_node)

            reconst_path.reverse()
            return reconst_path
        
        for (m, weight) in Connected_nodes2dictionary(self,n):
            if m not in open_list and m not in closed_list:
                open_list.add(m)
                parents[m] = n
                g[m] = g[n] + weight

            else:
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

        open_list.remove(n)
        closed_list.add(n)
    return None
def h( n,stop_node,self):
    a=convert_strlist_to_int(n)
    b=convert_strlist_to_int(stop_node)
    # a=(x-x1)**2 +(y-y1)**2
    # math.sqrt(a)
    # self.debug_log += f'nnnnnn {str(math.sqrt(a))}\n'
    return math.sqrt(math.dist(a,b))



def convert_strlist_to_int(str):# '[3,4]'--->(3,4)
    a=str.split(',')
    b=a[0]
    c=b.split('[')
    d=a[1]
    e=d.split(']')
    return int(c[1]),int(e[0])

def get_connected_nodes(self,coordinates):
    map_gride=self.map.grid
    i,j=coordinates
    list_coordinates=[[i,j+1],[i,j-1],[i-1,j],[i+1,j]]
    for i in map_gride:
        if i.coordinates in list_coordinates and i.type==4:
            list_coordinates.remove(i.coordinates)
    return list_coordinates


def Connected_nodes2dictionary(self,coordinates):
    c,w=convert_strlist_to_int(coordinates)
    poslist=get_connected_nodes(self,(c,w))
    res=[]
    for  element in (poslist):
        
        res.append(( f'{element}',1 ))
             
    dic={
        f'{coordinates}': res
    }
    return dic[coordinates]

class Action(Enum):
    def __str__(self) -> str:
        return str(self.value)

    STAY = 0
    MOVE_DOWN = 1
    MOVE_UP = 2
    MOVE_RIGHT = 3
    MOVE_LEFT = 4
    UPGRADE_DEFENCE = 5
    UPGRADE_ATTACK = 6
    LINEAR_ATTACK_DOWN = 7
    LINEAR_ATTACK_UP = 8
    LINEAR_ATTACK_RIGHT = 9
    LINEAR_ATTACK_LEFT = 10
    RANGED_ATTACK = 11


class MapType(Enum):
    def __str__(self) -> str:
        return str(self.value)

    EMPTY = 0
    AGENT = 1
    GOLD = 2
    TREASURY = 3
    WALL = 4
    FOG = 5
    OUT_OF_SIGHT = 6
    OUT_OF_MAP = 7


class MapTile:
    def __init__(self) -> None:
        self.type: MapType
        self.data: int
        self.coordinates: tuple(int, int)


class Map:
    def __init__(self) -> None:
        self.width: int
        self.height: int
        self.gold_count: int
        self.sight_range: int
        self.grid: list

    def set_grid_size(self) -> None:
        self.grid = [MapTile() for _ in range(self.sight_range ** 2)]


class GameState:
    def __init__(self) -> None:
        self.rounds = int(input())
        self.def_upgrade_cost = int(input())
        self.atk_upgrade_cost = int(input())
        self.cool_down_rate = float(input())
        self.linear_attack_range = int(input())
        self.ranged_attack_radius = int(input())
        self.map = Map()
        self.map.width, self.map.height = map(int, input().split())
        self.map.gold_count = int(input())
        self.map.sight_range = int(input())  # equivalent to (2r+1)
        self.map.set_grid_size()
        self.debug_log = ''

    def set_info(self) -> None:
        self.location = tuple(map(int, input().split()))  # (row, column)
        for tile in self.map.grid:
            tile.type, tile.data, *tile.coordinates = map(int, input().split())
        self.agent_id = int(input())  # player1: 0,1 --- player2: 2,3
        self.current_round = int(input())  # 1 indexed
        self.attack_ratio = float(input())
        self.deflvl = int(input())
        self.atklvl = int(input())
        self.wallet = int(input())
        self.safe_wallet = int(input())
        self.wallets = [*map(int, input().split())]  # current wallet
        self.last_action = int(input())  # -1 if unsuccessful

    def debug(self) -> None:
        # Customize to your needs
        self.debug_log += f'round: {str(self.current_round)}\n'
        self.debug_log += f'location: {str(self.location)}\n'
        self.debug_log += f'attack ratio: {str(self.attack_ratio)}\n'
        self.debug_log += f'defence level: {str(self.deflvl)}\n'
        self.debug_log += f'attack level: {str(self.atklvl)}\n'
        self.debug_log += f'wallet: {str(self.wallet)}\n'
        self.debug_log += f'safe wallet: {str(self.safe_wallet)}\n'
        self.debug_log += f'list of wallets: {str(self.wallets)}\n'
        self.debug_log += f'last action: {str(self.last_action)}\n'
        
        # self.debug_log += f'self.map.grid {str(a=get_connected_nodes(self.map.grid,0.0))}\n'
        self.debug_log += f'{60 * "-"}\n'
    def debug_file(self) -> None:
        fileName = 'Clients/logs/'
        makedirs(fileName, exist_ok=True)
        fileName += f'AGENT{self.agent_id}.log'
        with open(fileName, 'a') as f:
            f.write(self.debug_log)

   


    def get_action(self) -> Action:
        # write your code here
        # return the action value
        start=list(self.location)
        path=a_star_algorithm(self,self.map.grid,str(start),str(find_gold(self)))
        # path=a_star_algorithm(self,self.map.grid,str(start),str([7,7]))
        if len(path)>1:
            path.pop(0)

        goal=convert_strlist_to_int(path.pop(0))
        
        self.debug_log += f'path {str(path)}\n'
        return getStepTowards(self.location,goal)

def getStepTowards(source,destination) -> Action:
    if source[0] < destination[0]:
        return Action.MOVE_DOWN
    if source[0] > destination[0]:
        return Action.MOVE_UP

    if source[1] < destination[1]:
        return Action.MOVE_RIGHT
    if source[1] > destination[1]:
        return Action.MOVE_LEFT

    return Action.STAY
 
def find_gold(self):
    for i in self.map.grid:
        if i.type==2:
            self.debug_log += f'self.map.grid {str(i.type)}\n'
            return i.coordinates
    r=random.randint(0,len(self.map.grid)//3)
    self.debug_log += f'rrrrrrrrrr {str(r)}\n'
    self.debug_log += f'len(self.map.grid) {str(len(self.map.grid))}\n'
    gride=self.map.grid[r]
    self.debug_log += f'gride.coordinates {str(gride.coordinates)}\n'
    gride=self.map.grid[1]
    return list((gride.coordinates))

if __name__ == '__main__':
    game_state = GameState()
    for _ in range(game_state.rounds):
        game_state.set_info()
        print(game_state.get_action())
        if DEBUG:
            game_state.debug()
    if DEBUG:
        game_state.debug_file()
