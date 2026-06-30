import pygame
from constants import *
from logger import log_state, log_event
from player import *
from asteroid import *
from asteroidfield import *
import sys
from shot import Shot

# TODO: Game over screen

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) 
    import constants 
    constants.SCREEN_WIDTH = screen.get_width() 
    constants.SCREEN_HEIGHT = screen.get_height()
    clock = pygame.time.Clock() #Clock and delta time for FPS
    dt: float = 0.0

    updatable = pygame.sprite.Group()   # creates groups
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # adds player class to groups (x,y)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)

    asteroid_field = AsteroidField()

    player = Player(x = screen.get_width() / 2, y = screen.get_height() / 2)

    pygame.font.init()
    font = pygame.font.Font(None, 80)
    game_over = False
    
    while True:         # game loop, this updates the screen and check for user input... I think
        log_state()

        for event in pygame.event.get():    #makes it so the game doesn't need ctrl + c, but the x button to close
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                
        if not game_over:
            updatable.update(dt)
            for asteroid in asteroids.sprites():
                if asteroid.collides_with(player):
                    game_over = True

                for shot in shots.sprites():
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        break

        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        
        if game_over:
            text = font.render("GAME OVER", True, "white")
            rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(text, rect)

        pygame.display.flip()       # brings picture to the screen
        dt = clock.tick(60) / 1000  # FPS limiter to 60
        

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
