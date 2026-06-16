from circleshape import *
from constants import PLAYER_RADIUS

class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float, rotation: float):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

    