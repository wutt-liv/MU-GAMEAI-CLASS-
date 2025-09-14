import pygame
from pygame.draw import circle, lines, rect
from pygame.math import Vector2
from agent import Agent

screen_width = 1280
screen_height = 720

class App:
    def __init__(self):
        print("Application is created")
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.CHAGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHAGE_DIR, 2000)
        self.running = True
        self.ball = Agent(position = Vector2(screen_width/2, screen_height/2), 
                          radius= 30, 
                          color= (100,0,0))
        self.agents = [
            Agent(position = Vector2(100, screen_height/2), 
                          radius= 30, 
                          color= (100,0,0)),
            Agent(position = Vector2(300, screen_height/2), 
                          radius= 30, 
                          color= (100,0,0)),
            Agent(position = Vector2(500, screen_height/2), 
                          radius= 30, 
                          color= (100,0,0))
        ]
        self.waypoints = [Vector2(100,0), Vector2(1000, 100), Vector2(0, 800)]
        self.current_waypoint_numbers = [0, 1, 2]  
        self.targets = [self.waypoints[self.current_waypoint_numbers[0]],
                        self.waypoints[self.current_waypoint_numbers[1]],
                        self.waypoints[self.current_waypoint_numbers[2]],
        ]   
    
    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        #mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_pos_x, mouse_pos_y)
    
    def update(self, delta_time_ms):
        '''d = self.ball.position - self.target
        dist = d.length()
        if dist < 5:
            self.current_waypoint_number += 1
            if self. current_waypoint_number <= len(self.waypoints):
                self.current_waypoint_number = 0
            
            self.target = self.waypoints[self.current_waypoint_number]
        self.ball.arrive_to(self.target)
        self.ball.update(delta_time_ms)'''

        for i, agent in enumerate(self.agents):
            d = agent.position - self.targets[i]
            dist = d.length()
            if dist < 5:
                self.current_waypoint_numbers[i] += 1
                if self. current_waypoint_numbers[i] >= len(self.waypoints):
                    self.current_waypoint_numbers[i] = 0
                    print(self.current_waypoint_numbers)
            
                self.targets[i] = self.waypoints[self.current_waypoint_numbers[i]]
            agent.arrive_to(self.targets[i])
            agent.update(delta_time_ms)

    def draw(self):
        self.screen.fill("grey")
        #self.ball.draw(self.screen)
        for agent in self.agents:
            agent.draw(self.screen)
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
