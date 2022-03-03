#!/usr/bin/env python3

import numpy as np
import math
from numba import njit
from planet import Planet
from triangle import Triangle
from vars import *

class Orbit():
    pos = None
    a = None
    e = None
    perc = None
    points_angles = []
    points = []
    planet = Planet(500, [], 10)

    def __init__(self, pos, a, e, perc=0.001):
        self.pos = pos
        self.a = a
        self.e = e
        self.perc = perc


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
                    #print(x, y)
                    self.points.append([x, y])


    def motion(self):
        stepsize = 0.01
        # checking if planet already has a position
        if self.planet.position == []:
            # if not, search for point at 0 degree and assign
            for p in range(len(self.points_angles)):
                if self.points_angles[p][-2] == 0:
                    self.planet.position = self.points_angles[p][2:]
        else:
            # NUTS
            for theta in np.arange(self.planet.position[-2] + stepsize, self.planet.position[-2] + 359, stepsize):
                theta = theta % 360
                print("THETA", theta)
                d = (self.a * (1 - self.e**2))/(1 + self.e * math.cos(theta))
                # converting to Cartesian
                y = math.sin(theta) * d + self.pos[1]
                x = math.cos(theta) * d + self.pos[0]
                print("X {}, Y {}".format(x, y))
                triangle = Triangle([self.pos, self.planet.position, [x, y]])
                print("AREA", triangle.getArea())
                if triangle.getArea() >= 1000:
                    triangle.draw()
                    for p in triangle.points:
                        pixels[int(p[0])][int(p[1])] = 2
                    self.planet.position = [x, y, theta, d]
                    return
                # self.planet.position = [x, y, theta, d]

        print("PLANET POS", self.planet.position)



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
