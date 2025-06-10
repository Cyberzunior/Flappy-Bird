import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.display.set_caption("Flappy Bird")

# Window setup
WIDTH, HEIGHT = 1700, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 30)

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 163, 255)
GREEN = (0, 255, 32)

# Bird setup
bird_width = 45
bird_height = 45
bird_x = 100
bird_y = 300
bird_mass = 0.4
bird_speed = 0

# Pipes setup
pipes = []
new_pipe = 1500  # milliseconds
last_pipe_time = pygame.time.get_ticks()

# Score
score = 0
passed_pipes = []

def create_pipes():
    pipe_width = 52
    pipe_height = random.randint(150, 400)
    pipe_x = WIDTH
    pipe_gap = 150

    pipe_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)
    return pipe_top, pipe_bottom

def reset_game():
    global bird_y, bird_speed, pipes, score, passed_pipes, last_pipe_time
    bird_y = 300
    bird_speed = 0
    pipes = []
    score = 0
    passed_pipes = []
    last_pipe_time = pygame.time.get_ticks()

def run_game():
    global bird_y, bird_speed, pipes, score, passed_pipes, last_pipe_time

    running = True
    game_over = False

    while running:
        clock.tick(60)
        screen.fill(WHITE)

        # Draw bird as a blue square
        pygame.draw.rect(screen, BLUE, (bird_x, bird_y, bird_width, bird_height))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird_speed = -8
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    bird_speed = -8
            else:
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    reset_game()
                    run_game()
                    return

        if not game_over:
            # Gravity
            bird_speed += bird_mass
            bird_y += bird_speed

            # Create new pipes
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_time > new_pipe:
                pipes.append(create_pipes())
                last_pipe_time = current_time

            # Move and draw pipes
            new_pipes = []
            for top_pipe, bottom_pipe in pipes:
                top_pipe.x -= 5
                bottom_pipe.x -= 5
                pygame.draw.rect(screen, GREEN, top_pipe)
                pygame.draw.rect(screen, GREEN, bottom_pipe)

                if top_pipe.x + top_pipe.width < bird_x and top_pipe not in passed_pipes:
                    score += 1
                    passed_pipes.append(top_pipe)

                if top_pipe.right > 0:
                    new_pipes.append((top_pipe, bottom_pipe))

            pipes = new_pipes

            # Collision
            bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
            for top_pipe, bottom_pipe in pipes:
                if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                    game_over = True

            if bird_y > HEIGHT or bird_y < -50:
                game_over = True

        # Score display
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Game Over screen
        if game_over:
            over_text = FONT.render("Game Over! Click to Restart", True, (255, 0, 0))
            screen.blit(over_text, (40, HEIGHT // 2))

        pygame.display.update()

# Start the game
run_game()
pygame.quit()
sys.exit()
