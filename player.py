from pygame import Surface
from circleshape import *
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import *

class Player(CircleShape):
    def __init__(self, x: float, y: float,):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    def triangle(self) -> list[pygame.Vector2]:     #triangle function
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def is_near_line(self, edgepoint_1, edgepoint_2, asteroid_position, asteroid_radius): # chek for collision with triangle
        triangle_side = edgepoint_2 - edgepoint_1
        edge_to_asteroid = asteroid_position - edgepoint_1
        if triangle_side.length_squared() == 0:
            return edgepoint_1.distance_to(asteroid_position) < asteroid_radius
        scaler = edge_to_asteroid.dot(triangle_side) / triangle_side.length_squared()
        scaler = max(0, min(1, scaler))
        closest_point = edgepoint_1 + triangle_side * scaler
        if closest_point.distance_to(asteroid_position) < asteroid_radius:
            return True
        return False

    def collides_with(self, other: CircleShape) -> bool:    # creates the triangle sides, uses is_near_line()
        edgepoints = self.triangle()
        for i in range(len(edgepoints)):
            tup = (edgepoints[i], edgepoints[(i + 1) %3])
            if self.is_near_line(tup[0], tup[1], other.position, other.radius):
                return True
        return False

    def draw(self, screen: pygame.Surface) -> None:     #draws player sprite
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:        # rotater method
        self.rotation += PLAYER_TURN_SPEED * dt
        
    def move(self, dt: float) -> None:      # mover method
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        final_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += final_vector

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shot_cooldown -= dt
        self.speed = 0

        if keys[pygame.K_a]:    # rotation
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:    # movement
            self.move(dt)
            self.speed = PLAYER_SPEED
        if keys[pygame.K_s]:
            self.move(-dt)
            self.speed = -PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self) -> None:
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * (PLAYER_SHOOT_SPEED + self.speed)

    