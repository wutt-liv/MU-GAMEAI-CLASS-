import pygame
from pygame.draw import circle, lines, rect
from pygame.math import Vector2
from missile_bullet import Agent

screen_width = 1280
screen_height = 720

class App:
    def __init__(self):
        print("Application is created")
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Missile_Boom_Boom")
        self.clock = pygame.time.Clock()
        self.CHAGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHAGE_DIR, 2000)
        self.running = True
        self.player_pos = None
        self.missile_position = Vector2(100, (screen_height/2) - 30)
        self.hit_range = 15
        self.missile_space = Vector2(0,60)
        self.turret_pos = Vector2(150, (screen_height/2) - 110)
        self.barrel_pos = self.turret_pos + Vector2(0, 50)
        self.barrel = [Agent(position = self.turret_pos ,
                                                radius = 50, color = (84, 84, 84), respawn_pos = Vector2(0,0) )]
        self.Background = [Agent(position = self.turret_pos,
                                                radius = 50, color = (84, 84, 84), respawn_pos = Vector2(0,0) )]
        self.agents = [
                        Agent(position = self.missile_position + (self.missile_space * i),
                                                radius = 30, color = (255, 0, 0),
                            respawn_pos = self.missile_position + (self.missile_space * i)) 
                        
                        for i in range(1, 6)                                         
                                                ]
        self.max_agents = 5
        
        self.agents[0].mass = 5  
        self.agents[1].mass = 5
        self.agents[2].mass = 5
        self.agents[3].mass = 5
        self.agents[4].mass = 5

        self.agents[0].set_gravity(Vector2(0,3)) 
        self.agents[1].set_gravity(Vector2(0,3)) 
        self.agents[2].set_gravity(Vector2(0,3)) 
        self.agents[3].set_gravity(Vector2(0,3))
        self.agents[4].set_gravity(Vector2(0,3))
 
    
    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for agent in self.agents:
                            if not agent.moving:
                                agent.respawn_to_barrel(self.barrel_pos)
                                break
        
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        self.player_pos = Vector2(mouse_pos_x, mouse_pos_y)
    
    def update(self, delta_time_ms):
        
        MAX_FORCE = 80
        for agent in self.agents:    
            if agent.moving:      
                arrive_force = agent.arrive_to(self.player_pos)
                combine_force = arrive_force 

                if combine_force.length() > MAX_FORCE:
                    combine_force.scale_to_length(MAX_FORCE)
            
                agent.apply_force(combine_force)
                agent.update(delta_time_ms)

                if (agent.position - self.player_pos).length() < self.hit_range:
                    agent.position = agent.respawn_pos
                    agent.vel = Vector2(0, 0)
                    agent.moving = False
                    agent.has_hit_target = True


    def draw(self):
        self.screen.fill("grey")
        self.Background[0].draw_BG(self.screen)
        self.barrel[0].barrel(self.screen, self.player_pos)
        for agent in self.agents:
            agent.draw(self.screen, self.player_pos)

        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time_ms = self.clock.tick(60)
            self.handle_input()
            self.update(delta_time_ms)
            self.draw()
 
        pygame.quit()

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
