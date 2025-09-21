import pygame
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
        self.detect_distance = 200
        self.safe_distance = 250
        self.panic_distance = 150
        self.MAX_speed = 300
        self.truck_sprite_sheet_image = pygame.image.load('truck.png').convert_alpha()
        self.truck_sprite_size = Vector2(64, 64)
        self.BLACK = (0,0,0)
        self.truck_scale = 2.0
        self.truck_animation_list = []
        self.truck_animation_list_rotate1 = []
        self.truck_animation_list_rotate2 = []
        self.truck_animation_list_rotate3 = []
        self.truck_animation_step = 2
        self.truck_frame = 0
        self.truck_rotate_angle1 = 270
        self.truck_rotate_angle2 = 180
        self.truck_rotate_angle3 = 90
        self.base_sheet_image = pygame.image.load('base.png').convert_alpha()
        self.base_scale = 5
        self.base_sprite_size = Vector2(128, 128)
        self.base_frame = 0
        self.base_position = Vector2(0, 50)
        self.dirt_sheet_image = pygame.image.load('dirt.png').convert_alpha()
        self.dirt_scale = 1
        self.dirt_sprite_size = Vector2(240, 720)
        self.dirt_frame = 0
        self.dirt_position = Vector2(self.screen_width-200, 0)
        self.waypoint1 = Vector2(self.screen_width-300,(self.screen_height/2)-240)
        self.waypoint2 = Vector2(self.screen_width-300,(self.screen_height/2)+100)
        self.waypoint3 = Vector2(-250,(self.screen_height/2)+100)
        self.waypoint4 = Vector2(-250, (self.screen_height/2)-240)
        self.waypoints = [self.waypoint1, self.waypoint2,
                          self.waypoint3,self.waypoint4]

    def get_image(sheet, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        # add image to surface (image, position, image_area)
        image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        #Make colour tranparent
        image.set_colorkey(colour)
        return image

    def arrive_to(self, target_pos):
        '''add arriving bahavior here'''
        MAX_FORCE = 30

        d = target_pos - self.position
        dist = d.length() # square root is expensive in games

        if d.length_squared() == 0:
            return Vector2(0,0)
        
        if dist < self.STOP_DIST:
            desired = Vector2(0,0)
            return Vector2(0,0)

        elif dist < self.EYE_SIGHT:
            # slowing down forces
            desired = d.normalize() * (self.MAX_speed*(dist/self.EYE_SIGHT))
        else:
            desired = d.normalize() * self.MAX_speed

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        return steering

    def flee_from(self, player_pos):
        MAX_FORCE_flee = 30
        if player_pos is None:
            return Vector2(0,0)

        d_flee = self.position - player_pos
        dist_flee = d_flee.length()
        if d_flee.length_squared() == 0:
            return Vector2(0,0)
        
        if 0 < dist_flee < self.safe_distance:
            if 0 < dist_flee < self.panic_distance:
                desired_flee = d_flee.normalize() * (self.MAX_speed)
            else:
                desired_flee = d_flee.normalize() * (self.MAX_speed*((self.safe_distance - dist_flee)/self.panic_distance))
            steering_flee = desired_flee - self.vel 
            if steering_flee.length() > MAX_FORCE_flee: 
                steering_flee.scale_to_length(MAX_FORCE_flee)
            return steering_flee
        else:
            desired_flee = Vector2(0,0)
            return Vector2(0,0)
        
    def apply_force(self, force):
        self.acc += force / self.mass
    
    def update(self, delta_time_ms):
        delta_time = delta_time_ms/1000
        self.vel += self.acc 
        
        if self.vel.length() > self.MAX_speed:
            self.vel.scale_to_length(self.MAX_speed)

        self.position += self.vel*delta_time
        self.vel *= 0.95
        self.acc.x = 0
        self.acc.y = 0

    def draw_BG(self,screen):
        base_image = Agent.get_image(self.base_sheet_image, self.base_frame, 
                                     self.base_sprite_size.x, self.base_sprite_size.y,
                                     self.base_scale, self.BLACK)
        dirt_image = Agent.get_image(self.dirt_sheet_image, self.dirt_frame, 
                                     self.dirt_sprite_size.x, self.dirt_sprite_size.y,
                                     self.dirt_scale, self.BLACK)
        
        screen.blit(base_image, self.base_position)
        screen.blit(dirt_image, self.dirt_position)

    def draw(self,screen):
        rotate1_truck = pygame.transform.rotate(self.truck_sprite_sheet_image, self.truck_rotate_angle1)
        rotate2_truck = pygame.transform.rotate(self.truck_sprite_sheet_image, self.truck_rotate_angle2)
        rotate3_truck = pygame.transform.rotate(self.truck_sprite_sheet_image, self.truck_rotate_angle3)
        

        for i in range(self.truck_animation_step):
            self.truck_animation_list_rotate1.append (Agent.get_image(rotate1_truck,
                                                i, self.truck_sprite_size.x,
                                                self.truck_sprite_size.y, self.truck_scale,
                                                self.BLACK))
        
        for i in range(self.truck_animation_step):
            self.truck_animation_list_rotate2.append (Agent.get_image(rotate2_truck,
                                                i, self.truck_sprite_size.x,
                                                self.truck_sprite_size.y, self.truck_scale,
                                                self.BLACK))
            
        for i in range(self.truck_animation_step):
            self.truck_animation_list_rotate3.append (Agent.get_image(rotate3_truck,
                                                i, self.truck_sprite_size.x,
                                                self.truck_sprite_size.y, self.truck_scale,
                                                self.BLACK))
            
        for i in range(self.truck_animation_step):
            self.truck_animation_list.append (Agent.get_image(self.truck_sprite_sheet_image,
                                                i, self.truck_sprite_size.x,
                                                self.truck_sprite_size.y, self.truck_scale,
                                                self.BLACK))
        
        if self.position.distance_to(self.waypoint1) < 3:
            self.truck_frame += 1
            if self.truck_frame >= len(self.truck_animation_list_rotate1):
                self.truck_frame = 0

        sprite_to_draw = self.truck_animation_list[self.truck_frame]  

        if abs(self.vel.x) > abs(self.vel.y):  
            if self.vel.x > 1:
                sprite_to_draw = self.truck_animation_list_rotate1[self.truck_frame]        
            elif self.vel.x < -1:
                sprite_to_draw = self.truck_animation_list_rotate3[self.truck_frame] 
        else:  
            if self.vel.y > 1:
                sprite_to_draw = self.truck_animation_list_rotate2[self.truck_frame] 
            elif self.vel.y < -1:
                sprite_to_draw = self.truck_animation_list[self.truck_frame]

        screen.blit(sprite_to_draw, self.position)
        circle(screen, (100,100,0), 
                self.position + (self.truck_sprite_size), self.panic_distance, width = 1)
        