#!/usr/bin/env python3

import math
from line import Line
from vars import *
import numpy as np

class Triangle():
    points = []
    def __init__(self, points, debug):
        self.debug = debug
        self.Bpoints = points
        self.ls = [Line(), Line(), Line()]
        self.ls[0].eqp([self.Bpoints[0], self.Bpoints[2]])
        self.ls[1].eqp([self.Bpoints[1], self.Bpoints[2]])
        self.ls[2].eqp([self.Bpoints[0], self.Bpoints[1]])

    def getArea(self):
        lengths = []
        for line in self.ls:
            lengths.append(line.getLength())
        # https://www.mathopenref.com/heronsformula.html
        if self.debug:
            print("TRI LENGTHS", lengths)
        p = sum(lengths)/2
        self.area = math.sqrt(p * (p - lengths[0]) * (p - lengths[1]) * (p - lengths[2]))
        return self.area

    def draw(self):
        self.ls[0].drawp([self.Bpoints[0], self.Bpoints[2]], perc=1)
        self.ls[1].drawp([self.Bpoints[1], self.Bpoints[2]], perc=1)
        self.ls[2].drawp([self.Bpoints[0], self.Bpoints[1]], perc=1)
        for p in self.Bpoints:
            self.sphere(p, 5)
        for l in self.ls:
            for p in l.points:
                self.points.append(p)
                #pixels[int(p[0])][int(p[1])] = 1

    def sphere(self, pos, rad):
        # looping through region of circle
        for x in range(int(pos[0] - rad), int(pos[0] + rad)):
            for y in range(int(pos[1] - rad), int(pos[1] + rad)):
                # checking if position is in circle
                if (x - pos[0])**2 + (y - pos[1])**2 <= rad**2:
                    self.points.append([x, y])
