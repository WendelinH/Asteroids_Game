import pygame
from constants import *
from logger import log_state, log_event
from player import *
from asteroid import *
from asteroidfield import *
import sys
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    clock = pygame.time.Clock() #Clock and delta time for FPS
    dt: float = 0.0

    updatable: pygame.sprite.Group  = pygame.sprite.Group()   # creates groups
    drawable: pygame.sprite.Group  = pygame.sprite.Group()
    asteroids: pygame.sprite.Group[Asteroid] = pygame.sprite.Group()
    shots: pygame.sprite.Group[Shot]  = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # adds player class to groups (x,y)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)

    asteroid_field = AsteroidField()

    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    while True:         # game loop, this updates the screen and check for user input... I think
        log_state()

        for event in pygame.event.get():    #makes it so the game doesn't need ctrl + c, but the x button to close
            if event.type == pygame.QUIT:
                return
            
        screen.fill("black")

        updatable.update(dt)
        for object in drawable:
            object.draw(screen)

        for asteroid in asteroids:      #collisions between shots and asteroids!
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        pygame.display.flip()       # brings picture to the screen
        dt = clock.tick(60) / 1000  # FPS limiter to 60
        

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
