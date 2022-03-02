#!/usr/bin/env python3
from vars import *
import numpy as np
import math

class Line ():
    points = []
    dx = None
    dy = None
    dydx = None
    c = None
    length = 0
    def __init__(self, points=[], dydx=None, c=None):
        self.points = points
        self.dydx = dydx
        self.c = c


    def draw(self, interv, perc=0.1):
        # loopint through all x values, bigger than x0 and smaller than x1
        if interv[0] > interv[1]: interv = interv[::-1]
        print("INTERV", interv)
        points = []
        for x in np.arange(interv[0], interv[1], perc):
            for y in range(window_res[1]):
                # checking if roughly y
                #print(x, self.dydx, self.c)
                ty = x * self.dydx + self.c
                if (ty >= y*0.999 and ty <= y*1.001) and ty > 0 and ty < window_res[1]:
                    #print("{}*{} + {} = {}".format(x, self.dxdy, self.c, y))
                    points.append([x, y])
                if (ty < 0 and self.dydx < 0) or (ty > window_res[1] and self.dydx > 0):
                    self.points = points
                    return
        self.points = points

    def drawp(self, upoints, perc=0.1):
        # setting the point with smaller x as first (if you wanna use 2 points with the same x, ... ffs)
        points = upoints if upoints[0][0] < upoints[1][0] else [upoints[1], upoints[0]]
        # getting x and y changes
        self.dy = points[1][1] - points[0][1]
        self.dx = points[1][0] - points[0][0]
        self.dydx = self.dy/self.dx
        # y at x = 0
        self.c = points[0][1] - points[0][0] * self.dydx
        self.draw([points[0][0], points[1][0]], perc)

    def drawop(self, point, l2=None, perc=0.1):
        #print(point)
        self.c = point[1] - point[0] * self.dydx
        self.draw([0, window_res[0]])
        if l2 != None:
            print(point[0], self.comp(l2))
            self.draw([point[0], self.comp(l2)[0]], perc)

    def comp(self, l):
        for p1 in l.points:
            for p2 in self.points:
                # searching for "similar" point with threshold of 0.001
                if (p1[0] >= 0.999*p2[0] and p1[0] <= 1.001*p2[0]) and (p1[1] >= 0.999*p2[1] and p1[1] <= 1.001*p2[1]):
                    print("P1", p1, p2)
                    return p1
        return None

    def mkparallel(self, point):
        parallel = Line()
        parallel.dydx = self.dydx
        # getting y for x = 0
        parallel.c = point[1] - point[0] * parallel.dydx
        return parallel

    def getLength(self):
        dy = abs(self.points[0][1] - self.points[-1][1])
        dx = abs(self.points[0][0] - self.points[-1][0])
        # pythagoras
        self.length = math.sqrt(dy**2 + dx**2)
        return self.length
