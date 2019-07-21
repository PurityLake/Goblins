import pygame
from random import choice
import math
import sys
from ai import pathfinding
from mapgen.mapgen import MapGenPerlin
import numpy as np

map_choices = [".", "#", "g", ",", "a"]
wall_choices = ["#"]

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

    game_map = random_map()
    blit_map = [[font.render(i, True, [255, 255, 255]) for i in line] for line in game_map]

    running = True
    first = True
    flip = False
    curr_time = 0
    while running:
        if first:
            if test_noise:
                mgp = MapGenPerlin(30, 30, 100)
                m = max(max(line) for line in mgp.noise)
                letters = []
                for l in mgp.noise:
                    line = []
                    for pix in l:
                        val = pix % 255 / 255
                        if val > 0.7:
                            line.append("^")
                        else:
                            line.append(".")
                    letters.append(line)
                letters = [[font.render(i, True, [255, 255, 255]) for i in line] for line in letters]
                x, y = 8, 0
                for line in letters:
                    for letter in line:
                        screen.blit(letter, (x, y))
                        x += 18
                    x = 8
                    y += 18
                #noise = []
                #for i in mgp.noise:
                #    line = []
                #    for j in i:
                #        val = j % 255
                #        line.append((val, val, val))
                #    noise.append(line)
                #surface = pygame.surfarray.make_surface(np.array(noise))
                #screen.blit(surface, (0, 0))
                pygame.display.flip()
            elif test_astar:
                test_map = pathfinding.MapPathfinding.test_pathfinding_map()
                mp = pathfinding.MapPathfinding(test_map)
                path = mp.pathfind_from_a_to_b((9, 3), (0, 0))
                test_blit_map = [[font.render(i, True, [255, 255, 255]) for i in line] for line in test_map]
                while path != None:
                    pygame.draw.rect(screen, [0, 255, 0], (path.x * 18 + 4, path.y * 18, 16, 16))
                    path = path.prev
                x, y = 8, 0
                for i, line in enumerate(test_blit_map):
                    for j, c in enumerate(line):
                        screen.blit(c, (x, y))
                        x += 18
                    x = 8
                    y += 18
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
            else:
                pygame.draw.rect(screen, [0, 255, 0], (cursor_x * 18 + 4, cursor_y * 18, 16, 16))
                x, y = 8, 0
                for line in blit_map:
                    for c in line:
                        screen.blit(c, (x, y))
                        x += 18 + 8
                    x = 8
                    y += 18
                pygame.display.flip()
                curr_time = pygame.time.get_ticks()
        else:
            if not test_astar and not test_noise:
                if flip:
                    if pygame.time.get_ticks() - curr_time > 500:
                        pygame.draw.rect(screen, [0, 0, 0], (cursor_x * 18 + 4, cursor_y * 18, 16, 16))
                        screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * 18 + 9, cursor_y * 18))
                        flip = not flip
                        pygame.display.flip()
                        curr_time = pygame.time.get_ticks()
                else:
                    if pygame.time.get_ticks() - curr_time > 500:
                        pygame.draw.rect(screen, [0, 255, 0], (cursor_x * 18 + 4, cursor_y * 18, 16, 16))
                        screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * 18 + 9, cursor_y * 18))
                        flip = not flip
                        pygame.display.flip()
                        curr_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if not test_astar:
                    if event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_RIGHT:
                        if cursor_x + 1 < len(blit_map[0]):
                            pygame.draw.rect(screen, [0, 0, 0], (cursor_x * 18 + 4, cursor_y * 18, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * 18 + 9, cursor_y * 18))
                            cursor_x += 1
                            pygame.draw.rect(screen, [0, 255, 0], (cursor_x * 18 + 4, cursor_y * 18, 16, 16))
                            screen.blit(blit_map[cursor_y][cursor_x], (cursor_x * 18 + 9, cursor_y * 18))
                            flip = True
                            curr_time = pygame.time.get_ticks()
                            pygame.display.flip()
                    elif event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_LEFT:
                        pass
        first = False

if __name__ == "__main__":
    main([i.lower() for i in sys.argv[1:]])