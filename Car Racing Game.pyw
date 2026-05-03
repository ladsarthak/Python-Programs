import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Open-World Racing Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Car properties
CAR_WIDTH = 50
CAR_HEIGHT = 100
car_x = SCREEN_WIDTH // 2
car_y = SCREEN_HEIGHT - CAR_HEIGHT - 10
car_speed = 5

# AI cars
AI_CAR_WIDTH = 50
AI_CAR_HEIGHT = 100
ai_cars = [
    {"x": random.randint(200, 600), "y": random.randint(-600, -100), "speed": random.randint(3, 6)}
    for _ in range(3)
]

# Road properties
ROAD_WIDTH = 400
ROAD_LEFT = (SCREEN_WIDTH - ROAD_WIDTH) // 2
ROAD_RIGHT = ROAD_LEFT + ROAD_WIDTH
LINE_WIDTH = 5
LINE_HEIGHT = 50
LINE_GAP = 20
line_y = 0

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

def draw_road():
    """Draw the road and lane dividers."""
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, SCREEN_HEIGHT))
    for y in range(line_y, SCREEN_HEIGHT, LINE_HEIGHT + LINE_GAP):
        pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH // 2 - LINE_WIDTH // 2, y, LINE_WIDTH, LINE_HEIGHT))

def draw_car(x, y, color=BLUE):
    """Draw a car."""
    pygame.draw.rect(screen, color, (x, y, CAR_WIDTH, CAR_HEIGHT))

def display_score(score):
    """Display the current score."""
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > ROAD_LEFT:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < ROAD_RIGHT - CAR_WIDTH:
        car_x += car_speed
    if keys[pygame.K_UP] and car_y > 0:
        car_y -= car_speed
    if keys[pygame.K_DOWN] and car_y < SCREEN_HEIGHT - CAR_HEIGHT:
        car_y += car_speed

    # Move road lines
    line_y += 5
    if line_y > LINE_HEIGHT + LINE_GAP:
        line_y = 0

    # Move AI cars
    for ai_car in ai_cars:
        ai_car["y"] += ai_car["speed"]
        if ai_car["y"] > SCREEN_HEIGHT:
            ai_car["y"] = random.randint(-600, -100)
            ai_car["x"] = random.randint(ROAD_LEFT, ROAD_RIGHT - AI_CAR_WIDTH)
            ai_car["speed"] = random.randint(3, 6)
            score += 1

    # Check for collisions
    for ai_car in ai_cars:
        if (car_x < ai_car["x"] + AI_CAR_WIDTH and
            car_x + CAR_WIDTH > ai_car["x"] and
            car_y < ai_car["y"] + AI_CAR_HEIGHT and
            car_y + CAR_HEIGHT > ai_car["y"]):
            print("Game Over!")
            running = False

    # Draw everything
    draw_road()
    draw_car(car_x, car_y)
    for ai_car in ai_cars:
        draw_car(ai_car["x"], ai_car["y"], color=RED)
    display_score(score)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()