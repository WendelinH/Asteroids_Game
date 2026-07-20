import os

import pygame
from constants import *
from database import ScoreDatabase
from player import *
from asteroid import *
from asteroidfield import *
from score import Score
from shot import Shot
from _version import VERSION


def main():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()     # Clock and delta time for FPS
    dt: float = 0.0

    updatable = pygame.sprite.Group()   # creates groups
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable) # adds player class to groups (x,y)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, drawable, updatable)

    asteroid_field = AsteroidField(screen)

    player = Player(x = screen.get_width() / 2, y = screen.get_height() / 2)

    game_over = False
    
    cursor = pygame.Surface((1, 1), pygame.SRCALPHA) # trying to make cursor invisible, does not work :(
    cursor.fill((0, 0, 0, 0))
    pygame.mouse.set_cursor((0, 0), cursor)

    background = pygame.image.load(os.path.join(BASE_PATH, "./image/background.png")).convert()
    
    while True:         # game loop, this updates the screen and check for user input

        for event in pygame.event.get():    # makes it so the game doesn't need ctrl + c, but the x button to close
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over == True:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return
                
        if not game_over:
            updatable.update(dt)
            for asteroid in asteroids.sprites():
                if asteroid.is_out_of_screen(screen):
                    asteroid.kill()
                    continue
                if player.collides_with(asteroid):  # uses player. collides with, else the circle collision would be used
                    game_over = True
                    db.save_score()

                for shot in shots.sprites():
                    if shot.is_out_of_screen(screen):
                        shot.kill()
                        continue
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        Score().increase()
                        break

        screen.blit(background, (0,0))
        for obj in drawable:
            obj.draw(screen)
        show_version(screen)
        
        if not game_over:
            Score().draw(screen, text_mid_font, "white")
        
        if game_over:   # draws the game over text
            overlay = pygame.Surface((screen.get_width(), screen.get_height()))
            overlay.set_alpha(20)
            overlay.fill("gray")
            screen.blit(overlay, (0, 0))

            text = gameover_font.render("GAME OVER", True, "red")
            rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 4))
            screen.blit(text, rect)

            exit_text = text_small_font.render("press esc to EXIT", True, "orange")
            exit_rect = exit_text.get_rect(center=rect.center)
            exit_rect.top += 55
            screen.blit(exit_text, exit_rect)

            restart_text = text_small_font.render("press R to RESTART", True, "blue")
            restart_rect = exit_text.get_rect(center=exit_rect.center)
            restart_rect.top += 25
            screen.blit(restart_text, restart_rect)

            Score().draw_leaderboard(screen, text_mid_font, "white", restart_rect.top)

        pygame.display.flip()       # brings picture to the screen
        dt = clock.tick(60) / 1000  # FPS limiter to 60

def show_version(screen: pygame.Surface):
    text = version_font.render(f"v{VERSION}", True, "#cdcdcd")
    rect = pygame.Vector2(screen.get_width() - 50, screen.get_height() - 50) - text.get_size()
    screen.blit(text, rect)

if __name__ == "__main__":  # makes it so the current window gets closed after restart
    pygame.init()

    pygame.font.init()
    main_font_path = os.path.join(BASE_PATH, "fonts/BoldPixels.ttf")
    version_font_path = os.path.join(BASE_PATH, "fonts/QuinqueFive.ttf")
    gameover_font = pygame.font.Font(main_font_path, 80)
    text_mid_font = pygame.font.Font(main_font_path, 50)
    text_small_font = pygame.font.Font(main_font_path, 30)
    version_font = pygame.font.Font(version_font_path, 20)

    db = ScoreDatabase()

    while True:
        restart = main()
        Score().reset()
        if restart is not True:
            break
