from __future__ import annotations
import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with(self, other: CircleShape) -> bool:
        return self.radius + other.radius > self.position.distance_to(other.position)
    
    def is_out_of_screen(self, screen: pygame.Surface) -> bool:
        if (self.position.x < - (self.radius + 20)
        or self.position.y < - (self.radius + 20)
        or self.position.x > screen.get_width() +  (self.radius + 20)
        or self.position.y > screen.get_height() +  (self.radius + 20)):
            return True
        return False