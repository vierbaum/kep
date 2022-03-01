#!/usr/bin/env python3

import pygame
import sys
import math
import numpy as np


window_res = [1366, 768]

pixels = [[0 for _ in range(window_res[1])] for _ in range(window_res[0])]
pixels[10][10] = 1

def drawGrid(SCREEN):
    # looping through grid
    for x in range(0, window_res[0] - 1):
        for y in range(0, window_res[1] - 1):
            # checking value of pixel
            if pixels[x][y] == 1:
                rect = pygame.Rect(x, y, 1, 1)
                color = [142, 192, 124]
                pygame.draw.rect(SCREEN, tuple(color), rect)


# positive e, pos on right, if negative e, pos on left
def orbit(pos, a, e):
    points = []
    # looping through all angles
    for theta in np.arange(0, 360, 0.001):
        # polar coordinate from pos (https://en.wikipedia.org/wiki/Kepler_orbit#Development_of_the_laws)
        d = (a * (1 - e**2))/(1 + e * math.cos(theta))
        # converting to Cartesian
        y = math.sin(theta) * d + pos[1]
        x = math.cos(theta) * d + pos[0]
        if [int(x), int(y)] not in points:
            points.append([int(x), int(y)])
    return points

def sphere(pos, rad):
    # looping through region of circle
    for x in range(pos[0] - rad, pos[0] + rad):
        for y in range(pos[1] - rad, pos[1] + rad):
            # checking if position is in circle
            if (x - pos[0])**2 + (y - pos[1])**2 <= 1:
                pixels[x][y] = 1


if __name__ == "__main__":
    for p in orbit([500, 100], 100, -0.75):
        pixels[p[0]][p[1]] = 1
    sphere([500, 100], 5)
    pygame.init()
    SCREEN = pygame.display.set_mode((window_res[0], window_res[1]))
    SCREEN.fill((27, 29, 30))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        drawGrid(SCREEN)
        pygame.display.update()
