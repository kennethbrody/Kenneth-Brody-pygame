# Example file showing a basic pygame "game loop"


import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions and create screen object
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Example: Movable Player")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player settings
player_size = 40
player_color = BLUE
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 5

# Background settings
background_color = WHITE

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key press handling
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Border wrapping (if the player moves off one edge, they appear on the opposite side)
    if player_x < 0:
        player_x = SCREEN_WIDTH
    elif player_x > SCREEN_WIDTH:
        player_x = 0

    if player_y < 0:
        player_y = SCREEN_HEIGHT
    elif player_y > SCREEN_HEIGHT:
        player_y = 0

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw the player (a blue square)
    pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
