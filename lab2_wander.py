import pygame
import pygame_gui
from pygame.draw import circle, lines, rect
from pygame.math import Vector2
from agent import Agent
import random
import math

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
        self.timer = 0
        #self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        #self.manager = pygame_gui.UIManager((self.screen_width, self.screen_height))
        #self.horizonslider = pygame_gui.elements.UIHorizontalSlider(relative_rect = pygame.rect((50, 50, 200, 30)),
                                                                    #start_value = 0,
                                                                    #value_range = (0, 100),
                                                                    #manager = self.manager)
        #self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                                #text='Say Hello',
                                                #manager=self.manager)
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

        for agent in self.agents:
            agent.vel = Vector2(1,0)

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

                #if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                    #hasattr(event, 'ui_element') and event.ui_element == self.hello_button):
                    
                    #print('Hello World!')

                #self.manager.process_events(event)

        #mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_pos_x, mouse_pos_y)
    
    def update(self, delta_time_s):

        #self.manager.update(delta_time_s)
        self.timer += delta_time_s
        time_limit = 1

        for i, agent in enumerate(self.agents):
            target = agent.position + (agent.vel.normalize() * 200)
            if self.timer > time_limit:
                theta = random.randint(-90, 90)
                target += Vector2(math.cos(theta), math.sin(theta)) * 50
                
                
            agent.arrive_to(target)
            agent.update(delta_time_s)
        
        if self.timer > time_limit:
            self.timer = 0
        

    def draw(self):
        self.screen.fill("grey")
        
        for agent in self.agents:
            agent.draw(self.screen)

        #self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time_s = self.clock.tick(60)/1000
            self.handle_input()
            self.update(delta_time_s)
            self.draw()
 
        
        pygame.quit()

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()