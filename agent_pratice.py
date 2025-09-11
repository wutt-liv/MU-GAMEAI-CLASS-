
from pygame.draw import circle
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color):
        self.radius = radius
        self.cycle_color = color
        self.position = position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.mass = 1.0
    
    def escape_to(self, player_pos, screen_center):
        escape_distance = 300
        MAX_FORCE = 5
        STOP_RADIUS = 5

        d = player_pos - self.position
        if d.length_squared() == 0:
            return
        
        if d.length() < escape_distance:
            desired = d.normalize() * MAX_FORCE
            escape_desired = desired * -1
            steering = escape_desired - self.vel  
        
        else:
            toward_center = screen_center - self.position
            if toward_center.length_squared() > STOP_RADIUS:
                 desired = toward_center.normalize() * MAX_FORCE
                 steering = desired - self.vel
            
            else:
                self.vel = Vector2(0, 0)
                self.acc = Vector2(0, 0)
                return

        if steering.length() > MAX_FORCE:
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)


    def apply_force(self, force):
        self.acc += force / self.mass
    
    def update(self, delta_time_ms, player_pos, screen_width, screen_height):
        self.vel = self.vel + self.acc
        self.position = self.position + self.vel
        self.acc.x = 0
        self.acc.y = 0

        if self.position.x > screen_width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = screen_width

        if self.position.y > screen_height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = screen_height

    def draw(self,screen):
        circle(screen, self.cycle_color, self.position, self.radius)