
from pygame.draw import circle, line
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color):
        self.screen_width = 1280
        self.screen_height = 720
        self.radius = radius
        self.cycle_color = color
        self.position = position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.mass = 1.0
        self.EYE_SIGHT = 100
        self.STOP_DIST = 5
        self.detect_distance = 300
        self.safe_distance = 500
        self.origin_post = Vector2(self.screen_width/2,0)
        self.first_stop = Vector2(self.screen_width, self.screen_height/2)
        self.second_stop = Vector2(self.screen_width/2, self.screen_height)
        
    
    def seek_to(self, target_pos):
        MAX_FORCE = 5
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAX_FORCE
        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)

    def arrive_to(self, target_pos):
        '''add arriving bahavior here'''
        MAX_FORCE = 5

        d = target_pos - self.position

        if d.length_squared() == 0:
            return True
        
        dist = d.length() # square root is expensive in games
        if dist < self.STOP_DIST:
            desired = Vector2(0,0)

        elif dist < self.EYE_SIGHT:
            # slowing down forces
            desired = d.normalize() * (MAX_FORCE*(dist/self.EYE_SIGHT))
        else:
            desired = d.normalize() * MAX_FORCE

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        self.apply_force(steering)

    def flee_from(self, target_pos):
        MAX_FORCE = 5

        d = target_pos - self.position
        dist = d.length()
        if d.length_squared() == 0:
            return
        
        if dist > self.safe_distance:
            desired = Vector2(0,0)
        elif dist < self.detect_distance:
            desired = d.normalize() * (MAX_FORCE*(self.detect_distance/dist))*-1
        else:
            desired = Vector2(0,0)

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        self.apply_force(steering)

    def guard(self):
        MAX_FORCE = 5

        d = self.first_stop - self.position

        if d.length_squared() == 0:
            return
        
        dist = d.length()
        if dist < self.STOP_DIST:
            desired = Vector2(0,0)

        elif dist < self.EYE_SIGHT:
            # slowing down forces
            desired = d.normalize() * (MAX_FORCE*(dist/self.EYE_SIGHT))
        else:
            desired = d.normalize() * MAX_FORCE

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        self.apply_force(steering)
        


    def apply_force(self, force):
        self.acc += force / self.mass
    
    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc
        self.position = self.position + self.vel
        self.acc.x = 0
        self.acc.y = 0

    def draw(self,screen):
            
        circle(screen, (100,100,0), 
                self.position, self.EYE_SIGHT, width = 1)
        circle(screen, self.cycle_color, 
               self.position, self.radius)
    