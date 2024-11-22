import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bird Bounce Game")

# Load the bird image
bird_img = pygame.image.load('assets/images/bird.png')
bird_img = pygame.transform.scale(bird_img, (50, 50))  # Resize bird to 50x50 pixels

# Pipe settings
PIPE_WIDTH = 80
PIPE_COLOR = (0, 200, 0)
PIPE_GAP = 200  # Gap between pipes for the bird to pass through

# Initialize bird position and speed
bird_x, bird_y = 100, 300
bird_speed_y = 0  # Start with no vertical speed

# Gravity and fly speed
gravity = 0.5
fly_speed = -10  # Negative speed to make the bird "fly" upwards

# Score
score = 0
high_score = 0

# Generate random pipes
def generate_pipes():
    pipe_height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 150)
    return {"top": pipe_height, "bottom": pipe_height + PIPE_GAP}

# List of pipes
pipes = [generate_pipes() for _ in range(3)]
pipe_positions = [400, 700, 1000]  # X positions of pipes

# Font setup
font = pygame.font.SysFont("Arial", 24)

# Game loop
running = True
clock = pygame.time.Clock()

def display_message(text, color, y_offset=0):
    message = font.render(text, True, color)
    screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 + y_offset))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Spacebar to make the bird fly
                bird_speed_y = fly_speed

    # Apply gravity to bird
    bird_speed_y += gravity
    bird_y += bird_speed_y

    # Move pipes to the left
    for i in range(len(pipe_positions)):
        pipe_positions[i] -= 2  # Speed of pipes moving left
        if pipe_positions[i] < -PIPE_WIDTH:  # Reset pipes when they go off-screen
            pipe_positions[i] = SCREEN_WIDTH
            pipes[i] = generate_pipes()

    # Clear the screen
    screen.fill((255, 255, 255))  # White background

    # Draw pipes
    for i in range(len(pipe_positions)):
        pygame.draw.rect(screen, PIPE_COLOR, (pipe_positions[i], 0, PIPE_WIDTH, pipes[i]["top"]))
        pygame.draw.rect(screen, PIPE_COLOR, (pipe_positions[i], pipes[i]["bottom"], PIPE_WIDTH, SCREEN_HEIGHT - pipes[i]["bottom"]))

    # Draw the bird
    screen.blit(bird_img, (bird_x, bird_y))

    # Check for collisions with pipes
    collision = False
    for i in range(len(pipe_positions)):
        if (bird_x + 50 > pipe_positions[i] and bird_x < pipe_positions[i] + PIPE_WIDTH and
            (bird_y < pipes[i]["top"] or bird_y + 50 > pipes[i]["bottom"])):
            collision = True
            break

    # Check for collision with the screen edges
    if bird_y < 0 or bird_y + 50 > SCREEN_HEIGHT:
        collision = True

    if collision:
        if score > high_score:
            high_score = score

        # Display Game Over screen
        screen.fill((255, 255, 255))  # Clear screen
        display_message("Game Over!", (255, 0, 0), -50)
        display_message(f"Your Score: {score}", (0, 0, 0), 0)
        display_message(f"High Score: {high_score}", (0, 0, 0), 50)
        display_message("Press R to Restart or Q to Quit", (0, 0, 0), 100)
        pygame.display.update()

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Quit the game
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:  # Restart the game
                        # Reset game variables
                        bird_x, bird_y = 100, 300
                        bird_speed_y = 0
                        pipes = [generate_pipes() for _ in range(3)]
                        pipe_positions = [400, 700, 1000]
                        score = 0
                        game_over = False

    # Increase score as the bird successfully passes pipes
    for i in range(len(pipe_positions)):
        if bird_x > pipe_positions[i] + PIPE_WIDTH and not pipes[i].get('scored', False):
            score += 1
            pipes[i]['scored'] = True  # Mark pipe as passed for scoring

    # Draw score on the screen
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Draw high score on the screen
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 10))

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(30)
