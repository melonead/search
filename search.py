# search algorithms

search_type = 'dfs'
class Node:
    
    def __init__(self, state):
        self.state = state
        self.parent = None
        # self.action = action
        # self.type = type

class StackFrontier:

    def __init__(self):
        self.frontier = []
    
    def add_state(self, state): # state is a node
        self.frontier.append(state)
    
    def remove_state(self, state):
        if self.frontier:
            self.frontier.remove(state)
    
    def get_state(self):
        return self.frontier[0]

    @property
    def size(self):
        return len(self.frontier)
    
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

def get_valid_actions(state, grid):
    actions = []
    all_actions = [-4, -3, -2, -1, 1, 2, 3, 4]
    for action in all_actions:
        if grid[state + action] != 1:
            actions.append(action)
    return actions

def expand(state, grid, frontier, explored_set):
    actions = get_valid_actions(state, grid)
    for action in actions:
        new_state = state + action
        if (new_state not in frontier) and (new_state not in explored_set):
            frontier.append(state + action)


def Search(frontier, explored_set, grid, current_state=None):
    if frontier.size == 0:
        print('no solution found')
        return False # no solution available
    
    current_state = frontier[0]
    frontier.remove_state(current_state)

    if current_state.type == 'g':
        return True # solution found
    # expand the state
    expand(current_state, grid, frontier)
    explored_set.add(current_state)





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