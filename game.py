import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Start background music (looped)
pygame.mixer.music.load("Kenneth-Brody-pygame/assets/mareux---the-perfect-girl-made-with-Voicemod.mp3")  # Path to the music file
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
pygame.mixer.music.play(-1)  # Loop the music indefinitely

# Set up screen dimensions and create screen object
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man-like Maze with NPCs")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PELT_COLOR = (0, 0, 0)  # Color of the pellet changed to black

# Player settings
player_size = 40
player_color = YELLOW
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
player_speed = 5

# Tile size (for the maze)
TILE_SIZE = 50

# Maze dimensions (based on screen size)
maze_width = SCREEN_WIDTH // TILE_SIZE
maze_height = SCREEN_HEIGHT // TILE_SIZE

# Directions for movement (up, right, down, left)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # (dy, dx)

# Function to generate the maze using recursive backtracking
def generate_maze():
    maze = [[1] * maze_width for _ in range(maze_height)]  # Start with walls everywhere
    stack = []

    # Start at a random cell
    start_y, start_x = random.randint(0, maze_height - 1), random.randint(0, maze_width - 1)
    maze[start_y][start_x] = 0  # Mark the start as a path
    stack.append((start_y, start_x))

    while stack:
        y, x = stack[-1]
        neighbors = []

        # Check all 4 possible directions
        for dy, dx in directions:
            ny, nx = y + dy * 2, x + dx * 2
            if 0 <= ny < maze_height and 0 <= nx < maze_width and maze[ny][nx] == 1:
                neighbors.append((dy, dx))

        if neighbors:
            dy, dx = random.choice(neighbors)
            ny, nx = y + dy * 2, x + dx * 2
            maze[ny][nx] = 0  # Mark as a path
            maze[y + dy][x + dx] = 0  # Remove the wall between the current cell and the new cell
            stack.append((ny, nx))  # Add the new cell to the stack
        else:
            stack.pop()  # Backtrack if there are no unvisited neighbors

    return maze

# Create a maze
maze = generate_maze()

