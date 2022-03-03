#!/usr/bin/env python3

from vars import *

class Planet():
    def __init__(self, v, pos, s):
        self.v = v
        self.position = []
        self.size = s
        self.points = []

    def draw(self):
        for p in self.points:
            pixels[p[0]][p[1]] = 99
        self.points = []
        # looping through region of circle
        for x in range(int(self.position[0]) - self.size, int(self.position[0]) + self.size):
            for y in range(int(self.position[1]) - self.size, int(self.position[1]) + self.size):
                # checking if position is in circle
                if (x - self.position[0])**2 + (y - self.position[1])**2 <= self.size**2:
                    self.points.append([x, y])
                    pixels[x][y] = 1
