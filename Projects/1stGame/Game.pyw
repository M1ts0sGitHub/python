# https://www.youtube.com/watch?v=RuTmd4g5K8Q&t=2697s

import pygame, random, time, os

#Load Assets from current directory
background = pygame.image.load(os.path.join("python/1stgame/Assets", "background.png"))
icon = pygame.image.load(os.path.join("python/1stgame/Assets", "icon.png"))

#Settings
window_size = (500, 500)
window = pygame.display.set_mode(window_size) #, pygame.NOFRAME)
pygame.font.init()
pygame.display.set_caption("Alien Invaders")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
starting_time = time.time()
elapsed_time = 0

#Font
font = pygame.font.SysFont("comicsans", 30)

#player Settings
player_size = 10, 25
player_x, player_y = (window_size[0]+player_size[0])/2 , window_size[1]-player_size[1]
player_speed = 5
player = pygame.Rect(player_x, player_y, player_size[0], player_size[1])


def main():
    run = True

    while run:
        #quit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        clock.tick(60)
        elapsed_time = time.time() - starting_time

        #move player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < window_size[0]-player_size[0]:
            player.x += player_speed


        draw(player, elapsed_time)

    pygame.quit()

def draw(player, elapsed_time):
    window.blit(background, (0,0))
    score = font.render(f"Score: {int(elapsed_time)}", 1, (255, 255, 255))
    window.blit(score, (5, 5))
    pygame.draw.rect(window,"red", player)
    pygame.display.update()



if __name__ == "__main__":
    main()