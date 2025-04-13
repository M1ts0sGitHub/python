## Inspiration from Langton's Ant - Python edition  ##
## https://en.wikipedia.org/wiki/Langton%27s_ant    ##

import pygame
import pygame.locals

window_size = [800, 800]

class grid:
    def __init__(self, size : list):
        self.size = size
        self.grid = [[0 for _ in range(size[0])] for _ in range(size[1])]
        self.size_of_cell_x = window_size[0] / size[0]
        self.size_of_cell_y = window_size[1] / size[1] 
    def set_cell_color(self, x, y, color):
        self.grid[x][y] = color
    def read_cell_color(self, x, y):
        return self.grid[x][y]
    def draw_cells(self):
        # Draw the grid with grey lines
        for x in range(self.size[0]):
            pygame.draw.line(screen, (20, 20, 20), (x*self.size_of_cell_x, 0), (x*self.size_of_cell_x, window_size[1]))
        for y in range(self.size[1]):
            pygame.draw.line(screen, (20, 20, 20), (0, y*self.size_of_cell_y), (window_size[0], y*self.size_of_cell_y))
    def draw_active_cell(self,x,y,color):
        pygame.draw.rect(screen, (255,70,0), (x*self.size_of_cell_x, y*self.size_of_cell_y, self.size_of_cell_x+1, self.size_of_cell_y+1),5)     
    def draw_cell(self,x,y,color):
        pygame.draw.rect(screen, color_palette[color], (x*self.size_of_cell_x, y*self.size_of_cell_y, self.size_of_cell_x+1, self.size_of_cell_y+1)) 

class ant:
    def __init__(self, x,y, direction, grid):
        self.position = [x, y]
        self.pre_position = [x, y]
        self.direction = direction
        self.grid = grid
        self.grid.active_cell = self.position
    def next_step(self):
        color = self.grid.read_cell_color(self.position[0], self.position[1])
        self.grid.set_cell_color(self.position[0],self.position[1],color_rules[color])
        self.move_ant(color)
    def move_ant(self,color):
        self.pre_position = [self.position[0], self.position[1]]

        self.direction = (self.direction + move_rules[color]) % 4
        
        if self.direction == 0:
            self.position[1] -= 1
        elif self.direction == 1:
            self.position[0] += 1      
        elif self.direction == 2:
            self.position[1] += 1
        elif self.direction == 3:
            self.position[0] -= 1
        
        if self.position[0] < 0:
            self.position[0] = self.grid.size[0]-1
        if self.position[1] < 0:
            self.position[1] = self.grid.size[1]-1
        if self.position[0] >= self.grid.size[0]:
            self.position[0] = 0
        if self.position[1] >= self.grid.size[1]:
            self.position[1] = 0

       

pygame.init()
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Langton's Ant - Python Edition")
clock = pygame.time.Clock()

# Rules of the my Ant
move_rules = {0: 1,
              1: 3}
color_rules = {0 : 1, 
               1 : 0}
color_palette = [(0, 0, 0), 
                 (255, 255, 255)]

mygrid = grid([200, 200])
myant = ant(100, 100, 3, mygrid)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # myant.grid.draw_cells()
    myant.next_step()
    myant.grid.draw_active_cell(myant.position[0],myant.position[1],color_rules[myant.grid.read_cell_color(myant.position[0], myant.position[1])])
    myant.grid.draw_cell(myant.pre_position[0],myant.pre_position[1],color_rules[myant.grid.read_cell_color(myant.position[0], myant.position[1])])
    

    pygame.display.update() 
    clock.tick(550)