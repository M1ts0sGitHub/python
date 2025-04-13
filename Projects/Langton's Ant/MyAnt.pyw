## Inspiration from Langton's Ant - Python edition  ##
## https://en.wikipedia.org/wiki/Langton%27s_ant    ##

import pygame
import random
import pygame.locals

window_size = [600, 600]

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
move_rules = {0: random.randint(0,3),
              1: random.randint(0,3),
              2: random.randint(0,3),
              3: random.randint(0,3),
              4: random.randint(0,3),
              5: random.randint(0,3),
              6: random.randint(0,3),
              7: random.randint(0,3)}
color_rules = {0 : random.randint(0,7), 
               1 : random.randint(0,7),
               1 : random.randint(0,7),
               2 : random.randint(0,7),
               3 : random.randint(0,7),
               4 : random.randint(0,7),
               5 : random.randint(0,7),
               6 : random.randint(0,7),
               7 : 0}
color_palette = [(0, 0, 0), 
                 (255, 255, 255),
                 (255, 0, 0),
                 (0, 255, 0),
                 (0, 0, 255),
                 (255, 255, 0),
                 (0, 255, 255),
                 (255, 0, 255)]

mygrid = grid([50, 50])
myant = ant(25, 25, 3, mygrid)

interation = 0
skip_frames = 1
keypressed = 0
ct = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    myant.next_step()
    myant.grid.draw_active_cell(myant.position[0],myant.position[1],color_rules[myant.grid.read_cell_color(myant.position[0], myant.position[1])])
    myant.grid.draw_cell(myant.pre_position[0],myant.pre_position[1],color_rules[myant.grid.read_cell_color(myant.position[0], myant.position[1])])
    myant.grid.draw_cells()
    
    if interation % skip_frames == 0: 
        pygame.display.update() 
        pygame.display.set_caption(f'Langton\'s Ant - Python Edition - Iteration: {interation} - skip_frames: {skip_frames} - ct: {ct}')

    #if i press up arrow key increase skip_frames by 10 and if i press down arrow key decrease skip_frames by 10 - one acion per key stroke
    if event.type == pygame.KEYDOWN and keypressed == 0:
        keypressed = 1
        if event.key == pygame.K_UP and keypressed == 1:
            skip_frames += 10
        elif event.key == pygame.K_RIGHT and keypressed == 1:
            ct += 10
        elif event.key == pygame.K_DOWN and keypressed == 1 and skip_frames > 10:
            skip_frames -= 10
        elif event.key == pygame.K_LEFT and keypressed == 1 and ct > 10:
            ct -= 10

    if event.type == pygame.KEYUP:
        keypressed = 0   
    interation += 1
    
    
    clock.tick(ct)