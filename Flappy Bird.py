"""
Name - Dhyanesh
Teacher - Ms. Strelkovska
Grade - 9
Date - 10 June 2025
Course Code - TEJ207
Game - Flappy Bird"""

import pygame
import random
import sys

# Setup
pygame.init()
pygame.display.set_caption("Flappy Bird")
WIDTH = 1280
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 45)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (235, 15, 15)

#Background

bg = pygame.image.load("FB bg.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Bird settings
bird_w = 60
bird_h = 60 
bird_x = 100
bird_y = 300
bird_speed = 0
gravity = 0.4

# Load bird image
bird_img = pygame.image.load("flappy bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (bird_w, bird_h)).convert_alpha() 

# Pipes
pipes = []
pipe_gap = 200 
pipe_timer = 1500
last_pipe_time = pygame.time.get_ticks()

# Score
score = 0
passed = []

# Game over image (scale to full screen)
gameover_img = pygame.image.load("gameover.png")
gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))  # Fill the screen

# Track highest score
highest_score = 0

# Game loopx
running = True
while running:
    clock.tick(60)
    screen.blit(bg, (0, 0)) 

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -8
            if event.key == pygame.K_s:
                running = True
            if event.key == pygame.K_e: 
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird_speed = -8
         
    # Bird movement
    bird_speed += gravity
    bird_y += bird_speed

    # Make pipes
    now = pygame.time.get_ticks()
    if now - last_pipe_time > pipe_timer:
        height = random.randint(150, 400)
        top = pygame.Rect(WIDTH, 0, 52, height)
        bottom = pygame.Rect(WIDTH, height + pipe_gap, 52, HEIGHT - height - pipe_gap)
        pipes.append((top, bottom))
        last_pipe_time = now

    # Move and draw pipes
    new_pipes = []
    for top, bottom in pipes:
        top.x -= 5
        bottom.x -= 5

        # Add score
        if top.x + top.width < bird_x and top not in passed:
            score += 1
            passed.append(top)

        if top.right > 0:
            new_pipes.append((top, bottom))
    pipes = new_pipes

    # Show score
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Collision
    bird_rect = pygame.Rect(bird_x, bird_y, bird_w, bird_h)
    for top, bottom in pipes:
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            running = False

    # If the bird goes out of the screen
    if bird_y < 0 or bird_y > HEIGHT:
        running = False

    # Draw pipes
    for top, bottom in pipes:
        pygame.draw.rect(screen, RED, top) 
        pygame.draw.rect(screen, RED, bottom)

    # Draw bird
    screen.blit(bird_img, (bird_x, bird_y))

    # Show highest score
    if score > highest_score:
        highest_score = score

    pygame.display.update()

# Game Over screen
while True:
    screen.blit(gameover_img, (0, 0))  
    # Show highest score at the top 
    high_score_text = font.render(f"Your Highest Score is: {highest_score}", True, (255, 255, 255))
    screen.blit(high_score_text, (WIDTH//2 - 251, 49)) 
    # Show instructions below the highest score
    text = font.render("Press 'R' to Restart, 'E' to Exit", True, (255, 0, 0))
    screen.blit(text, (WIDTH//2 - 251, 155)) 
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset the game if player presses 'R'
                bird_y = 300
                bird_speed = 0
                pipes = []
                score = 0
                passed = []
                last_pipe_time = pygame.time.get_ticks()
                running = True
                break
            if event.key == pygame.K_e:
                pygame.quit()
                sys.exit()
    if running:
        break
