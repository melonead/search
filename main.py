import sys
import pygame

class Grid:

    def __init__(self, dimension, size):
        self.structure = {}
        self.dimension = dimension
        self.size = size
        for x in range(0, dimension, size): # optimize: use a single loop
            for y in range(0, dimension, size):
                self.structure[f"{x//size}:{y//size}"] = 0 # zero for empty: 1 occupied


class Main:
    def __init__(self):
        self.SCREEN_SIZE = (600, 600)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.grid = Grid(self.SCREEN_SIZE[0], 20)
        self.left_click = False
        self.right_click = False
        self.click = False
        self.start = None
        self.goal = None
    
    def draw_grid(self):

        for x in range(0, self.SCREEN_SIZE[0], self.grid.size):
            pygame.draw.line(self.screen, (0, 255, 0), (x, 0), (x, self.SCREEN_SIZE[1]))
            pygame.draw.line(self.screen, (0, 255, 0), (0, x), (self.SCREEN_SIZE[0], x))

    def create_obstacle(self):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        x = mouse_pos[0] // self.grid.size
        y = mouse_pos[1] // self.grid.size
        key = f"{x}:{y}"
        # show 
        if self.left_click: # ordinary obstacle
            try:
                print(self.grid.structure[key])
            except KeyError:
                print(mouse_pos)
                x = mouse_pos[0] // self.grid.size
                y = mouse_pos[1] // self.grid.size
                print(x, y)
            if self.grid.structure[key] == 0:
                self.grid.structure[key] = 1 # occupied
                pygame.draw.rect(self.screen, (255, 0, 0), pygame.Rect(x * self.grid.size, y * self.grid.size, self.grid.size, self.grid.size))
        if self.right_click: # start or goal
            if self.start == None:
                if self.grid.structure[key] == 0:
                    self.grid.structure[key] = 's'
                    self.start = True
                    pygame.draw.rect(self.screen, (0, 0, 255), pygame.Rect(x * self.grid.size, y * self.grid.size, self.grid.size, self.grid.size))
            else:
                if self.grid.structure[key] == 0 and self.goal == None:
                    self.grid.structure[key] = 'g'
                    self.goal = True
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(x * self.grid.size, y * self.grid.size, self.grid.size, self.grid.size))

    def update(self):
        
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

            self.draw_grid()
            pygame.display.update()
            self.clock.tick(60)


game = Main()

game.update()