# Function to draw the maze
def draw_maze():
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                # Draw the wall (blue)
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                # Draw the path (white)
                pygame.draw.rect(screen, WHITE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# NPC (Ghost) settings
ghost_size = 40
ghost_speed = 1  # Slow down the ghost speed (less than player speed)
ghosts = []

# Create 3 NPC ghosts
for _ in range(3):
    ghost_x = random.randint(0, maze_width - 1) * TILE_SIZE
    ghost_y = random.randint(0, maze_height - 1) * TILE_SIZE
    ghosts.append({'x': ghost_x, 'y': ghost_y})

# BFS to find the shortest path avoiding walls
def bfs(start, goal):
    queue = deque([start])
    parent = {start: None}
    visited = set()
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return path

        for dy, dx in directions:
            ny, nx = current[0] + dy, current[1] + dx
            if 0 <= ny < maze_height and 0 <= nx < maze_width and maze[ny][nx] == 0 and (ny, nx) not in visited:
                visited.add((ny, nx))
                parent[(ny, nx)] = current
                queue.append((ny, nx))

    return []  # Return empty path if no path exists

# Function to move the ghosts (chasing the player)
def move_ghosts(frame_count):
    # Only move the ghosts every 60 frames, or 1 second at 60 FPS
    if frame_count % 60 == 0:  
        for ghost in ghosts:
            # Convert ghost position to maze coordinates
            ghost_tile_x = ghost['x'] // TILE_SIZE
            ghost_tile_y = ghost['y'] // TILE_SIZE
            goal_x = player_x // TILE_SIZE
            goal_y = player_y // TILE_SIZE

            # Find path from ghost to player
            path = bfs((ghost_tile_y, ghost_tile_x), (goal_y, goal_x))

            if path:
                # Move ghost along the path (only move one step towards the player)
                next_y, next_x = path[1]  # Get the second tile in the path (the next step)
                ghost['x'] = next_x * TILE_SIZE
                ghost['y'] = next_y * TILE_SIZE

# Check if player collides with a ghost
def check_ghost_collision():
    global player_x, player_y
    for ghost in ghosts:
        ghost_rect = pygame.Rect(ghost['x'], ghost['y'], ghost_size, ghost_size)
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        if ghost_rect.colliderect(player_rect):
            return True
    return False

# Function to check if Pac-Man collects a pellet
def check_pellet_collision(pellets):
    global player_x, player_y, score
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    collected_pellets = []

    for pellet in pellets:
        pellet_rect = pygame.Rect(pellet[0], pellet[1], TILE_SIZE // 3, TILE_SIZE // 3)
        if player_rect.colliderect(pellet_rect):
            collected_pellets.append(pellet)

    # Remove collected pellets from the list
    for pellet in collected_pellets:
        pellet[2] = True  # Mark the pellet as collected (change its color to black)
        pellets.remove(pellet)  # Remove the pellet from the list
        score += 1  # Increment the score by 1 for each collected pellet

# Generate the initial list of pellets (placed throughout the entire maze)
def generate_pellets():
    pellets = []
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 0:  # Only place pellets in navigable areas
                # Create a pellet at each valid path position
                if random.random() < 0.2:  # Adjust this probability to control pellet density
                    pellets.append([x * TILE_SIZE + TILE_SIZE // 4, y * TILE_SIZE + TILE_SIZE // 4, False])  # Add collected status
    return pellets

# Initialize the list of pellets and the score
pellets = generate_pellets()
score = 0

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Font for displaying the score and instructions
font = pygame.font.SysFont("Arial", 24)

# Function to display the intro screen
def display_intro_screen():
    screen.fill(BLACK)
    title_font = pygame.font.SysFont("Arial", 48)
    instructions_font = pygame.font.SysFont("Arial", 32)
    
    # Title
    title_text = title_font.render("Pac-Man-like Game", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

    # Instructions
    instructions = [
        "Use the arrow keys to move",
        "Collect pellets",
        "Avoid ghosts!",
        "Press Space to continue"
    ]

    for i, text in enumerate(instructions):
        instruction_text = instructions_font.render(text, True, WHITE)
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, SCREEN_HEIGHT // 2 + i * 40))

    # Display everything
    pygame.display.flip()

    # Wait for space key to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False  # Exit intro screen

# Main game loop
def main():
    global player_x, player_y, pellets, score
    running = True
    frame_count = 0

    # Display the intro screen
    display_intro_screen()

    # Start the game loop
    while running:
        frame_count += 1
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movement logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # Keep the player inside the screen boundaries
        player_x = max(0, min(player_x, SCREEN_WIDTH - player_size))
        player_y = max(0, min(player_y, SCREEN_HEIGHT - player_size))

        # Move the ghosts
        move_ghosts(frame_count)

        # Check for collisions with ghosts
        if check_ghost_collision():
            print("Game Over! You were caught by a ghost.")
            running = False  # End the game if player collides with a ghost

        # Check if the player collects a pellet
        check_pellet_collision(pellets)

        # Draw the maze and other game elements
        draw_maze()

        # Draw the player
        pygame.draw.rect(screen, player_color, (player_x, player_y, player_size, player_size))

        # Draw the ghosts
        for ghost in ghosts:
            pygame.draw.rect(screen, RED, (ghost['x'], ghost['y'], ghost_size, ghost_size))

        # Draw pellets
        for pellet in pellets:
            if not pellet[2]:  # Only draw non-collected pellets
                pygame.draw.circle(screen, PELT_COLOR, (pellet[0], pellet[1]), TILE_SIZE // 6)

        # Display the score (changed font color to black)
        score_text = font.render(f"Score: {score}", True, BLACK)  # Font color changed to black
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.flip()

        # Frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main()
