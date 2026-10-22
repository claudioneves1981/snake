import pygame
import random
import math

pygame.init()

WIDTH = 900
HEIGHT = 700
CELL = 20

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake AI Visualizer")

clock = pygame.time.Clock()

BLACK = (8,8,12)
GRID = (18,18,25)
GREEN =(0,255,120)
HEAD = (120,255,180)
RED = (255,70,70)
WHITE = (240, 240, 240)

COLS = WIDTH // CELL
ROWS = HEIGHT // CELL

font = pygame.font.SysFont("consolas",24, True)

snake = [
    [10,10],
    [9,10],
    [8,10],
    [7,10]
]

direction = (0,0)

score = 0

food = [
    random.randint(2, COLS - 3),
    random.randint(2, ROWS - 3)
]

def spawn_food():
    global food

    while True:

        x = random.randint(2,COLS - 3)
        y = random.randint(2,ROWS - 3)

        if [x, y] not in snake:

            food = [x, y]
            return

def draw_grid():
    for y in range(0, WIDTH, CELL):
        pygame.draw.line(

            screen,

            GRID,

            (0,y),

            (WIDTH, y)
        )

def draw_food():
    pygame.draw.circle(

        screen,

        RED,

        (

            food[0] * CELL + CELL // 2,
            food[1] * CELL + CELL // 2
        ),

        CELL // 2 - 2
    )

def draw_snake():
    
    for i, part in enumerate(snake):
        
        color = HEAD if i == 0 else GREEN

        pygame.draw.rect(

            screen,

            color,

            (

                part[0] * CELL + 2,

                part[1] * CELL + 2,

                CELL - 4,

                CELL - 4
            ),

            border_radius=5

        )

def move_ai():
    global direction

    hx, hy = snake[0]
    fx, fy = food

    options = []

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != (0, 1):
        options.append((0,-1))
        direction = (0, -1)
    elif keys[pygame.K_DOWN] and direction != (0, -1):
        options.append((0, 1))
        direction = (0, 1)
    elif keys[pygame.K_LEFT] and direction != (1, 0):
        options.append((-1, 0))
        direction = (-1, 0)
    elif keys[pygame.K_RIGHT] and direction!= (-1, 0):
       options.append((1, 0))  
       direction = (1, 0)     

    options.extend([
        (0,-1),
        (0,1),
        (-1,0),
        (1,0)
    ])

    for dx, dy in options:
        nx = hx + dx
        ny = hy + dy

        if nx < 0 or nx >= COLS:
            continue
        if ny < 0 or ny >= ROWS:
            continue
        if [nx, ny] in snake[:-1]:
            continue

        direction = (dx, dy)
        return

running = True

while running:

    clock.tick(12)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    move_ai()

    hx, hy = snake[0]
    dx, dy = direction


    #if direction != (0,0):

    new_head = [hx + dx, hy + dy]

    if (
            new_head[0] < 0 or
            new_head[0] >= COLS or
            new_head[1] < 0 or
            new_head[1] >= ROWS or
            new_head in snake[:-1]
        ):
            snake[:] = [
                [10, 10],
                [9, 10],
                [8, 10],
                [7,10]
            ]
            direction = (0, 0)
            score = 0
            spawn_food()
            continue

    snake.insert(0,new_head)

    if new_head == food:
            score += 1
            spawn_food()
    else:
            snake.pop()

    screen.fill(BLACK)
    draw_grid()
    draw_food()
    draw_snake()
    glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for part in snake:

        pygame.draw.circle(
            glow,
            (0,255,120,35),
                (
                    part[0] * CELL + CELL // 2,
                    part[1] * CELL + CELL // 2
                ),
                CELL
            )
    pygame.draw.circle(
        glow,
        (255,70,70,50),
            (
                food[0] * CELL + CELL // 2,
                food[1] * CELL + CELL // 2
            ),
            CELL
        )

    screen.blit(glow, (0,0))

    score_text = font.render(
            f"Score : {score}",
            True,
            WHITE
        )

    screen.blit(score_text,(15,15))

    ai_text = font.render(
            "AI MODE",
            True,
            GREEN
        )

    screen.blit(
            ai_text,
            (WIDTH - ai_text.get_width() - 15, 15)
        )

    fps_text = font.render(
            f"FPS : {int(clock.get_fps())}",
            True,
            WHITE
        )

    screen.blit(
            fps_text,
            (15,50)
        )

    pygame.display.flip()

pygame.quit()