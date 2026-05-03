import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PvP Shooting Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Player properties
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
player1_x = 100
player1_y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
player2_x = SCREEN_WIDTH - 100 - PLAYER_WIDTH
player2_y = SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2
player_speed = 5

# Bullet properties
BULLET_WIDTH = 10
BULLET_HEIGHT = 5
bullets1 = []
bullets2 = []
bullet_speed = 10

# Game state
winner = None

def draw_player(x, y, color):
    """Draw a player."""
    pygame.draw.rect(screen, color, (x, y, PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_bullet(bullets, color):
    """Draw bullets."""
    for bullet in bullets:
        pygame.draw.rect(screen, color, bullet)

def check_collision(bullets, opponent_x, opponent_y):
    """Check if a bullet hits the opponent."""
    for bullet in bullets:
        if (opponent_x < bullet.x < opponent_x + PLAYER_WIDTH and
            opponent_y < bullet.y < opponent_y + PLAYER_HEIGHT):
            return True
    return False

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()

    # Player 1 movement (WASD)
    if keys[pygame.K_w] and player1_y > 0:
        player1_y -= player_speed
    if keys[pygame.K_s] and player1_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player1_y += player_speed
    if keys[pygame.K_a] and player1_x > 0:
        player1_x -= player_speed
    if keys[pygame.K_d] and player1_x < SCREEN_WIDTH // 2 - PLAYER_WIDTH:
        player1_x += player_speed

    # Player 2 movement (Arrow keys)
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= player_speed
    if keys[pygame.K_DOWN] and player2_y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player2_y += player_speed
    if keys[pygame.K_LEFT] and player2_x > SCREEN_WIDTH // 2:
        player2_x -= player_speed
    if keys[pygame.K_RIGHT] and player2_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player2_x += player_speed

    # Player 1 shooting (Space)
    if keys[pygame.K_e]:
        if len(bullets1) < 5:  # Limit bullets
            bullets1.append(pygame.Rect(player1_x + PLAYER_WIDTH, player1_y + PLAYER_HEIGHT // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT))

    # Player 2 shooting (Right Ctrl)
    if keys[pygame.K_RCTRL]:
        if len(bullets2) < 5:  # Limit bullets
            bullets2.append(pygame.Rect(player2_x - BULLET_WIDTH, player2_y + PLAYER_HEIGHT // 2 - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT))

    # Move bullets
    for bullet in bullets1:
        bullet.x += bullet_speed
        if bullet.x > SCREEN_WIDTH:
            bullets1.remove(bullet)

    for bullet in bullets2:
        bullet.x -= bullet_speed
        if bullet.x < 0:
            bullets2.remove(bullet)

    # Check for collisions
    if check_collision(bullets1, player2_x, player2_y):
        winner = "Player 1"
        running = False
    if check_collision(bullets2, player1_x, player1_y):
        winner = "Player 2"
        running = False

    # Draw everything
    draw_player(player1_x, player1_y, BLUE)
    draw_player(player2_x, player2_y, RED)
    draw_bullet(bullets1, BLUE)
    draw_bullet(bullets2, RED)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Display winner
screen.fill(WHITE)
font = pygame.font.Font(None, 74)
text = font.render(f"{winner} Wins!", True, BLACK)
screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()