from main import GameState
from main import Action
from main import MapType
import math

def a_star_algorithm(self, map_gride, start_node, stop_node):
    open_list = set([start_node])
    closed_list = set([])
    g = {}
    g[start_node] = 0
    parents = {}
    parents[start_node] = start_node

    while len(open_list) > 0:
        n = None
        for v in open_list:
            if n == None or g[v] + h(v, stop_node, self) < g[n] + h(n, stop_node, self):
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

        for (m, weight) in Connected_nodes2dictionary(self, n):
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


def Connected_nodes2dictionary(self, coordinates):
    c, w = convert_strlist_to_int(coordinates)
    poslist = get_connected_nodes(self, (c, w))
    res = []
    for element in (poslist):
        res.append((f'{element}', 1))

    dic = {
        f'{coordinates}': res
    }
    return dic[coordinates]


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


def find_gold(self):
    for i in self.map.grid:
        if i.type == MapType.GOLD.value or i.type == MapType.FOG.value:
            self.debug_log += f'self.map.grid {str(i.type)}\n'
            return i.coordinates

    return list(self.location)




def getAction(self:GameState) -> Action:
    # write your code here
    # return the action value
    start = list(self.location)
    path = a_star_algorithm(self, self.map.grid, str(start), str(find_gold(self)))
    # path=a_star_algorithm(self,self.map.grid,str(start),str([7,7]))
    if len(path) > 1:
        path.pop(0)

    goal = convert_strlist_to_int(path.pop(0))

    self.debug_log += f'path {str(path)}\n'
    return getStepTowards(self.location, goal)
