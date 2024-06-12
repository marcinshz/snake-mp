import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Definicje kolorów
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Wymiary okna gry
DIS_WIDTH = 800
DIS_HEIGHT = 600

# Inicjalizacja okna gry
dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake Game for Two Players')

# Zegar Pygame
clock = pygame.time.Clock()

# Parametry węża
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# Czcionka
font_style = pygame.font.SysFont(None, 50)


def message(msg, color, x, y):
    """Wyświetla wiadomość na ekranie"""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [x, y])


def draw_snake(snake_block, snake_list, color):
    """Rysuje węża na ekranie"""
    for segment in snake_list:
        pygame.draw.rect(dis, color, [segment[0], segment[1], snake_block, snake_block])


def game_over_screen():
    """Ekran końca gry"""
    message("Press C to restart", RED, DIS_WIDTH / 8, DIS_HEIGHT / 6)
    pygame.display.update()


def generate_food():
    """Generuje jedzenie w losowym miejscu na ekranie"""
    food_x = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
    return food_x, food_y


def handle_events(x1_change, y1_change, x2_change, y2_change):
    """Obsługuje zdarzenia gry"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True, x1_change, y1_change, x2_change, y2_change
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -SNAKE_BLOCK
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = SNAKE_BLOCK
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -SNAKE_BLOCK
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = SNAKE_BLOCK
                x1_change = 0
            elif event.key == pygame.K_a:
                x2_change = -SNAKE_BLOCK
                y2_change = 0
            elif event.key == pygame.K_d:
                x2_change = SNAKE_BLOCK
                y2_change = 0
            elif event.key == pygame.K_w:
                y2_change = -SNAKE_BLOCK
                x2_change = 0
            elif event.key == pygame.K_s:
                y2_change = SNAKE_BLOCK
                x2_change = 0
    return False, x1_change, y1_change, x2_change, y2_change


def check_collision(x, y, snake_list):
    """Sprawdza, czy wąż uderzył w siebie lub w innego węża"""
    if x >= DIS_WIDTH or x < 0 or y >= DIS_HEIGHT or y < 0:
        return True
    for segment in snake_list[:-1]:
        if segment == [x, y]:
            return True
    return False


def update_snake_position(x, y, x_change, y_change, snake_list, snake_length):
    """Aktualizuje pozycję węża"""
    x += x_change
    y += y_change
    snake_head = [x, y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]
    return x, y


def check_food_collision(x, y, foodx, foody):
    """Sprawdza, czy wąż zjadł jedzenie"""
    if x == foodx and y == foody:
        return True
    return False


def gameLoop():
    game_over = False
    game_close = False

    # Pozycje początkowe węży
    x1, y1 = DIS_WIDTH / 4, DIS_HEIGHT / 2
    x2, y2 = (DIS_WIDTH / 4) * 3, DIS_HEIGHT / 2

    # Zmiana położenia węży
    x1_change, y1_change = 0, 0
    x2_change, y2_change = 0, 0

    # Listy segmentów węży i ich długości
    snake_list1, snake_length1 = [], 1
    snake_list2, snake_length2 = [], 1

    # Pozycje jedzenia
    foodx1, foody1 = generate_food()
    foodx2, foody2 = generate_food()

    while not game_over:

        while game_close:
            game_over_screen()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        game_over, x1_change, y1_change, x2_change, y2_change = handle_events(x1_change, y1_change, x2_change,
                                                                              y2_change)

        if check_collision(x1, y1, snake_list1) or check_collision(x2, y2, snake_list2):
            game_close = True

        x1, y1 = update_snake_position(x1, y1, x1_change, y1_change, snake_list1, snake_length1)
        x2, y2 = update_snake_position(x2, y2, x2_change, y2_change, snake_list2, snake_length2)

        dis.fill(BLACK)
        pygame.draw.rect(dis, GREEN, [foodx1, foody1, SNAKE_BLOCK, SNAKE_BLOCK])
        pygame.draw.rect(dis, GREEN, [foodx2, foody2, SNAKE_BLOCK, SNAKE_BLOCK])

        # Sprawdzenie kolizji węży ze sobą nawzajem
        if any(segment == [x1, y1] for segment in snake_list2):
            game_close = True
        if any(segment == [x2, y2] for segment in snake_list1):
            game_close = True

        draw_snake(SNAKE_BLOCK, snake_list1, BLUE)
        draw_snake(SNAKE_BLOCK, snake_list2, RED)

        pygame.display.update()

        # Sprawdzenie kolizji z jedzeniem
        if check_food_collision(x1, y1, foodx1, foody1) or check_food_collision(x1, y1, foodx2, foody2):
            if check_food_collision(x1, y1, foodx1, foody1):
                foodx1, foody1 = generate_food()
            else:
                foodx2, foody2 = generate_food()
            snake_length1 += 1

        if check_food_collision(x2, y2, foodx1, foody1) or check_food_collision(x2, y2, foodx2, foody2):
            if check_food_collision(x2, y2, foodx1, foody1):
                foodx1, foody1 = generate_food()
            else:
                foodx2, foody2 = generate_food()
            snake_length2 += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()


gameLoop()
