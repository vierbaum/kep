#!/usr/bin/env python3

from vars import *
import orbit

class Planet():
    def __init__(self, v, pos, s, orb=False, visual=False, color=1):
        self.v = v
        self.position = []
        self.size = s
        self.points = []
        self.orbits = []
        self.orb = orb
        self.visual = visual
        self.color = color

    def draw(self):
        for p in self.points:
            pixels[p[0]][p[1]] = 99
        self.points = []
        # looping through region of circle
        for x in range(int(self.position[0] - 1.25 * self.size), int(self.position[0] + 1.25 * self.size)):
            for y in range(int(self.position[1] - 1.25 * self.size), int(self.position[1] + 1.25 * self.size)):
                # checking if position is in circle
                if (x - self.position[0])**2 + (y - self.position[1])**2 <= self.size**2:
                    if pixels[x][y] == 0 or pixels[x][y] == 99:
                        self.points.append([x, y])
                        pixels[x][y] = self.color

    def aorb(self):
        if self.orbits == [] and self.orb is not False:
            for o in self.orb:
                self.orbits.append(orbit.Orbit(self.position, o[0], o[1], o[2], o[3], o[4], o[5]))
        #[pos a, e, debug, visual, ao]
        for orb in self.orbits:
            orb.pos = self.position
            if self.visual:
                orb.draw()
                for p in orb.points:
                    pixels[p[0]][p[1]] = 1
            orb.motion()


    def __str__(self):
        return f'(Planet, v={self.v}, size={self.size}, pos={self.position}, orbits={self.orbits})'
