#!/usr/bin/env python3


from enum import Enum
from line import Line
from triangle import Triangle
from orbit import Orbit
from planet import Planet
from vars import window_res, pixels, Colors
import pygame
import sys
import math
import numpy as np
import argparse
from PIL import ImageColor, Image
import imageio
from numba import njit
from numba.typed import List
import vars


colors = [ImageColor.getcolor(h, "RGB") for h in [Colors.BG, Colors.red, Colors.green, Colors.yellow, Colors.blue, Colors.purple, Colors.aqua, Colors.orange, Colors.gray, Colors.grayl, Colors.redl, Colors.greenl, Colors.yellowl, Colors.bluel, Colors.purplel, Colors.aqual, Colors.orangel, Colors.FG]]
pix = [[colors[0] for _ in range(window_res[0])] for _ in range(window_res[1])]

def drawGrid(SCREEN):
    # looping through grid
    for x in range(window_res[0]):
        for y in range(1, window_res[1] - 1):
            # checking value of pixel
            if pixels[x][window_res[1] - y] == 1:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.red)
                pygame.draw.rect(SCREEN, color, rect)
            if pixels[x][window_res[1] - y] == 2:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.green)
                pygame.draw.rect(SCREEN, color, rect)
            if pixels[x][window_res[1] - y] == 3:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.blue)
                pygame.draw.rect(SCREEN, color, rect)
            if pixels[x][window_res[1] - y] == 4:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.orange)
                pygame.draw.rect(SCREEN, color, rect)
            if pixels[x][window_res[1] - y] == 5:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.aqua)
                pygame.draw.rect(SCREEN, color, rect)
            if pixels[x][window_res[1] - y] == 99:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.BG)
                pygame.draw.rect(SCREEN, color, rect)
                pixels[x][window_res[1] - y] = 0

def export(n):
    print(n)
    if n < 9180: return
    name = "pix/" + "0" * (5 - len(str(n))) + str(n) + ".png"
    for x in range(window_res[0]):
        for y in range(1, window_res[1] - 1):
            if pixels[x][window_res[1] - y] == 99:
                pixels[x][window_res[1] - y] = 0
            if pixels[x][window_res[1] - y] != 99:
                pix[window_res[1] - y][x] = colors[pixels[x][window_res[1] - y]]
    Image.fromarray(np.array(pix, dtype=np.uint8)).save(name)



def sphere(pos, rad, color):
    # looping through region of circle
    for x in range(pos[0] - rad, pos[0] + rad):
        for y in range(pos[1] - rad, pos[1] + rad):
            # checking if position is in circle
            if (x - pos[0])**2 + (y - pos[1])**2 <= rad**2:
                #print(x, y)
                pixels[x][y] = color


@njit(parallel=True)
def genpix(tpix, tpixels, twindow_res, tcolors):
    return tpix, tpixels

if __name__ == "__main__":
    n = 0
    parser = argparse.ArgumentParser(description='Calculate orbits.')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-v', action='store_true')
    parser.add_argument('--display', action='store_true')
    args, leftovers = parser.parse_known_args()

    pix_orb0 = Orbit([300, 510], 400, -0.75, args.d, args.v, 30,
                     Planet(500, [], 10, [[50, -0.5, args.d, args.v, -90, Planet(100, [], 3, visual=args.v, color=3)],
                                          [60, -0.7, args.d, args.v, 30, Planet(70, [], 3, visual=args.v, color=4)]], color=5
                            ))

    sphere([300, 510], 25, 3)
    if args.v:
        pix_orb0.draw()
        for p in pix_orb0.points:
            pixels[p[0]][p[1]] = 1
    pix_orb0.motion()

    """pix_orb1 = Orbit([600, 384], 200, -0.75, args.d, args.v, -45, [Planet(500, [], 10)])
    if args.v:
        pix_orb1.draw()
    for p in pix_orb1.points:
        pixels[p[0]][p[1]] = 1
    pix_orb1.motion()
    """


    if args.display:
        pygame.init()
        SCREEN = pygame.display.set_mode((window_res[0], window_res[1]))
        SCREEN.fill(Colors.BG)
    while True:
        export(n)
        n += 1
        pix_orb0.motion()
        # pix_orb1.motion()
        if args.display:
            click = pygame.mouse.get_pressed()[0]
            if click:
                xm,ym = pygame.mouse.get_pos()
                if args.d:
                    print(xm, ym)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            drawGrid(SCREEN)
            pygame.display.update()
