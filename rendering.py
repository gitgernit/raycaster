import pygame
from consts import *


def draw_grid(screen, grid):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = GRAY if grid[y][x] == "X" else WHITE
            pygame.draw.rect(
                screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )
            pygame.draw.rect(
                screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1
            )
