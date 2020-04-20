import pygame
from random import choice
import math
import sys
from ai import pathfinding
from mapgen.mapgen import Map, MapGenPerlin

map_choices = [".", "#", ","]
wall_choices = ["#"]
font_size = 16
font_padding = 2
font_with_padding = font_size + font_padding


def random_map():
    #TODO: make into a map class
    lines = []
    current_line = []
    for i in range(10):
        for j in range(10):
            current_line.append(choice(map_choices))
        lines.append(current_line)
        current_line = []
    return lines

def main(args):
    test_astar = "pathfinding" in args
    test_noise = "noise" in args
    cursor_x, cursor_y = 0, 0
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Goblins")

    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Consolas", 16)

    test_map = None
    game_map = None
    blit_map = None
    if test_noise:
        test_map = Map(20, 20, MapGenPerlin, font, map_choices)
        game_map = test_map.get_symbol_map()
        blit_map = test_map.get_symbol_blit_map()
    else:
        game_map = random_map()
        blit_map = [[font.render(i, True, [255, 255, 255]) for i in line] for line in game_map]

    running = True
    first = True
    flip = False
    curr_time = 0
    while running:
        if first:
            if test_map is not None:
                test_map.draw_noise()
            if test_astar:
                test_map = pathfinding.MapPathfinding.test_pathfinding_map()
                mp = pathfinding.MapPathfinding(game_map)
                start, end = None, None
                for y, line in enumerate(game_map):
                    for x, c in enumerate(line):
                        if c != "#":
                            start = (x, y)
                            break
                    if start != None:
                        break
                            
                for y, line in enumerate(game_map[::-1]):
                    for x, c in enumerate(line[::-1]):
                        if c != "#":
                            end = (19 - x, 19 - y)
                            break
                    if end != None:
                        break

                path = mp.pathfind_from_a_to_b(start, end)
                test_blit_map = [[font.render(i, True, [255, 255, 255]) for i in line] for line in test_map]
                while path != None:
                    pygame.draw.rect(screen, [0, 255, 0], (path.x * font_with_padding + 4, path.y * font_with_padding, 16, 16))
                    path = path.prev
                x, y = 8, 0
                for i, line in enumerate(blit_map):
                    for j, c in enumerate(line):
                        screen.blit(c, (x, y))
                        x += font_with_padding
                    x = 8
                    y += font_with_padding
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
            else:
                pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                x, y = 8, 0
                for line in blit_map:
                    for c in line:
                        screen.blit(c, (x, y))
                        x += font_with_padding
                    x = 8
                    y += font_with_padding
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
        else:
            if not test_astar:
                if flip:
                    if pygame.time.get_ticks() - curr_time > 500:
                        pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                        screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                        flip = not flip
                        pygame.display.flip()
                        curr_time = pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks() - curr_time > 500:
                        pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                        screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                        flip = not flip
                        pygame.display.flip()
                        curr_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if not test_astar:
                    drawMade = False
                    if event.key == pygame.K_LEFT:
                        if cursor_x - 1 >= 0:
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_x -= 1
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True
                    elif event.key == pygame.K_RIGHT:
                        if cursor_x + 1 < len(blit_map[0]):
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_x += 1
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True
                    if event.key == pygame.K_UP:
                        if cursor_y - 1 >= 0:
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_y -= 1
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True
                    elif event.key == pygame.K_DOWN:
                        if cursor_y + 1 < len(blit_map):
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_y += 1
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True

                    if drawMade:
                        pygame.display.flip()
        first = False

if __name__ == "__main__":
    main([i.lower() for i in sys.argv[1:]])