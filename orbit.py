#!/usr/bin/env python3

import numpy as np
import math
from numba import njit
from planet import Planet
from triangle import Triangle
from vars import *

class Orbit():

    def __init__(self, pos, a, e, debug, visual, perc=0.001):
        self.debug = debug
        self.visual = visual
        self.planet = Planet(500, [], 10)
        self.pos = pos
        self.a = a
        self.e = e
        self.perc = perc
        self.points_angles = []
        self.points = []
        self.sphere(5)


    def draw(self):
        points = dr(self.a, self.e, self.pos)
        self.points = points[0]
        self.points_angles = points[1]


    def sphere(self, rad):
        # looping through region of circle
        for x in range(self.pos[0] - rad, self.pos[0] + rad):
            for y in range(self.pos[1] - rad, self.pos[1] + rad):
                # checking if position is in circle
                if (x - self.pos[0])**2 + (y - self.pos[1])**2 <= rad**2:
                    self.points.append([x, y])


    def motion(self):
        stepsize = 0.01
        # checking if planet already has a position
        if self.planet.position == []:
            d = (self.a * (1 - self.e**2))/(1 + self.e)
            # converting to Cartesian
            y = self.pos[1]
            x = d + self.pos[0]
            self.planet.position = [x, y, 0, d]
        else:
            # NUTS
            for theta in np.arange(self.planet.position[-2] + stepsize, self.planet.position[-2] + 359, stepsize):
                theta = theta % 360
                d = (self.a * (1 - self.e**2))/(1 + self.e * math.cos(theta))
                # converting to Cartesian
                y = math.sin(theta) * d + self.pos[1]
                x = math.cos(theta) * d + self.pos[0]
                triangle = Triangle([self.pos, self.planet.position, [x, y]], self.debug)
                if self.debug:
                    print("MOTION T {}, X {}, Y {}, D {}, A {}, POS {}".format(theta, x, y, d, triangle.getArea(), self.planet.position))
                if triangle.getArea() >= self.planet.v:
                    if self.visual:
                        triangle.draw()
                        for p in triangle.points:
                            pixels[int(p[0])][int(p[1])] = 2
                    self.planet.position = [x, y, theta, d]
                    self.planet.draw()
                    return




@njit(parallel = True)
def dr(a, e, pos):
    points = []
    points_angles = []
    for theta in np.arange(0, 360, 0.001):
        # polar coordinate from pos (https://en.wikipedia.org/wiki/Kepler_orbit#Development_of_the_laws)
        d = (a * (1 - e**2))/(1 + e * math.cos(theta))
        # converting to Cartesian
        y = math.sin(theta) * d + pos[1]
        x = math.cos(theta) * d + pos[0]
        if [int(x), int(y)] not in points:
            points.append([int(x), int(y)])
        points_angles.append([int(x), int(y), x, y, theta, d])
    return points, points_angles
