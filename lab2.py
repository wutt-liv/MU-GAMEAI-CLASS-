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
                          radius= 100, 
                          color= (255,0,0))
        self.target = Vector2(0, 0)
        
    
    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        self.target = Vector2(mouse_pos_x, mouse_pos_y)
    
    def update(self, delta_time_ms):
        self.ball.seek_to(self.target)
        self.ball.update(delta_time_ms)

    def draw(self):
        self.screen.fill("grey")
        self.ball.draw(self.screen)
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
