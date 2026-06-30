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

    player = Player(x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2)
    
    while True:         # game loop, this updates the screen and check for user input... I think
        log_state()

        for event in pygame.event.get():    #makes it so the game doesn't need ctrl + c, but the x button to close
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            
        screen.fill("black")

        updatable.update(dt)
        for object in drawable:
            object.draw(screen)

        # FIXME: death after asteroid shot ghost hitbox

        for asteroid in asteroids.sprites(): 
            if asteroid.collides_with(player): 
                log_event("player_hit") 
                print("Game over!") 
                sys.exit() 
                
            for shot in shots.sprites(): 
                if asteroid.collides_with(shot): 
                    log_event("asteroid_shot") 
                    asteroid.split() 
                    shot.kill() 
                    break

        pygame.display.flip()       # brings picture to the screen
        dt = clock.tick(60) / 1000  # FPS limiter to 60
        

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
