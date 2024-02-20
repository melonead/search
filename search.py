# search algorithms

search_type = 'dfs'
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

    def get_next_state(self):
        return self.states[0]

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


def Search(stack_frontier, explored_set, grid, goal_state, current_state=None):
    if stack_frontier.size == 0:
        print('no solution found')
        return False # no solution available
    
    current_state = stack_frontier.frontier[0]
    stack_frontier.remove_state(current_state)

    if current_state == goal_state:
        return True # solution found
    # expand the state
    expand(current_state, grid, stack_frontier, explored_set)
    explored_set.set.add(current_state)





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