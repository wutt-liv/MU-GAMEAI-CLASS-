
from pygame.draw import circle
from pygame.math import Vector2

class Agent:
    def __init__(self):
        self.radius = 100
        self.cycle_color = (255,0,0)
        self.position = Vector2(200,200)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.acc.x = 1
        self.acc.y = 1
    
    def update(self):
        self.vel = self.vel + self.acc
        self.position = self.position + self.vel
        self.acc.x = 0
        self.acc.y = 0

    def draw(self,screen):
        circle(screen, self.cycle_color, self.position, self.radius)