import sys
import pygame

class Main:
    def __init__(self):
        self.SCREEN_SIZE = (600, 600)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)
        self.clock = pygame.time.Clock()
    
    def draw_grid(self):
        for x in range(0, self.SCREEN_SIZE[0], 20):
            # draw horizontal line
            pygame.draw.line(self.screen, (0, 255, 0), (x, 0), (x, self.SCREEN_SIZE[1]))

        for y in range(0, self.SCREEN_SIZE[1], 20):
            # draw vertical line
            pygame.draw.line(self.screen, (0, 255, 0), (0, y), (self.SCREEN_SIZE[0], y))
    

    def update(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(60)


game = Main()

game.update()