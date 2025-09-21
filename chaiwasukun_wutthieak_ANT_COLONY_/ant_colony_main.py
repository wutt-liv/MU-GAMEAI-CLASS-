import pygame
from pygame.draw import circle, lines, rect
from pygame.math import Vector2
from ant_colony_ant import Agent

screen_width = 1280
screen_height = 720

class App:
    def __init__(self):
        print("Application is created")
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Ant_Colony")
        self.clock = pygame.time.Clock()
        self.CHAGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHAGE_DIR, 2000)
        self.running = True
        self.player_pos = None

        self.agents = [
            Agent(position = Vector2(-300, (screen_height/2)-240), 
                          radius= 10, 
                          color= (100,0,0)),
            Agent(position = Vector2(-1200, (screen_height/2)-240), 
                          radius= 10, 
                          color= (100,0,0)),
            Agent(position = Vector2(-2100, (screen_height/2)-240), 
                          radius= 10, 
                          color= (100,0,0))
        ]

        self.waypoints = self.agents[0].waypoints
        self.current_waypoint_numbers = [0, 0, 0]  
        self.targets = [self.waypoints[self.current_waypoint_numbers[0]],
                        self.waypoints[self.current_waypoint_numbers[0]],
                        self.waypoints[self.current_waypoint_numbers[0]],
        ]   
    
    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        if pygame.mouse.get_focused():
            self.player_pos = Vector2(pygame.mouse.get_pos())
        else:
            self.player_pos = None
    
    def update(self, delta_time_ms):
        MAX_FORCE = 30
        for i, agent in enumerate(self.agents):
            d = agent.position - self.targets[i]
            dist = d.length()
            if dist < 10:
                self.current_waypoint_numbers[i] += 1
                if self. current_waypoint_numbers[i] >= len(self.waypoints):
                    self.current_waypoint_numbers[i] = 0
                    #print(self.current_waypoint_numbers)
                self.targets[i] = self.waypoints[self.current_waypoint_numbers[i]]
            arrive_force = agent.arrive_to(self.targets[i])
            flee_force = agent.flee_from(self.player_pos)
            combine_force = arrive_force + flee_force

            if combine_force.length() > MAX_FORCE:
                combine_force.scale_to_length(MAX_FORCE)
            
            agent.apply_force(combine_force)
            agent.update(delta_time_ms)

    def draw(self):
        self.screen.fill("grey")
        for agent in self.agents:
            agent.draw(self.screen)

        self.agents[0].draw_BG(self.screen)
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
