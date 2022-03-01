#!/usr/bin/env python3

from enum import Enum
import pygame
import sys
import math
import numpy as np

class Colors ():
    BG = "#1B1D1E"
    red = "#CC241D"
    green = "#98971A"
    yellow = "#D79921"
    blue = "#458588"
    purple = "#B16286"
    aqua = "#689D6A"
    orange = "#D65D0E"
    gray = "#928374"
    grayl = "#A89984"
    redl = "#FB4934"
    greenl = "#B8BB26"
    yellowl = "#FABD2F"
    bluel = "#83A598"
    purplel = "#D3869B"
    aqual = "#8EC07C"
    orangel = "#FE8019"
    FG = "#F8F8F2"


window_res = [1366, 768]

pixels = [[0 for _ in range(window_res[1])] for _ in range(window_res[0])]

def drawGrid(SCREEN):
    # looping through grid
    for x in range(0, window_res[0] - 1):
        for y in range(0, window_res[1] - 1):
            # checking value of pixel
            if pixels[x][y] == 1:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.red)
                pygame.draw.rect(SCREEN, color, rect)


# positive e, pos on right, if negative e, pos on left
def orbit(pos, a, e):
    points = []
    points_angles = []
    # looping through all angles
    for theta in np.arange(0, 360, 0.001):
        # polar coordinate from pos (https://en.wikipedia.org/wiki/Kepler_orbit#Development_of_the_laws)
        d = (a * (1 - e**2))/(1 + e * math.cos(theta))
        # converting to Cartesian
        y = math.sin(theta) * d + pos[1]
        x = math.cos(theta) * d + pos[0]
        if [int(x), int(y)] not in points:
            points.append([int(x), int(y)])
        points_angles.append([int(x), int(y), x, y, theta, d])
    return points_angles

def sphere(pos, rad):
    # looping through region of circle
    for x in range(pos[0] - rad, pos[0] + rad):
        for y in range(pos[1] - rad, pos[1] + rad):
            # checking if position is in circle
            if (x - pos[0])**2 + (y - pos[1])**2 <= rad**2:
                print(x, y)
                pixels[x][y] = 1

def areaEl(theta0, theta1, points, orig):
    post0 = 0
    post1 = 0
    # getting points at angle values
    for i in points:
        if i[-2] == theta0:
            post0 = i
        elif i[-2] == theta1:
            post1 = i
    # all points of triangle
    triag_points = [post0[:2], post1[:2], orig]
    # nice (useless) lines
    for p in drawLinep([triag_points[1], triag_points[0]]):
        pixels[p[0]][p[1]] = 1
    for p in drawLinep([triag_points[2], triag_points[0]]):
        pixels[p[0]][p[1]] = 1
    for p in drawLinep([triag_points[2], triag_points[1]]):
        pixels[p[0]][p[1]] = 1

    # not implemented logic
    for i in triag_points:
        print(i)
        sphere(i, 5)
    print(triag_points)


def drawLine(interv, m, c):
    points = []
    # loopint through all x values, bigger than x0 and smaller than x1
    for x in range(interv[0], interv[1]):
        for y in range(window_res[1]):
            # checking if roughly y
            if int(x * m + c) == y:
                points.append([x, y])
    return points

def drawLinep(upoints):
    # setting the point with smaller x as first (if you wanna use 2 points with the same x, ... ffs)
    points = upoints if upoints[0][0] < upoints[1][0] else [upoints[1], upoints[0]]
    # getting x and y changes
    dy = points[1][1] - points[0][1]
    dx = points[1][0] - points[0][0]
    # y at x = 0
    c = points[0][1] - points[0][0] * (dy/dx)
    #print("DP", points, dy, dx, dy/dx, c)
    return drawLine([points[0][0], points[1][0]], dy/dx, c)


if __name__ == "__main__":
    pix_orb0 = orbit([500, 100], 100, 0.75)
    for p in pix_orb0:
        pixels[p[0]][p[1]] = 1
    sphere([500, 100], 5)
    areaEl(5, 100, pix_orb0, [500, 100])
    pygame.init()
    SCREEN = pygame.display.set_mode((window_res[0], window_res[1]))
    SCREEN.fill(Colors.BG)
    while True:
        click = pygame.mouse.get_pressed()[0]
        if click:
            xm,ym = pygame.mouse.get_pos()
            print(xm, ym)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        drawGrid(SCREEN)
        pygame.display.update()
