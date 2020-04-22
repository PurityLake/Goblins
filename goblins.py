import pygame
from random import choice, seed
import math
import sys
from ai import pathfinding
from mapgen.mapgen import Map, MapGenPerlin
import time

map_choices = [".", ".", ".", "#"]
wall_choices = ["#"]
font_size = 16
font_padding = 2
font_with_padding = font_size
max_floors = 3
map_width, map_height = 30, 30

def move_cursor(screen, game_map, cursor_x, cursor_y, width, height, dx=0, dy=0):
    pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding, cursor_y * font_with_padding, width, height))
    game_map[cursor_y][cursor_x].draw(screen, cursor_x * font_with_padding + 8, cursor_y * font_with_padding)
    cursor_x += dx
    cursor_y += dy
    pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding, cursor_y * font_with_padding, width, height))
    game_map[cursor_y][cursor_x].draw(screen, cursor_x * font_with_padding + 8, cursor_y * font_with_padding, drawbg=False)
    curr_time = pygame.time.get_ticks()
    return cursor_x, cursor_y

def main(args):
    seed(4)
    curr_floor = 0
    test_astar = "pathfinding" in args
    cursor_x, cursor_y = 0, 0
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Goblins")

    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Consolas", 16)

    floors = [
        Map(map_width, map_height, MapGenPerlin, font, font_size, map_choices),
        Map(map_width, map_height, MapGenPerlin, font, font_size, map_choices),
        Map(map_width, map_height, MapGenPerlin, font, font_size, map_choices)
    ]
    
    map3d = []
    lower_floor = None
    for f in floors:
        if lower_floor == None:
            map3d.append(f.get_symbol_map())
            lower_floor = 0
        else:
            new_floor = f.get_symbol_map()
            for i, line in enumerate(new_floor):
                for j, ch in enumerate(line):
                    each_floor = [not map3d[idx][i][j].is_none() for idx in range(0, lower_floor + 1)]
                    if any(each_floor):
                        new_floor[i][j].set_ch(" ")
                        new_floor[i][j].set_surf(None)
                    elif new_floor[i][j].is_none():
                        new_floor[i][j].set_ch('.')
                        new_floor[i][j].set_surf(font.render('.', True, [255, 255, 255]))
            map3d.append(new_floor)
            lower_floor += 1

    game_map = map3d[curr_floor]

    mp = None
    path = None
    if test_astar:
        mp = pathfinding.MapPathfinding(map3d, map_width, map_height, 3)
        start, end = None, None
        for y, line in enumerate(game_map):
            for x, node in enumerate(line):
                if node.ch != "#" and not node.is_none():
                    start = (x, y, 0)
                    break
            if start != None:
                break     
        for y, line in enumerate(game_map[::-1]):
            for x, node in enumerate(line[::-1]):
                if node.ch != "#" and not node.is_none():
                    end = (map_width - 1 - x, map_height - 1 - y, 0)
                    break
            if end != None:
                break
        path = mp.pathfind_from_a_to_b(start, end)
        print(path)

    running = True
    dirty = True
    flip = False
    curr_time = 0
    while running:
        if dirty:
            screen.fill((0,0,0))
            if test_astar:
                temppath = path
                while temppath != None:
                    if temppath.z != curr_floor:
                        pygame.draw.rect(screen, [255, 0, 0], (temppath.x * font_with_padding, temppath.y * font_with_padding, 16, 16))
                    else:
                        pygame.draw.rect(screen, [0, 255, 0], (temppath.x * font_with_padding, temppath.y * font_with_padding, 16, 16))
                    temppath = temppath.prev
            x, y = 8, 0
            for line in game_map:
                for node in line:
                    node.draw(screen, x, y, drawbg=not test_astar)
                    x += font_with_padding
                x = 8
                y += font_with_padding
            curr_time = pygame.time.get_ticks()
            dirty = False
        if flip:
            if pygame.time.get_ticks() - curr_time > 500:
                pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding, cursor_y * font_with_padding, 16, 16))
                game_map[cursor_y][cursor_x].draw(screen, cursor_x * font_with_padding + 8, cursor_y * font_with_padding)
                flip = not flip
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() - curr_time > 500:
                pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding, cursor_y * font_with_padding, 16, 16))
                game_map[cursor_y][cursor_x].draw(screen, cursor_x * font_with_padding + 8, cursor_y * font_with_padding, drawbg=False)
                flip = not flip
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                drawMade = False
                if event.key == pygame.K_LEFT:
                    if cursor_x - 1 >= 0:
                        cursor_x, cursor_y = move_cursor(screen, game_map, cursor_x, cursor_y, font_size, font_size, dx=-1)
                        curr_time = pygame.time.get_ticks()
                        drawMade = True
                        flip = True
                elif event.key == pygame.K_RIGHT:
                    if cursor_x + 1 < map_width:
                        cursor_x, cursor_y = move_cursor(screen, game_map, cursor_x, cursor_y, font_size, font_size, dx=1)
                        curr_time = pygame.time.get_ticks()
                        drawMade = True
                        flip = True
                if event.key == pygame.K_UP:
                    if cursor_y - 1 >= 0:
                        cursor_x, cursor_y = move_cursor(screen, game_map, cursor_x, cursor_y, font_size, font_size, dy=-1)
                        curr_time = pygame.time.get_ticks()
                        drawMade = True
                        flip = True
                elif event.key == pygame.K_DOWN:
                    if cursor_y + 1 < map_height:
                        cursor_x, cursor_y = move_cursor(screen, game_map, cursor_x, cursor_y, font_size, font_size, dy=1)
                        curr_time = pygame.time.get_ticks()
                        drawMade = True
                        flip = True
                if event.key == pygame.K_w:
                    if curr_floor + 1 < max_floors:
                        curr_floor += 1
                        game_map = map3d[curr_floor]
                        dirty = True
                elif event.key == pygame.K_s:
                    if curr_floor - 1 >= 0:
                        curr_floor -= 1
                        game_map = map3d[curr_floor]
                        dirty = True

                if drawMade:
                    pygame.display.flip()
        first = False

if __name__ == "__main__":
    main([i.lower() for i in sys.argv[1:]])