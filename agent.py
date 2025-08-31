
from pygame.draw import circle
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color):
        self.radius = radius
        self.cycle_color = color
        self.position = position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.acc.x = 1
        self.acc.y = 1
    
    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc
        self.position = self.position + self.vel
        self.acc.x = 0
        self.acc.y = 0

    def draw(self,screen):
        circle(screen, self.cycle_color, self.position, self.radius)