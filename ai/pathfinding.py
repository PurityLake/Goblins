"""
pathfinding
This module simply provides a pathfinding functionality for any entity that can move.
This uses the a-star method of finding a path.
"""

import math

class PathfindingNode(object):
    """
    PathfindingNode
    Node used by MapPathfinding used in a linked list to hold one point in a path
    =======
    Data Members:
    x: x coordinate
    y: y coordinate
    z: z coordinate
    cost: cost g(x) + h(x)
    prev: the previous node in the path
    """

    def __init__(self, pos, prev, cost):
        self.x, self.y, self.z = pos
        self.cost = cost
        self.prev = prev
        if self.prev is not None:
            self.gx = self.prev.gx + 1
        else:
            self.gx = 0
        
        def get_cost(self):
            return self.cost + self.gx
    
    def __lt__(self, value):
        return self.cost < value.cost

    def __eq__(self, value):
        if type(value) == PathfindingNode:
            return (self.x, self.y) == (value.x, value.y)
        return False

class MapPathfinding(object):
    """
    MapPathfinding:
    A class that encapsuates the pathfinding of the AI. Uses a simple A-star method
    of finding an optimal path to from a given point to another point. Using
    `pathfind_from_a_to_b` a path is from a to b but in reverse so it is advised to 
    reverse the origin point and destination point.
    This class can be reused and does not have to be created more than once as long as
    the same object is used for the map.
    ======
    Data Members:
    width: width of the crosssection of the map (max x coord).
    length: length of the crosssection of the map (max y coord).
    height: how many crosssections are in the level (max z coord).
    area_map: the 3-dimensional list representing the map.
    ======
    Methods:
    pathfind_from_a_to_b: find the optimal path from a to b and returns a `PathfindNode`
                          containing the reverse path in a linked list i.e. from b to a.
    """
    def __init__(self, area_map, width, length, height):
        self.width = width
        self.length = length
        self.height = height
        self.area_map = area_map
    
    def _get_open_nodes(self, x, y, z):
        if z >= self.height:
            return []

        open_list = []
        can_go_up = z + 1 < self.height
        can_go_down = z - 1 >= 0
        if x - 1 >= 0:
            node = self.area_map[z][y][x-1]
            if not node.can_walk():
                if can_go_up:
                    up_node = self.area_map[z+1][y][x-1]
                    if not up_node.can_walk():
                        open_list.append((x - 1, y, z + 1))
                if can_go_down:
                    down_node = self.area_map[z-1][y][x-1]
                    if down_node.can_walk():
                        open_list.append((x - 1, y, z - 1))
            else:
                open_list.append((x - 1, y, z))
        if x + 1 < self.width:
            node = self.area_map[z][y][x+1]
            if not node.can_walk():
                if can_go_up:
                    up_node = self.area_map[z+1][y][x+1]
                    if up_node.can_walk():
                        open_list.append((x + 1, y, z + 1))
                if can_go_down:
                    down_node = self.area_map[z-1][y][x+1]
                    if down_node.can_walk:
                        open_list.append((x + 1, y, z - 1))
            else:
                open_list.append((x + 1, y, z))
        if y - 1 >= 0:
            node = self.area_map[z][y-1][x]
            if not node.can_walk():
                if can_go_up:
                    up_node = self.area_map[z+1][y-1][x]
                    if up_node.can_walk:
                        open_list.append((x, y - 1, z + 1))
                if can_go_down:
                    down_node = self.area_map[z-1][y-1][x]
                    if down_node.can_walk:
                        open_list.append((x, y - 1, z - 1))
            else:
                open_list.append((x, y - 1, z))
        if y + 1 < self.length:
            node = self.area_map[z][y+1][x]
            if not node.can_walk():
                if can_go_up:
                    up_node = self.area_map[z+1][y+1][x]
                    if up_node.can_walk:
                        open_list.append((x, y + 1, z + 1))
                if can_go_down:
                    down_node = self.area_map[z-1][y+1][x]
                    if down_node.can_walk:
                        open_list.append((x, y + 1, z - 1))
            else:
                open_list.append((x, y + 1, z))
        
        return open_list

    def _get_cost_of_node(self, current, goal):
        x, y, z = current
        goalx, goaly, goalz = goal
        return math.sqrt(math.pow(goalx - x, 2) + math.pow(goaly - y, 2) + math.pow(goalz - z, 2))

    def _lowest_cost(self, current, open_set):
        lowest = 100000000
        node = None
        for i in open_set:
            if i.cost < lowest:
                node = i
                lowest = i.cost
        return node

    def pathfind_from_a_to_b(self, a, b):
        assert(a[0] >= 0 and a[1] >= 0 and a[2] >= 0 and b[0] >= 0 and b[1] >= 0 and b[2] >= 0)
        assert(a[0] < self.width and a[1] < self.length and a[2] < self.height)
        assert(b[0] < self.width and b[1] < self.length and b[2] < self.height)

        open_set = [PathfindingNode(a, None, math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2) + math.pow(a[2] - b[2], 2)))]
        closed_set = []
        prev = current = open_set[0]
        gx = 0
        running = True
        while running and len(open_set) > 0 or current != None and (current.x, current.y) != b:
            if (current.x, current.y, current.z) == b:
                break
            closed_set.append(current)
            new_nodes = self._get_open_nodes(current.x, current.y, current.z)
            new_nodes_costs = [self._get_cost_of_node((node[0], node[1], node[2]), b) for node in new_nodes]
            temp = []
            for n, c in zip(new_nodes, new_nodes_costs):
                if c == 0:
                    goal = PathfindingNode(n, current, 0)
                    current = goal
                    running = False
                    break
                if n in open_set:
                    if n.get_cost() < current.get_cost():
                        open_set.remove(n)
                        temp.append(PathfindingNode(n, current, c))
                else:
                    temp.append(PathfindingNode(n, current, c))
            if running:
                new_nodes = temp
                new_nodes = filter(lambda x: x not in closed_set, new_nodes)
                open_set.extend(new_nodes)
                open_set.remove(current)
                prev = current
                current = self._lowest_cost(current, open_set)
                gx += 1
        return current