import pygame
import random
import sys

# Setup
pygame.init()
pygame.display.set_caption("Flappy Bird")
WIDTH = 1700
HEIGHT = 1700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Bird settings
bird_w, bird_h = 45, 45
bird_x = 100
bird_y = 300
bird_speed = 0
gravity = 0.4

# Load bird image
bird_img = pygame.image.load("flappy bird.png").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (bird_w, bird_h))

# Pipes
pipes = []
pipe_gap = 150
pipe_timer = 1500
last_pipe_time = pygame.time.get_ticks()

bg = pygame.image.load("flappy-bird-background.jpg")

# Score
score = 0
passed = []

# Game loop
running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_speed = -8
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bird_speed = -8

    # Bird movement
    bird_speed += gravity
    bird_y += bird_speed
    screen.blit(bird_img, (bird_x, bird_y))

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
        pygame.draw.rect(screen, GREEN, top)
        pygame.draw.rect(screen, GREEN, bottom)

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

    pygame.display.update()

# Exit
pygame.quit()
sys.exit()
