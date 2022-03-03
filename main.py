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


def drawGrid(SCREEN):
    # looping through grid
    for x in range(0, window_res[0] - 1):
        for y in range(1, window_res[1]):
            # checking value of pixel
            if pixels[x][window_res[1] - y] == 1:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.red)
                pygame.draw.rect(SCREEN, color, rect)
            if pixels[x][window_res[1] - y] == 2:
                rect = pygame.Rect(x, y, 1, 1)
                color = pygame.Color(Colors.green)
                pygame.draw.rect(SCREEN, color, rect)


def sphere(pos, rad):
    # looping through region of circle
    for x in range(pos[0] - rad, pos[0] + rad):
        for y in range(pos[1] - rad, pos[1] + rad):
            # checking if position is in circle
            if (x - pos[0])**2 + (y - pos[1])**2 <= rad**2:
                #print(x, y)
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
    tri = Triangle(triag_points)
    tri.draw()
    for p in tri.points:
        pixels[int(p[0])][int(p[1])] = 2
    print("AREA", tri.getArea())

def motion():
    # TODO shit-ton of logic
    pass


if __name__ == "__main__":
    pix_orb0 = Orbit([500, 600], 200, -0.75)
    pix_orb0.draw()
    for p in pix_orb0.points:
        pixels[p[0]][p[1]] = 1
    sphere([500, 600], 5)
    #areaEl(5, 10, pix_orb0.points_angles, [500, 600])
    pix_orb0.motion()



    pygame.init()
    SCREEN = pygame.display.set_mode((window_res[0], window_res[1]))
    SCREEN.fill(Colors.BG)
    while True:

        pix_orb0.motion()
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
