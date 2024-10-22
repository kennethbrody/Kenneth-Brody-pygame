# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load the background image
background = pygame.image.load("assets/backgroundColorDesert.png")  # Update the path to your image

# Scale the background to fit the screen
background = pygame.transform.scale(background, (800, 600))

running = True

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # RENDER YOUR GAME HERE
    screen.blit(background, (0, 0))  # Draw the background image

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
