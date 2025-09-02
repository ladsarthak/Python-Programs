import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 6

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (150, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)

# Soil Data
SOIL_LEVELS = [
    {"name": "Alluvial", "mineral": "Potash", "bg": (235, 222, 164), "food_color": GREEN, "fact": "Alluvial soil is fertile and great for farming."},
    {"name": "Black Soil", "mineral": "Lime", "bg": (50, 50, 50), "food_color": YELLOW, "fact": "Black soil is good for cotton and retains moisture."},
    {"name": "Red Soil", "mineral": "Iron", "bg": (165, 42, 42), "food_color": RED, "fact": "Red soil is rich in iron but low in fertility."},
    {"name": "Laterite", "mineral": "Aluminium", "bg": (210, 105, 30), "food_color": BROWN, "fact": "Laterite soil is found in areas with heavy rainfall."},
    {"name": "Desert Soil", "mineral": "Phosphates", "bg": (237, 201, 175), "food_color": WHITE, "fact": "Desert soil is sandy and low in moisture."},
    {"name": "Mountain Soil", "mineral": "Humus", "bg": (170, 170, 170), "food_color": GRAY, "fact": "Mountain soil is rich in humus and found in hilly areas."}
]

# Fonts
font = pygame.font.SysFont("comicsansms", 30)
small_font = pygame.font.SysFont("arial", 20)

# Display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake of the Soil 🐛")

# Helper Functions
def draw_worm_block(color, pos):
    center = (pos[0] + BLOCK_SIZE // 2, pos[1] + BLOCK_SIZE // 2)
    pygame.draw.circle(win, color, center, BLOCK_SIZE // 2)

def random_food():
    return [random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE),
            random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]

def show_message(text, y, color=BLACK, font_size=30):
    font_obj = pygame.font.SysFont("comicsansms", font_size)
    label = font_obj.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, y))
    win.blit(label, rect)

def draw_soil_patches(level):
    patch_color = tuple(max(c - 30, 0) for c in SOIL_LEVELS[level]["bg"])
    for _ in range(100):
        x = random.randint(0, WIDTH - BLOCK_SIZE)
        y = random.randint(0, HEIGHT - BLOCK_SIZE)
        pygame.draw.rect(win, patch_color, (x, y, 4, 4))

def draw_label_with_border(text, pos, base_color, bg_color, font_size=30):
    label = font.render(text, True, base_color)
    bg = font.render(text, True, bg_color)
    for dx in [-2, 2]:
        for dy in [-2, 2]:
            win.blit(bg, (pos[0]+dx, pos[1]+dy))
    win.blit(label, pos)

def start_screen():
    win.fill((120, 200, 150))
    show_message("Geography Culmination", HEIGHT // 2 - 180, BLACK, 50)
    show_message("Snake of the Soil", HEIGHT // 2 - 80, BLACK, 40)
    show_message("Press SPACE to start", HEIGHT // 2, BLACK, 30)
    show_message("Use arrow keys to move. Eat minerals to grow. Survive the soils!", HEIGHT // 2 + 80, BLACK, 20)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def game_loop():
    clock = pygame.time.Clock()
    snake = [[100, 50]]
    direction = [BLOCK_SIZE, 0]
    food = random_food()
    score = 0
    level = 0

    running = True
    game_over = False

    while running:
        clock.tick(FPS + level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != [BLOCK_SIZE, 0]:
            direction = [-BLOCK_SIZE, 0]
        if keys[pygame.K_RIGHT] and direction != [-BLOCK_SIZE, 0]:
            direction = [BLOCK_SIZE, 0]
        if keys[pygame.K_UP] and direction != [0, BLOCK_SIZE]:
            direction = [0, -BLOCK_SIZE]
        if keys[pygame.K_DOWN] and direction != [0, -BLOCK_SIZE]:
            direction = [0, BLOCK_SIZE]

        new_head = [
            (snake[0][0] + direction[0]) % WIDTH,
            (snake[0][1] + direction[1]) % HEIGHT
        ]
        snake.insert(0, new_head)

        if new_head in snake[1:]:
            game_over = True
            break

        if abs(new_head[0] - food[0]) < BLOCK_SIZE and abs(new_head[1] - food[1]) < BLOCK_SIZE:
            score += 1
            food = random_food()
            if score % 5 == 0 and level < len(SOIL_LEVELS) - 1:
                level += 1
            elif score == 31:
                time.sleep(1)
                exit()
        else:
            snake.pop()

        win.fill(SOIL_LEVELS[level]["bg"])
        draw_soil_patches(level)
        draw_worm_block(SOIL_LEVELS[level]["food_color"], food)
        for block in snake:
            draw_worm_block(BLACK, block)

        draw_label_with_border(f"Soil: {SOIL_LEVELS[level]['name']}", (10, 10), BLACK, SOIL_LEVELS[level]["bg"])
        draw_label_with_border(f"Mineral: {SOIL_LEVELS[level]['mineral']}", (10, 50), BLACK, SOIL_LEVELS[level]["bg"])

        win.blit(font.render(f"Score: {score}", True, BLACK), (10, 90))
        win.blit(small_font.render(SOIL_LEVELS[level]["fact"], True, BLACK), (10, HEIGHT - 30))

        pygame.display.update()

    while game_over:
        win.fill(WHITE)
        show_message("Game Over!", HEIGHT // 2 - 40, RED, 50)
        show_message(f"Final Score: {score}", HEIGHT // 2, BLACK, 35)
        show_message("Press R to Restart", HEIGHT // 2 + 60, BLACK, 25)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            start_screen()
            game_loop()

# Run the Game
start_screen()
game_loop()
