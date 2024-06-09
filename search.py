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


def trace_back_path(node, state_space, screen, cube_size):
    count = 0
    while node.parent != None:
        p_key = (node.state[0] - node.action[0], node.state[1] - node.action[1])
        node = state_space[p_key]
        pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(node.state[0] * cube_size, node.state[1] * cube_size, cube_size, cube_size))
        count += 1
    return count


def expand_node(actions, current_node, frontier, explored_set):
    for action in actions:
        a = current_node.state[0] + action[0]
        b = current_node.state[1] + action[1]
        new_node = Node((a, b), action)
        new_node.parent = current_node
        if (new_node.state not in frontier.states) and (new_node.state not in explored_set.set):
            frontier.add_node(new_node)

def expand_a_star_node(actions, current_node, frontier, explored_set, goal_state, initial_state):
    for action in actions:
        a = current_node.state[0] + action[0]
        b = current_node.state[1] + action[1]
        new_node = NodeAStar((a, b), action)
        new_node.compute_costs(initial_state, goal_state)
        new_node.parent = current_node
        if (new_node.state not in frontier.states) and (new_node.state not in explored_set.set):
            frontier.add_node(new_node)


def Search(stype, search_vars, screen, cube_size, grid_structure, name, right_border):
    
    if not stype.searching: return stype.path_found, stype.searching
    
    if search_vars.goal_state != None and stype.searching:
        if stype.frontier.size == 0:
            print('no solution')
            stype.searching = False
            stype.path_found = False
            return stype.path_found, stype.searching
        else:
            current_node = stype.frontier.get_next_node()
            stype.state_space[current_node.state] = current_node

            pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(current_node.state[0] * cube_size, current_node.state[1] * cube_size, cube_size, cube_size), 3)

        if current_node.state == search_vars.goal_state:
            n = current_node
            count = trace_back_path(n, stype.state_space, screen, cube_size)
            stype.searching = False
            stype.path_found = True
            print(f'name: {name}')
            print(f'path length: {count}')

        actions = get_valid_actions(current_node, grid_structure, right_border)


        expand_node(actions, current_node, stype.frontier, stype.explored_set)


        stype.explored_set.set.add(current_node.state)
        stype.frontier.remove_node(current_node)
    return stype.path_found, stype.searching


def heuristic(frontier):
    lowest_cost = 9999999
    
    for cn in frontier.frontier:
        if cn.get_total_cost() < lowest_cost:
            lowest_cost = cn.get_total_cost()

    lowest_cost_nodes = []
    for cn in frontier.frontier:
        if cn.get_total_cost() == lowest_cost:
            lowest_cost_nodes.append(cn)
    
    lowest_h_cost = 99999
    for cn in lowest_cost_nodes:
        if cn.h_cost < lowest_h_cost:
            lowest_h_cost = cn.h_cost
            current_node = cn
    return current_node


def AStarSearch(astar, search_vars, screen, cube_size, grid_structure, name, right_border):
    if not astar.searching: return astar.path_found, astar.searching
    if search_vars.goal_state != None and astar.searching:
        if astar.frontier.size == 0:
            print('no solution')
            astar.searching = False
            astar.path_found = False
            return astar.path_found, astar.searching
        else:
            current_node = heuristic(astar.frontier)

            astar.state_space[current_node.state] = current_node

            pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(current_node.state[0] * cube_size, current_node.state[1] * cube_size, cube_size, cube_size), 3)
         
        if current_node.state == search_vars.goal_state:
            n = current_node
            count = trace_back_path(n, astar.state_space, screen, cube_size)
            astar.searching = False
            astar.path_found = True
            print(f'name: {name}')
            print(f'path length: {count}')

        actions = get_valid_actions(current_node, grid_structure, right_border)

        expand_a_star_node(actions, current_node, astar.frontier, astar.explored_set, search_vars.goal_state, search_vars.initial_state)

        astar.explored_set.set.add(current_node.state)
        astar.frontier.remove_node(current_node)
        
    return astar.path_found, astar.searching


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