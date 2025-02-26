import pygame
import math
from consts import *
import rendering


pygame.init()


def toggle_tile(grid, x, y):
    grid[y][x] = "X" if grid[y][x] == "O" else "O"


def is_wall(x, y):
    grid_x, grid_y = int(x // TILE_SIZE), int(y // TILE_SIZE)
    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        return MAP[grid_y][grid_x] == "X"
    return True


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

grid = [["O" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 50, 100, 40)

selecting = True
while selecting:
    screen.fill(BLACK)
    rendering.draw_grid(screen, grid)
    pygame.draw.rect(screen, RED, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render("start", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 25, HEIGHT - 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if button_rect.collidepoint(mx, my):
                selecting = False
            else:
                grid_x, grid_y = mx // TILE_SIZE, my // TILE_SIZE
                if grid_x < GRID_SIZE and grid_y < GRID_SIZE:
                    toggle_tile(grid, grid_x, grid_y)

    pygame.display.flip()
    clock.tick(30)

MAP = ["".join(row) for row in grid]

player_x, player_y = TILE_SIZE, TILE_SIZE
player_angle = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

while running:
    screen.fill(BLACK)
    pygame.draw.rect(screen, DARK_GRAY, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    keys = pygame.key.get_pressed()

    dx, dy = 0, 0
    speed = 3
    diag_speed = speed / math.sqrt(2)

    moving_x = keys[pygame.K_w] or keys[pygame.K_s]
    moving_y = keys[pygame.K_a] or keys[pygame.K_d]

    if moving_x and moving_y:
        speed = diag_speed

    if keys[pygame.K_w]:
        dx += math.cos(player_angle) * speed
        dy += math.sin(player_angle) * speed

    if keys[pygame.K_s]:
        dx -= math.cos(player_angle) * speed
        dy -= math.sin(player_angle) * speed

    if keys[pygame.K_a]:
        dx += math.cos(player_angle - math.pi / 2) * speed
        dy += math.sin(player_angle - math.pi / 2) * speed

    if keys[pygame.K_d]:
        dx += math.cos(player_angle + math.pi / 2) * speed
        dy += math.sin(player_angle + math.pi / 2) * speed

    if not is_wall(player_x + dx, player_y):
        player_x += dx

    if not is_wall(player_x, player_y + dy):
        player_y += dy

    if keys[pygame.K_LEFT]:
        player_angle -= math.radians(5)

    if keys[pygame.K_RIGHT]:
        player_angle += math.radians(5)

    start_angle = player_angle - FOV / 2

    for ray in range(NUM_RAYS):
        angle = start_angle + (ray / NUM_RAYS) * FOV

        for depth in range(1, MAX_DEPTH * TILE_SIZE):
            target_x = player_x + math.cos(angle) * depth
            target_y = player_y + math.sin(angle) * depth

            if is_wall(target_x, target_y):
                corrected_depth = depth * math.cos(angle - player_angle)
                wall_height = HEIGHT / (corrected_depth / TILE_SIZE + 1)

                brightness = 255 - min(200, int(corrected_depth * 4))
                color = (brightness, brightness, brightness)

                pygame.draw.rect(
                    screen,
                    color,
                    (
                        ray * (WIDTH // NUM_RAYS),
                        HEIGHT // 2 - wall_height // 2,
                        WIDTH // NUM_RAYS,
                        wall_height,
                    ),
                )
                break

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)
pygame.quit()
