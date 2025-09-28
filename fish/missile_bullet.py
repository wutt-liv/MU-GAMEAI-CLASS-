import pygame
from pygame.draw import circle, rect
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color, respawn_pos = None):
        self.screen_width = 1280
        self.screen_height = 720
        self.radius = radius
        self.cycle_color = color
        self.position = position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.mass = 1.0
        self.EYE_SIGHT = 250
        self.HIT_DIST = 15
        self.MAX_speed = 1000
        self.fish_rocket_image = pygame.image.load('fish rocket.png').convert_alpha()
        self.fish_rocket_sprite_size = Vector2(320, 320)
        self.BLACK = (0,0,0)
        self.fish_rocket_scale = 0.4
        self.fish_rocket_animation_list = []
        self.fish_rocket_animation_step = 2
        self.fish_rocket_frame = 0
        self.cannon_sheet_image = pygame.image.load('feesh.png').convert_alpha()
        self.cannon_scale = 0.42
        self.cannon_sprite_size = Vector2(640, 320)
        self.cannon_frame = 0
        self.cannon_position = position
        self.respawn_pos = respawn_pos if respawn_pos else Vector2(0, 0)
        self.moving = False
        self.has_hit_target = False
        self.gravity = Vector2(0,0)

    def get_image(sheet, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        # add image to surface (image, position, image_area)
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        #Make colour tranparent
        image.set_colorkey(colour)
        return image

    def arrive_to(self, target_pos):
        MAX_FORCE = 80
        Thruster_Pow = 1.1

        d = target_pos - self.position
        dist = d.length() 

        if d.length_squared() == 0:
            return Vector2(0,0)
        
        if dist < self.HIT_DIST:
            return Vector2(0,0)

        elif dist < self.EYE_SIGHT:
            desired = d.normalize() * (self.MAX_speed*Thruster_Pow)
        else:
            desired = d.normalize() * self.MAX_speed

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        return steering
        
    def apply_force(self, force):
        self.acc += force / self.mass

    def set_gravity(self, gravity):
        self.gravity = gravity
    
    def update(self, delta_time_ms):
        delta_time = delta_time_ms/1000
        self.vel += (self.acc  + self.gravity) 
        
        if self.vel.length() > self.MAX_speed:
            self.vel.scale_to_length(self.MAX_speed)

        self.position += self.vel*delta_time
        self.vel *= 0.95
        self.acc.x = 0
        self.acc.y = 0

    def respawn_to_barrel(self, barrel_pos):
        self.position = barrel_pos + Vector2(160, 0)
        self.vel = Vector2(0, 0)
        self.moving = True
        self.has_hit_target = False

    def draw_BG(self,screen):
        circle(screen, self.cycle_color, self.position, self.radius)

    def barrel(self,screen, target_pos):
        fish_cannon = Agent.get_image(self.cannon_sheet_image, self.cannon_frame, 
                                     self.cannon_sprite_size.x, self.cannon_sprite_size.y,
                                     self.cannon_scale, self.BLACK)

        if target_pos is not None:
            direction = target_pos - self.position
            angle = direction.angle_to(Vector2(1, 0))  
        else:
            angle = 0
        
        rotated_cannon = pygame.transform.rotate(fish_cannon, angle)
        rotated_cannon_rect = rotated_cannon.get_rect(center = (self.position.x , self.position.y))
        screen.blit(rotated_cannon, rotated_cannon_rect.topleft)


    def draw(self,screen, target_pos):
        fish_rocket = Agent.get_image(self.fish_rocket_image, self.fish_rocket_frame, 
                                     self.fish_rocket_sprite_size.x, self.fish_rocket_sprite_size.y,
                                     self.fish_rocket_scale, self.BLACK)

        if target_pos is not None:
            direction = target_pos - self.position
            angle = direction.angle_to(Vector2(1, 0))  
        else:
            angle = 0
        
        #rotated_fish = pygame.transform.rotate(fish_rocket, angle*-1)
        #rotated_rect = rotated_fish.get_rect(center = (self.position.x, self.position.y))
        fish_rect = fish_rocket.get_rect(center = (self.position.x, self.position.y))

        screen.blit(fish_rocket, fish_rect.topleft)
        
        
        