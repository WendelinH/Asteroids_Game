import pygame
from constants import *
from logger import log_state

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock() #Clock and delta time for FPS
    dt: float = 0.0
    
    while True:         #The game loop, this updates the screen and check for user input... I think
        log_state()
        for event in pygame.event.get():
            pass
        screen.fill("black")
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        print(dt)
        
        for event in pygame.event.get():    #makes it so the game doesn't need ctrl + c, but the x button to close
            if event.type == pygame.QUIT:
                return
        
        

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
