import sys
import pygame
from search import (
    StackFrontier,
    ExploredSet,
    get_valid_actions,
    Node
)

# initilize
stack_frontier = StackFrontier()
explored_set = ExploredSet()
initial_state = None
goal_state = None


def get_key(pos, size):
    
    return pos[0] // size, pos[1] // size

STATE_SPACE = {}

class Grid:

    def __init__(self, dimension, size):
        self.structure = {}
        self.dimension = dimension
        self.size = size
        key = 0
        for x in range(0, dimension, size): # optimize: use a single loop
            for y in range(0, dimension, size):
                key = get_key((x, y), size)
                self.structure[key] = 0 # zero for empty: 1 occupied
                
                

class Main:
    def __init__(self):
        self.SCREEN_SIZE = (600, 600)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.cube_size = 20
        self.grid = Grid(self.SCREEN_SIZE[0], self.cube_size)
        self.left_click = False
        self.right_click = False
        self.click = False
        self.start_state = None
        self.goal_state = None
    
    def draw_grid(self):

        for x in range(0, self.SCREEN_SIZE[0], self.grid.size):
            pygame.draw.line(self.screen, (0, 255, 0), (x, 0), (x, self.SCREEN_SIZE[1]))
            pygame.draw.line(self.screen, (0, 255, 0), (0, x), (self.SCREEN_SIZE[0], x))

    def create_obstacle(self):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] // self.grid.size) * self.grid.size
        y = (mouse_pos[1] // self.grid.size) * self.grid.size
        key = get_key((x, y), self.grid.size)

        if self.left_click: # ordinary obstacle
            if self.grid.structure[key] == 0:
                self.grid.structure[key] = 1 # occupied
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))

        if self.right_click: # start or goal
            if self.start_state == None:
                if self.grid.structure[key] == 0:
                    self.grid.structure[key] = 's'
                    self.start_state = key
                    pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(x, y, self.grid.size, self.grid.size))
            else:
                if self.grid.structure[key] == 0 and self.goal_state == None:
                    self.grid.structure[key] = 'g'
                    self.goal_state = key
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))

    def update(self):
        global initial_state
        global goal_state
        global stack_frontier
        global explored_set
        searching = False
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click = True
                    if event.button == 1:
                        self.left_click = True
                    if event.button == 3:
                        self.right_click = True
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.click = False
                    if event.button == 1:
                        self.left_click = False
                    if event.button == 3:
                        self.right_click = False
                
            if self.click:
                self.create_obstacle()
                if self.goal_state != None:
                    searching = True
                initial_state = self.start_state
                goal_state = self.goal_state
                if stack_frontier.size == 0 and initial_state != None:
                    stack_frontier.add_node(Node(initial_state, (0, 0)))
            
            #print(self.grid.structure)
            if goal_state != None and searching:
                if stack_frontier.size == 0:
                    print('no solution')
                    searching = False
                else:
                    current_node = stack_frontier.get_next_node()
                    STATE_SPACE[current_node.state] = current_node
                    pygame.draw.rect(self.screen, (255, 0, 255), pygame.Rect(current_node.state[0] * self.cube_size, current_node.state[1] * self.cube_size, self.cube_size, self.cube_size), 3)

                    if current_node.state == goal_state:
                        print('found solution')
                        n = current_node
                        while n.parent != None:
                            p_key = (n.state[0] - n.action[0], n.state[1] - n.action[1])
                            n = STATE_SPACE[p_key]
                            pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(n.state[0] * self.cube_size, n.state[1] * self.cube_size, self.cube_size, self.cube_size))
                        searching = False
                    
                    actions = get_valid_actions(current_node, self.grid.structure, 30)

                    for action in actions:
                        a = current_node.state[0] + action[0]
                        b = current_node.state[1] + action[1]
                        new_node = Node((a, b), action)
                        new_node.parent = current_node
                        if (new_node.state not in stack_frontier.states) and (new_node.state not in explored_set.set):
                            stack_frontier.add_node(new_node)
                    
                    explored_set.set.add((a, b))
                    stack_frontier.remove_node(current_node)
                    

                

            self.draw_grid()
            pygame.display.update()
            self.clock.tick(60)


game = Main()

game.update()