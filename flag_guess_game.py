import random
import time
import pygame
import importlib

# Load flag data from emoji-flags package
flags_module = importlib.import_module('emoji-flags.data')
FLAGS = flags_module.flags

# Initialize pygame
pygame.init()
FONT_FLAG = pygame.font.Font(None, 200)  # large font for flag emoji
FONT_OPTION = pygame.font.Font(None, 36)
FONT_INFO = pygame.font.Font(None, 28)

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guess the Flag")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

score = 0
start_time = time.time()
TIME_LIMIT = 60  # seconds

clock = pygame.time.Clock()

# Prepare a list of (emoji, country name)
flag_pool = [(f['emoji'], f['name']) for f in FLAGS]

current_choices = []
current_flag = None

def new_round():
    global current_choices, current_flag
    current_flag = random.choice(flag_pool)
    options = {current_flag[1]}
    while len(options) < 3:
        options.add(random.choice(flag_pool)[1])
    options = list(options)
    random.shuffle(options)
    current_choices = options

new_round()

running = True
while running:
    SCREEN.fill(WHITE)
    elapsed = time.time() - start_time

    if elapsed >= TIME_LIMIT:
        running = False
        continue

    # Draw timer and score
    timer_text = FONT_INFO.render(f"Time: {TIME_LIMIT-int(elapsed)}", True, BLACK)
    SCREEN.blit(timer_text, (10, 10))
    score_text = FONT_INFO.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (WIDTH - 120, 10))

    # Draw flag
    flag_surface = FONT_FLAG.render(current_flag[0], True, BLACK)
    flag_rect = flag_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
    SCREEN.blit(flag_surface, flag_rect)

    # Draw options as buttons
    button_rects = []
    for i, option in enumerate(current_choices):
        rect = pygame.Rect(0, 0, 250, 50)
        rect.center = (WIDTH//2, HEIGHT//2 + i*70)
        button_rects.append(rect)
        pygame.draw.rect(SCREEN, GRAY, rect)
        label = FONT_OPTION.render(option, True, BLACK)
        label_rect = label.get_rect(center=rect.center)
        SCREEN.blit(label, label_rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for rect, option in zip(button_rects, current_choices):
                if rect.collidepoint(pos):
                    if option == current_flag[1]:
                        score += 1
                    new_round()
                    break

    clock.tick(30)

# Game over screen
SCREEN.fill(WHITE)
end_text = FONT_OPTION.render(f"Time's up! Your score: {score}", True, BLACK)
end_rect = end_text.get_rect(center=(WIDTH//2, HEIGHT//2))
SCREEN.blit(end_text, end_rect)
pygame.display.flip()

# Wait a few seconds before quitting
pygame.time.wait(5000)
pygame.quit()
