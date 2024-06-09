import pygame
# search algorithms

class Node:
    
    def __init__(self, state, action):
        self.state = state
        self.parent = None
        self.action = action
        # self.type = type

class NodeAStar(Node):
    def __init__(self, state, action):
        Node.__init__(self, state, action)
        self.h_cost = None
        self.g_cost = None
    
    def compute_costs(self, initial_state, goal_state):
        self.h_cost = abs(goal_state[0] - self.state[0]) + abs(goal_state[1] - self.state[1])
        self.g_cost = abs(self.state[0] - initial_state[0]) + abs(self.state[1] - initial_state[1])
    
    def get_total_cost(self):
        return self.h_cost + self.g_cost


class StackFrontier:

    def __init__(self):
        self.frontier = []
        self.states = []
    
    def add_node(self, node): # state is a node
        self.states.append(node.state)
        self.frontier.append(node)

    def remove_node(self, state):
        if self.frontier:
            self.frontier.remove(state)
    
    def get_next_node(self):
        return self.frontier[-1]


    @property
    def size(self):
        return len(self.frontier)
    
class AStarFrontier(StackFrontier):
    def add_node(self, node):
        self.states.append(node.state)
        self.frontier.append(node)
                    
    def get_next_node(self):
        return self.frontier[0]



class QueueFrontier(StackFrontier):

    def get_next_node(self):
        return self.frontier[0]
    
    
class ExploredSet:

    def __init__(self):
        self.set = set()

class BaseSearch:
    def __init__(self, frontier, set, name):
        # store the node of the current node to be explored in depth search
        self.frontier = frontier
        self.state_space = {}
        self.explored_set = set
        self.path_found = False
        self.searching = False
        self.current_node = None
        self.actions = []
        self.name = name
    
    def reset(self):
        self.frontier = None
        self.state_space = {}
        self.explored_set = ExploredSet()
        self.path_found = False
        self.searching = False
        self.current_node = None
        self.actions = []
    
    def search(self, search_vars, screen, cube_size, grid_structure, right_border):
        if not self.searching: return 
        if search_vars.goal_state != None and self.searching:
            if self.frontier.size == 0:
                print('no solution')
                self.searching = False
                self.path_found = False
                return self.path_found, self.searching
            else:
                self.applyHeuristic()
                self.state_space[self.current_node.state] = self.current_node

                pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.current_node.state[0] * cube_size, self.current_node.state[1] * cube_size, cube_size, cube_size), 3)

            if self.current_node.state == search_vars.goal_state:
                n = self.current_node
                count = self.trace_back_path(n, screen, cube_size)
                self.searching = False
                self.path_found = True
                print(f'name: {self.name}')
                print(f'path length: {count}')

            self.compute_valid_actions(grid_structure, right_border)
            self.expand_node()
            self.explored_set.set.add(self.current_node.state)
            self.frontier.remove_node(self.current_node)
        return
    # some algorithms have no heuristic, hence they won't override
    # this function, others have it and they will override it.
    def applyHeuristic(self):
        self.current_node = self.frontier.get_next_node()

    def expand_node(self):
        for action in self.actions:
            a = self.current_node.state[0] + action[0]
            b = self.current_node.state[1] + action[1]
            new_node = Node((a, b), action)
            new_node.parent = self.current_node
            if (new_node.state not in self.frontier.states) and (new_node.state not in self.explored_set.set):
                self.frontier.add_node(new_node)

    def compute_valid_actions(self, grid, right_border):
        self.actions = []
        all_actions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for action in all_actions:
            x = self.current_node.state[0] + action[0]
            y = self.current_node.state[1] + action[1]
            if (x < 0) or (y < 0) or (x >= right_border) or (y >= right_border): continue
            if grid[(x, y)] != 1:
                self.actions.append(action)

    def trace_back_path(self, node, screen, cube_size):
        count = 0
        while node.parent != None:
            p_key = (node.state[0] - node.action[0], node.state[1] - node.action[1])
            node = self.state_space[p_key]
            pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(node.state[0] * cube_size, node.state[1] * cube_size, cube_size, cube_size))
            count += 1
        return count
    

class Breadth(BaseSearch):

    def __init__(self, frontier, set, name):
        BaseSearch.__init__(self, frontier, set, name)
    
    def reset(self):
        BaseSearch.reset(self)
        self.frontier = QueueFrontier()

class Depth(BaseSearch):

    def __init__(self, frontier, set, name):
        BaseSearch.__init__(self, frontier, set, name)
    
    def reset(self):
        BaseSearch.reset(self)
        self.frontier = StackFrontier()

class AStar(BaseSearch):

    def __init__(self, frontier, set, name):
        BaseSearch.__init__(self, frontier, set, name)
    
    def reset(self):
        BaseSearch.reset(self)
        self.frontier = AStarFrontier()
    
    def expand_node(self, initial_state, goal_state):
        for action in self.actions:
            a = self.current_node.state[0] + action[0]
            b = self.current_node.state[1] + action[1]
            new_node = NodeAStar((a, b), action)
            new_node.compute_costs(initial_state, goal_state)
            new_node.parent = self.current_node
            if (new_node.state not in self.frontier.states) and (new_node.state not in self.explored_set.set):
                self.frontier.add_node(new_node)
    
    def search(self, search_vars, screen, cube_size, grid_structure, right_border):
        if not self.searching: return 
        if search_vars.goal_state != None and self.searching:
            if self.frontier.size == 0:
                print('no solution')
                self.searching = False
                self.path_found = False
                return self.path_found, self.searching
            else:
                self.applyHeuristic()
                self.state_space[self.current_node.state] = self.current_node

                pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.current_node.state[0] * cube_size, self.current_node.state[1] * cube_size, cube_size, cube_size), 3)

            if self.current_node.state == search_vars.goal_state:
                n = self.current_node
                count = self.trace_back_path(n, screen, cube_size)
                self.searching = False
                self.path_found = True
                print(f'name: {self.name}')
                print(f'path length: {count}')

            self.compute_valid_actions(grid_structure, right_border)
            self.expand_node(search_vars.initial_state, search_vars.goal_state)
            self.explored_set.set.add(self.current_node.state)
            self.frontier.remove_node(self.current_node)
        return
    
    def applyHeuristic(self):
        lowest_cost = 9999999
    
        for cn in self.frontier.frontier:
            if cn.get_total_cost() < lowest_cost:
                lowest_cost = cn.get_total_cost()

        lowest_cost_nodes = []
        for cn in self.frontier.frontier:
            if cn.get_total_cost() == lowest_cost:
                lowest_cost_nodes.append(cn)
        
        lowest_h_cost = 99999
        for cn in lowest_cost_nodes:
            if cn.h_cost < lowest_h_cost:
                lowest_h_cost = cn.h_cost
                self.current_node = cn

bs = Breadth(QueueFrontier(), ExploredSet(), "Breadth first")
ds = Depth(StackFrontier(), ExploredSet(), "Depth first")
astar = AStar(AStarFrontier(), ExploredSet(), "A-Star search")

# A* search
    # the expanded node is the one with the lowest cost
    # node has h(c) heuristic cost
    # node has g(c) cost from initial state

# initialize frontier, start state the one only in frontier
# initialize an empty explored set
        
# repeat
        # if the frontier is empty, no solution return
        # remove a node from the frontier
        # add node to the explored set
        # if node has goal state return solution
        # add node to explored set
        # expand the node, add resulting nodes to the frontier
        # if children/child/state(s) not in frontier and explored set
            # add children of node to frontier

# To Do
    # make stack based (depth-first) and queue based(breadth-first) run side by side
    # add A* search algorithm
    # create a web version