import sys
import pygame
from search import (bs, ds, astar, Node, NodeAStar)


class SearchVars:

    def __init__(self):
        # -------- goal and start node -----------------------------------
        self.initial_state = None
        self.goal_state = None
    
    def reset_vars(self):
        self.initial_state = None
        self.goal_state = None
    

# convert a position on screen to a key in grid structure
def get_key(pos, size):
    return pos[0] // size, pos[1] // size

# represent the grid structure: contains all the possible states
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
        self.SCREEN_SIZE = (600, 610)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)
        pygame.display.set_caption('search')
        self.screen.fill('white')
        self.surface_size = (300, 300)
        self.depth_first_surface = pygame.Surface(self.surface_size)
        self.breadth_first_surface = pygame.Surface(self.surface_size)
        self.a_star_surface = pygame.Surface(self.surface_size)
        self.clock = pygame.time.Clock()
        self.cube_size = 20
        self.grid = Grid(self.surface_size[0], self.cube_size)
        self.left_click = False
        self.right_click = False
        self.click = False
        self.start_state = None
        self.goal_state = None
        self.right_border = self.surface_size[0] // self.cube_size
        # compute the displacement of each surface from the first
        self.displacement1 = (self.SCREEN_SIZE[0] // 2) + 5, 0
        self.displacement2 = 0, (self.SCREEN_SIZE[1] // 2) + 5
    
    def reset(self):
        self.grid = Grid(self.surface_size[0], self.cube_size)
        self.goal_state = None
        self.start_state = None
    
    # draw the grid
    def draw_grid(self):

        for x in range(0, self.surface_size[0], self.grid.size):
            pygame.draw.line(self.breadth_first_surface, (0, 255, 0), (x, 0), (x, self.surface_size[1]))
            pygame.draw.line(self.breadth_first_surface, (0, 255, 0), (0, x), (self.surface_size[0], x))

            pygame.draw.line(self.depth_first_surface, (0, 255, 0), (x, 0), (x, self.surface_size[1]))
            pygame.draw.line(self.depth_first_surface, (0, 255, 0), (0, x), (self.surface_size[0], x))

            pygame.draw.line(self.a_star_surface, (0, 255, 0), (x, 0), (x, self.surface_size[1]))
            pygame.draw.line(self.a_star_surface, (0, 255, 0), (0, x), (self.surface_size[0], x))

    # draw obstacles, start and goal 
    def create_obstacle(self):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        x = (mouse_pos[0] // self.grid.size) * self.grid.size
        y = (mouse_pos[1] // self.grid.size) * self.grid.size
        key = get_key((x, y), self.grid.size)

        if key[0] >= self.right_border or key[1] >= self.right_border or key[0] < 0 or key[1] < 0:
            return

        if self.left_click: # ordinary obstacle
            if self.grid.structure[key] == 0:
                self.grid.structure[key] = 1 # occupied
                pygame.draw.rect(self.breadth_first_surface, (255, 0, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))
                pygame.draw.rect(self.depth_first_surface, (255, 0, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))
                pygame.draw.rect(self.a_star_surface, (255, 0, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))

        if self.right_click: # start or goal
            if self.start_state == None:
                if self.grid.structure[key] == 0:
                    self.grid.structure[key] = 's'
                    self.start_state = key
                    pygame.draw.rect(self.breadth_first_surface, (0, 0, 255), pygame.Rect(x, y, self.grid.size, self.grid.size))
                    pygame.draw.rect(self.depth_first_surface, (0, 0, 255), pygame.Rect(x, y, self.grid.size, self.grid.size))
                    pygame.draw.rect(self.a_star_surface, (0, 0, 255), pygame.Rect(x, y, self.grid.size, self.grid.size))
            else:
                if self.grid.structure[key] == 0 and self.goal_state == None:
                    self.grid.structure[key] = 'g'
                    self.goal_state = key
                    pygame.draw.rect(self.breadth_first_surface, (0, 255, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))
                    pygame.draw.rect(self.depth_first_surface, (0, 255, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))
                    pygame.draw.rect(self.a_star_surface, (0, 255, 0), pygame.Rect(x, y, self.grid.size, self.grid.size))

    def update(self):

        search_vars = SearchVars()
        reset = False

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
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        reset = False
            
            # RESET TO INITIAL STATE   
            if reset:
                self.screen.fill((255, 255, 255))
                self.depth_first_surface.fill((0, 0, 0))
                self.breadth_first_surface.fill((0, 0, 0))
                self.a_star_surface.fill((0, 0, 0))
                bs.reset()
                ds.reset()
                astar.reset()
                #a_star.reset()
                self.reset()

            if self.click:
                self.create_obstacle()
                if self.goal_state != None and not bs.path_found and not ds.path_found:
                    bs.searching = True
                    ds.searching = True
                    astar.searching = True

                search_vars.initial_state = self.start_state
                search_vars.goal_state = self.goal_state
                if bs.frontier.size == 0 and search_vars.initial_state != None:
                    bs.frontier.add_node(Node(search_vars.initial_state, (0, 0)))
                
                if ds.frontier.size == 0 and search_vars.initial_state != None:
                    ds.frontier.add_node(Node(search_vars.initial_state, (0, 0)))

                if astar.frontier.size == 0 and search_vars.initial_state != None and search_vars.goal_state != None:
                    i_n = NodeAStar(search_vars.initial_state, (0, 0))
                    i_n.compute_costs(search_vars.initial_state, search_vars.goal_state)
                    astar.frontier.add_node(i_n)
            
            bs.search(search_vars, self.breadth_first_surface, self.cube_size, self.grid.structure, self.right_border)
            ds.search(search_vars, self.depth_first_surface, self.cube_size, self.grid.structure, self.right_border)
            astar.search(search_vars, self.a_star_surface, self.cube_size, self.grid.structure, self.right_border)
                
            self.draw_grid()
            self.screen.blit(self.breadth_first_surface, (0, 0))
            self.screen.blit(self.depth_first_surface, (self.displacement1[0], self.displacement1[1]))
            self.screen.blit(self.a_star_surface, (self.displacement2[0], self.displacement2[1]))
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
