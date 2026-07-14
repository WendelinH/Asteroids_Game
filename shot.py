from circleshape import *
from constants import SHOT_RADIUS, LINE_WIDTH, BASE_PATH
import pygame
import os

class Shot(CircleShape):
    image: pygame.Surface = None

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        if Shot.image is None:
            Shot.image = pygame.image.load(os.path.join(BASE_PATH, "./image/shot.png")).convert_alpha()

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.position - pygame.Vector2(self.image.get_size()) / 2)
        # pygame.draw.circle(screen, "green", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
