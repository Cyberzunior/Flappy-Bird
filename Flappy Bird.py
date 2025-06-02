import pygame
import random
import sys

# Initializing the Pygame
pygame.init()
pygame.display.set_caption("Flappy Bird")

# Window
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 30)

# Colors 
WHITE = (255, 255, 255)
BLUE = (0, 163, 255)
GREEN = (0, 255, 32)
 
# Bird  
bird_width = 45
bird_height = 45 

def bird(x, y):
    bird = pygame.image.load("flappy bird.png").convert_alpha()
    bird = pygame.transform.scale(bird, (bird_width, bird_height)) 
    return bird 

# Pipes
def create_pipes(): 
    pipe_width = 52
    pipe_height = random.randint(150, 400)
    pipe_x = WIDTH
    pipe_gap = 150

    pipe_top = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    pipe_bottom = pygame.Rect(pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)

    return pipe_top, pipe_bottom

# Bird position
bird_x = 100    
bird_y = 300
bird_mass = 0.4
bird_speed = 0

# Pipes list
pipes = []

# Pipe timer
new_pipe = 1500
last_pipe_time = pygame.time.get_ticks()

# Score
score = 0
passed_pipes = []

# Game Loop
running = True
while running:
    clock.tick(60)  # FPS
    screen.fill(WHITE)

    screen.blit(bird(bird_x, bird_y), (bird_x, bird_y))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            running = False
  
        # Bird flap
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -8    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button  == 1:
                bird_speed = -8    

    # Bird physics
    bird_speed += bird_mass
    bird_y += bird_speed
    bird(bird_x, bird_y)

    # Pipe spawning
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

        # Count score when bird passes a pipe
        if top_pipe.x + top_pipe.width < bird_x and top_pipe not in passed_pipes:
            score += 1
            passed_pipes.append(top_pipe)

        if top_pipe.right > 0:
            new_pipes.append((top_pipe, bottom_pipe))

    pipes = new_pipes

    # Score number 
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))


 
    # Collisions with pipes and the bird
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    for top_pipe, bottom_pipe in pipes:
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
                running = False

    pygame.display.update()

# Quit
pygame.quit()
sys.exit()        
