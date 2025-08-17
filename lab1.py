#lab1
# Example file showing a basic pygame "game loop"
import pygame
from pygame.draw import circle, lines, rect
from pygame.math import Vector2

# pygame setup
pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

radius = 100
cycle_color = (255,0,0)
position = Vector2(screen_width/2,screen_height/2)
vel = Vector2(0,0)
acc = Vector2(0,0)

acc.x = 1
acc.y = 1

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    #draw a moving circle
    vel = vel + acc
    position = position + vel
    circle(screen, cycle_color, position, radius)
    acc.x = 0
    acc.y = 0

    #draw line
    linewidth = 3
    point1x = 1000
    point1y = 500 
    point2x = 600
    point2y = 500
    lines(screen, "red", True, [(point1x,point1y),(point2x,point2y)], linewidth)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    

pygame.quit()