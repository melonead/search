import pygame
# search algorithms

class Node:
    
    def __init__(self, state, action):
        self.state = state
        self.parent = None
        self.action = action
        # self.type = type


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
        return self.frontier[0]


    @property
    def size(self):
        return len(self.frontier)

class QueueFrontier(StackFrontier):

    def get_next_node(self):
        return self.frontier[-1]
    
    
class ExploredSet:

    def __init__(self):
        self.set = set()

# initialize the frontier and explored set

def initialize(initial_state, frontier, explored_state):
    frontier = StackFrontier()
    explored_set = ExploredSet()
    initial_state = Node(initial_state)
    frontier.add_state(initial_state)

def Result(state, actions):
    return 

def get_valid_actions(node, grid, right_border):
    actions = []
    all_actions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for action in all_actions:
        x = node.state[0] + action[0]
        y = node.state[1] + action[1]
        if (x < 0) or (y < 0) or (x >= right_border) or (y >= right_border): continue
        if grid[(x, y)] != 1:
            actions.append(action)
    return actions

def expand(node, grid, stack_frontier, explored_set, size): # get the valid neighbors
    actions = get_valid_actions(node, grid)

    for action in actions:
        x = node.state[0] + action * size
        y = node.state[1] + action * size
        state = f"{x}:{y}"
        if (state not in stack_frontier.states) and (state not in explored_set.set):
            stack_frontier.add_node(Node(state, action))

def trace_back_path(node, state_space, screen, cube_size):
    while node.parent != None:
        p_key = (node.state[0] - node.action[0], node.state[1] - node.action[1])
        node = state_space[p_key]
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(node.state[0] * cube_size, node.state[1] * cube_size, cube_size, cube_size))


def expand_node(actions, current_node, frontier, explored_set):
    for action in actions:
        a = current_node.state[0] + action[0]
        b = current_node.state[1] + action[1]
        new_node = Node((a, b), action)
        new_node.parent = current_node
        if (new_node.state not in frontier.states) and (new_node.state not in explored_set.set):
            frontier.add_node(new_node)

def Search(frontier, explored_set, goal_state, state_space, screen, cube_size, grid_structure, searching, path_found):
    if not searching: return path_found, searching
    
    if goal_state != None and searching:
        if frontier.size == 0:
            print('no solution')
            searching = False
            path_found = False
        else:
            current_node = frontier.get_next_node()
            state_space[current_node.state] = current_node
            pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(current_node.state[0] * cube_size, current_node.state[1] * cube_size, cube_size, cube_size), 3)

        if current_node.state == goal_state:
            print('found solution still')
            n = current_node
            trace_back_path(n, state_space, screen, cube_size)
            searching = False
            path_found = True

        actions = get_valid_actions(current_node, grid_structure, 30)

        expand_node(actions, current_node, frontier, explored_set)

        explored_set.set.add(current_node.state)
        frontier.remove_node(current_node)
    return path_found, searching







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
    # create a web version