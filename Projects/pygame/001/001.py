import sys, pygame

#  Setup pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# Window title
pygame.display.set_caption("Pygame Tutorial 001")

# Tick rate
clock = pygame.time.Clock()
clock.tick(60)

pressed_key_timestamp = 0
check_flag = False

running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pressed_key_timestamp = pygame.time.get_ticks()
            check_flag = True
            if event.key == pygame.K_LEFT:
                print("Left")
                screen.fill((188,188,122))
            if event.key == pygame.K_RIGHT:
                print("Right")
                screen.fill((188,122,188))
            if event.key == pygame.K_UP:
                print("Up")
                screen.fill((122,188,188))
            if event.key == pygame.K_DOWN:
                print("Down")
                screen.fill((188,188,188))
    if current_time - pressed_key_timestamp > 1000 and check_flag == True:
        screen.fill((0,0,0))
        print(current_time - pressed_key_timestamp)
        check_flag = False

    pygame.display.flip()
    