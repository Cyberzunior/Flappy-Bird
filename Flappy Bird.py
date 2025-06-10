# Game state
running = True
game_over = False

# Button settings
button_color = (200, 0, 0)
button_rect = pygame.Rect(WIDTH // 2 - 70, HEIGHT // 2 + 40, 140, 50)

while running:
    clock.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Restart game
                bird_y = 300
                bird_speed = 0
                pipes = []
                passed = []
                score = 0
                game_over = False
                last_pipe_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    bird_y = 300
                    bird_speed = 0
                    pipes = []
                    passed = []
                    score = 0
                    game_over = False
                    last_pipe_time = pygame.time.get_ticks()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_speed = -8
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                bird_speed = -8

    if not game_over:
        # Bird movement
        bird_speed += gravity
        bird_y += bird_speed
        screen.blit(bird_img, (bird_x, bird_y))

        # Create pipes
        now = pygame.time.get_ticks()
        if now - last_pipe_time > pipe_timer:
            height = random.randint(150, 400)
            top = pygame.Rect(WIDTH, 0, 52, height)
            bottom = pygame.Rect(WIDTH, height + pipe_gap, 52, HEIGHT - height - pipe_gap)
            pipes.append((top, bottom))
            last_pipe_time = now

        # Move pipes
        new_pipes = []
        for top, bottom in pipes:
            top.x -= 5
            bottom.x -= 5
            pygame.draw.rect(screen, GREEN, top)
            pygame.draw.rect(screen, GREEN, bottom)

            if top.x + top.width < bird_x and top not in passed:
                score += 1
                passed.append(top)

            if top.right > 0:
                new_pipes.append((top, bottom))
        pipes = new_pipes

        # Collision
        bird_rect = pygame.Rect(bird_x, bird_y, bird_w, bird_h)
        for top, bottom in pipes:
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                game_over = True

        if bird_y > HEIGHT or bird_y < -50:
            game_over = True

        # Score display
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (10, 10))

    else:
        # Show Game Over
        over_text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 60))

        # Show Restart button
        pygame.draw.rect(screen, button_color, button_rect)
        restart_text = font.render("Restart", True, (255, 255, 255))
        screen.blit(restart_text, (button_rect.x + 20, button_rect.y + 10))

    pygame.display.update()

# Exit
pygame.quit()
sys.exit()
