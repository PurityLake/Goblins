import pygame
from random import choice
import math
import sys
from ai import pathfinding
from mapgen.mapgen import Map, MapGenPerlin

map_choices = ["."]
wall_choices = ["#"]
font_size = 16
font_padding = 2
font_with_padding = font_size + font_padding
max_floors = 3


def main(args):
    curr_floor = 0
    test_astar = "pathfinding" in args
    cursor_x, cursor_y = 0, 0
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Goblins")

    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("Consolas", 16)

    floors = [
        Map(20, 20, MapGenPerlin, font, map_choices),
        Map(20, 20, MapGenPerlin, font, map_choices),
        Map(20, 20, MapGenPerlin, font, map_choices)
    ]
    
    map3d = []
    map3d_blit = []
    lower_floor = None
    for f in floors:
        if lower_floor == None:
            map3d.append(f.get_symbol_map())
            map3d_blit.append(f.get_symbol_blit_map())
            lower_floor = 0
        else:
            new_floor = f.get_symbol_map()
            new_floor_blit = f.get_symbol_blit_map()
            for i, line in enumerate(new_floor):
                for j, ch in enumerate(line):
                    each_floor = [map3d[idx][i][j] != None for idx in range(0, lower_floor + 1)]
                    if any(each_floor):
                        new_floor[i][j] = None
                        new_floor_blit[i][j] = None
            map3d.append(new_floor)
            map3d_blit.append(new_floor_blit)
            lower_floor += 1

    test_map = Map(20, 20, MapGenPerlin, font, map_choices)
    game_map = map3d[curr_floor]
    blit_map = map3d_blit[curr_floor]

    running = True
    dirty = False
    first = True
    flip = False
    curr_time = 0
    while running:
        if first:
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
                        if c != None:
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
                        if c != None:
                            screen.blit(c, (x, y))
                        x += font_with_padding
                    x = 8
                    y += font_with_padding
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
        else:
            if not test_astar:
                if dirty:
                    screen.fill((0,0,0))
                    x, y = 8, 0
                    for line in blit_map:
                        for c in line:
                            if c != None:
                                screen.blit(c, (x, y))
                            x += font_with_padding
                        x = 8
                        y += font_with_padding
                    curr_time = pygame.time.get_ticks()
                    dirty = False
                if flip:
                    if pygame.time.get_ticks() - curr_time > 500:
                        pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                        tile = blit_map[cursor_y][cursor_x]
                        if tile != None:
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                        flip = not flip
                        pygame.display.flip()
                        curr_time = pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks() - curr_time > 500:
                        pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                        tile = blit_map[cursor_y][cursor_x]
                        if tile != None:
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
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_x -= 1
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True
                    elif event.key == pygame.K_RIGHT:
                        if cursor_x + 1 < len(blit_map[0]):
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_x += 1
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True
                    if event.key == pygame.K_UP:
                        if cursor_y - 1 >= 0:
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_y -= 1
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True
                    elif event.key == pygame.K_DOWN:
                        if cursor_y + 1 < len(blit_map):
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            cursor_y += 1
                            tile = blit_map[cursor_y][cursor_x]
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * font_with_padding + 4, cursor_y * font_with_padding, 16, 16))
                            if tile != None:
                                screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * font_with_padding + 9, cursor_y * font_with_padding))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            drawMade = True

                    if event.key == pygame.K_w:
                        if curr_floor + 1 < max_floors:
                            curr_floor += 1
                            game_map = map3d[curr_floor]
                            blit_map = map3d_blit[curr_floor]
                            dirty = True
                    elif event.key == pygame.K_s:
                        if curr_floor - 1 >= 0:
                            curr_floor -= 1
                            game_map = map3d[curr_floor]
                            blit_map = map3d_blit[curr_floor]
                            dirty = True

                    if drawMade:
                        pygame.display.flip()
        first = False

if __name__ == "__main__":
    main([i.lower() for i in sys.argv[1:]])