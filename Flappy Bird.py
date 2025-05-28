import pygame
from pygame.locals import *

# Pygame initialization
pygame.init()

screen_height = 936
screen_width = 864

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")


#images
bg = pygame.image.load




run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()
    
