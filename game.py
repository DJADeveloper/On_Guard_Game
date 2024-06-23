import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Advanced Fighting Game")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Game variables
player_size = 50
player_pos = [width // 2, height - player_size - 10]
player_speed = 10
player_jump = -15
player_health = 3
is_jumping = False
jump_speed = 10

enemy_size = 50
enemy_speed = 3
num_enemies = 5
enemies = [{'pos': [random.randint(0, width - enemy_size), random.randint(0, height // 2)], 'health': 1} for _ in range(num_enemies)]

projectile_size = 10
projectile_speed = 15
projectiles = []

gravity = 1
player_velocity_y = 0

score = 0
font = pygame.font.SysFont("monospace", 35)

# Load sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        player_velocity_y = player_jump
    if keys[pygame.K_SPACE]:
        if len(projectiles) < 5:  # Limit the number of projectiles on screen
            projectiles.append({'pos': [player_pos[0] + player_size // 2, player_pos[1]], 'speed': projectile_speed})
            shoot_sound.play()  # Play shoot sound

    # Apply gravity
    if is_jumping:
        player_velocity_y += gravity
        player_pos[1] += player_velocity_y
        if player_pos[1] >= height - player_size - 10:
            player_pos[1] = height - player_size - 10
            is_jumping = False
            player_velocity_y = 0

    # Update projectile positions
    for projectile in projectiles[:]:
        projectile['pos'][1] -= projectile['speed']
        if projectile['pos'][1] < 0:
            projectiles.remove(projectile)

    # Update enemy positions and check collisions
    for enemy in enemies[:]:
        if enemy['pos'][0] < player_pos[0]:
            enemy['pos'][0] += enemy_speed
        elif enemy['pos'][0] > player_pos[0]:
            enemy['pos'][0] -= enemy_speed

        if enemy['pos'][1] < player_pos[1]:
            enemy['pos'][1] += enemy_speed
        elif enemy['pos'][1] > player_pos[1]:
            enemy['pos'][1] -= enemy_speed

        # Check collision with player
        if abs(player_pos[0] - enemy['pos'][0]) < player_size and abs(player_pos[1] - enemy['pos'][1]) < player_size:
            player_health -= 1
            enemies.remove(enemy)
            enemies.append({'pos': [random.randint(0, width - enemy_size), random.randint(0, height // 2)], 'health': 1})
            hit_sound.play()  # Play hit sound
            if player_health <= 0:
                running = False

        # Check collision with projectiles
        for projectile in projectiles[:]:
            if abs(projectile['pos'][0] - enemy['pos'][0]) < enemy_size and abs(projectile['pos'][1] - enemy['pos'][1]) < enemy_size:
                enemy['health'] -= 1
                projectiles.remove(projectile)
                if enemy['health'] <= 0:
                    enemies.remove(enemy)
                    enemies.append({'pos': [random.randint(0, width - enemy_size), random.randint(0, height // 2)], 'health': 1})
                    score += 1
                    hit_sound.play()  # Play hit sound

    # Clear screen
    window.fill(white)

    # Draw player
    pygame.draw.rect(window, black, (*player_pos, player_size, player_size))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(window, red, (*enemy['pos'], enemy_size, enemy_size))

    # Draw projectiles
    for projectile in projectiles:
        pygame.draw.rect(window, blue, (*projectile['pos'], projectile_size, projectile_size))

    # Draw score and health
    score_text = font.render(f"Score: {score}", True, black)
    health_text = font.render(f"Health: {player_health}", True, black)
    window.blit(score_text, (10, 10))
    window.blit(health_text, (width - 150, 10))

    # Update display
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(30)

pygame.quit()