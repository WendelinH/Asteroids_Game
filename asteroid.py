import pygame
from circleshape import CircleShape
from player import *
from constants import LINE_WIDTH, BASE_PATH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS
import random
import os

class Asteroid(CircleShape):
    image_big: pygame.Surface = None
    image_mid: pygame.Surface = None
    image_small: pygame.Surface = None

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        if Asteroid.image_big is None:
            Asteroid.image_big = pygame.image.load(os.path.join(BASE_PATH, "./image/asteorid-big.png")).convert_alpha()
            Asteroid.image_mid = pygame.image.load(os.path.join(BASE_PATH, "./image/asteorid-mid.png")).convert_alpha()
            Asteroid.image_small = pygame.image.load(os.path.join(BASE_PATH, "./image/asteorid-small.png")).convert_alpha()
        if self.radius == ASTEROID_MAX_RADIUS:
            self.image = self.image_big
        elif self.radius == ASTEROID_MIN_RADIUS:
            self.image = self.image_small
        else:
            self.image = self.image_mid

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.position - pygame.Vector2(self.image.get_size()) / 2)
        # pygame.draw.circle(screen, "green", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        random_angle = random.uniform(20, 50)
        velocity_1 = self.velocity.rotate(random_angle)
        velocity_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid_1.velocity = velocity_1 * 1.2
        asteroid_2.velocity = velocity_2 * 1.2
    
    def is_out_of_screen(self, screen: Surface):
        if (self.position.x < -ASTEROID_MAX_RADIUS
        or self.position.y < -ASTEROID_MAX_RADIUS
        or self.position.x > screen.get_width() + ASTEROID_MAX_RADIUS
        or self.position.y > screen.get_height() + ASTEROID_MAX_RADIUS):
            return True
        return False