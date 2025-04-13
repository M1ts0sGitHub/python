import sys, pygame

#  Setup pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Window title
pygame.display.set_caption("Pygame Tutorial 002")

# Tick rate
clock = pygame.time.Clock()
clock.tick(60)



running = True
while running:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            pygame.quit()
            sys.exit()


    pygame.display.flip()
    