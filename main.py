import sys
import pygame
from search import (
    StackFrontier,
    ExploredSet,
    Search,
    Node,
    QueueFrontier
)

# initilize
depth_frontier = StackFrontier()
breadth_frontier = QueueFrontier()
breadth_explored_set = ExploredSet()
depth_explored_set = ExploredSet()
initial_state = None
goal_state = None


def get_key(pos, size):
    
    return pos[0] // size, pos[1] // size

BREADTH_STATE_SPACE = {}
DEPTH_STATE_SPACE = {}

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
        self.screen.fill('white')
        self.surface_size = (300, 300)
        self.depth_first_surface = pygame.Surface(self.surface_size)
        self.breadth_first_surface = pygame.Surface(self.surface_size)
        self.clock = pygame.time.Clock()
        self.cube_size = 20
        self.grid = Grid(self.surface_size[0], self.cube_size)
        self.left_click = False
        self.right_click = False
        self.click = False
        self.start_state = None
        self.goal_state = None
        # compute the displacement of each surface from the first
        self.displacement1 = (self.SCREEN_SIZE[0] // 2) + 5, 0
    
    def draw_grid(self):

        for x in range(0, self.surface_size[0], self.grid.size):
            pygame.draw.line(self.breadth_first_surface, (0, 255, 0), (x, 0), (x, self.surface_size[1]))
            pygame.draw.line(self.breadth_first_surface, (0, 255, 0), (0, x), (self.surface_size[0], x))

            pygame.draw.line(self.depth_first_surface, (0, 255, 0), (x, 0), (x, self.surface_size[1]))
            pygame.draw.line(self.depth_first_surface, (0, 255, 0), (0, x), (self.surface_size[0], x))

    def create_obstacle(self):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] // self.grid.size) * self.grid.size
        y = (mouse_pos[1] // self.grid.size) * self.grid.size
        key = get_key((x, y), self.grid.size)

        if self.left_click: # ordinary obstacle
            if self.grid.structure[key] == 0:
                self.grid.structure[key] = 1 # occupied
                pygame.draw.rect(self.breadth_first_surface, (255, 0, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))
                pygame.draw.rect(self.depth_first_surface, (255, 0, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))

        if self.right_click: # start or goal
            if self.start_state == None:
                if self.grid.structure[key] == 0:
                    self.grid.structure[key] = 's'
                    self.start_state = key
                    pygame.draw.rect(self.breadth_first_surface, (0, 0, 255), pygame.Rect(x, y, self.grid.size, self.grid.size))
                    pygame.draw.rect(self.depth_first_surface, (0, 0, 255), pygame.Rect(x, y, self.grid.size, self.grid.size))
            else:
                if self.grid.structure[key] == 0 and self.goal_state == None:
                    self.grid.structure[key] = 'g'
                    self.goal_state = key
                    pygame.draw.rect(self.breadth_first_surface, (0, 255, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))
                    pygame.draw.rect(self.depth_first_surface, (0, 255, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))

    def update(self):
        global initial_state
        global goal_state
        global breadth_explored_set
        global depth_explored_set
        breadth_searching = False
        depth_searching = False
        breadth_path_found = False
        depth_path_found = False

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
                if self.goal_state != None and not breadth_path_found and not depth_path_found:
                    breadth_searching = True
                    depth_searching = True

                initial_state = self.start_state
                goal_state = self.goal_state
                if breadth_frontier.size == 0 and initial_state != None:
                    breadth_frontier.add_node(Node(initial_state, (0, 0)))
                
                if depth_frontier.size == 0 and initial_state != None:
                    depth_frontier.add_node(Node(initial_state, (0, 0)))
            
            #print(self.grid.structure)
            breadth_path_found, breadth_searching = Search(breadth_frontier, breadth_explored_set, goal_state, BREADTH_STATE_SPACE, self.breadth_first_surface, self.cube_size, self.grid.structure, breadth_searching, breadth_path_found)
            depth_path_found, depth_searching = Search(depth_frontier, depth_explored_set, goal_state, DEPTH_STATE_SPACE, self.depth_first_surface, self.cube_size, self.grid.structure, depth_searching, depth_path_found)
                
            self.draw_grid()
            self.screen.blit(self.breadth_first_surface, (0, 0))
            self.screen.blit(self.depth_first_surface, (self.displacement1[0], self.displacement1[1]))
            pygame.display.update()
            self.clock.tick(60)


game = Main()

game.update()


# simultaneous display of both algorithms
    # make obstacle
        # display on both screens
        # store in single grid
    # searching
        # use identical grid
        # use different search algorithms