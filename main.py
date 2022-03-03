#!/usr/bin/env python3

from enum import Enum
from line import Line
from triangle import Triangle
from orbit import Orbit
from vars import *
import pygame
import sys
import math
import numpy as np
import argparse



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
            if pixels[x][window_res[1] - y] == 99:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.BG)
                pygame.draw.rect(SCREEN, color, rect)
                pixels[x][window_res[1] - y] = 0


def sphere(pos, rad):
    # looping through region of circle
    for x in range(pos[0] - rad, pos[0] + rad):
        for y in range(pos[1] - rad, pos[1] + rad):
            # checking if position is in circle
            if (x - pos[0])**2 + (y - pos[1])**2 <= rad**2:
                #print(x, y)
                pixels[x][y] = 1



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate orbits.')
    parser.add_argument('-d', action='store_true')
    parser.add_argument('-v', action='store_true')
    args, leftovers = parser.parse_known_args()

    pix_orb0 = Orbit([600, 384], 200, -0.75, args.d, args.v)
    if args.v:
        pix_orb0.draw()
    for p in pix_orb0.points:
        pixels[p[0]][p[1]] = 1
    pix_orb0.motion()



    pygame.init()
    SCREEN = pygame.display.set_mode((window_res[0], window_res[1]))
    SCREEN.fill(Colors.BG)
    while True:

        pix_orb0.motion()
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
