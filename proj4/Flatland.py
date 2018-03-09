import graphics
from random import *
import copy
import time
from operator import add

class Flatland:
    def __init__(self, draw_it):
        self.pos = (5, 5)
        self.dir = (0, -1)
        self.n = 10
        self.flatland = [[0 for x in range(self.n)] for x in range(self.n)]
        self.foods = 0

        for x in range(self.n):
            for y in range(self.n):
                if uniform(0,1) < 0.33:
                    self.flatland[x][y] = 1
                    self.foods += 1
                elif uniform(0,1) < 0.33:
                    self.flatland[x][y] = 2
                else:
                    self.flatland[x][y] = 0

        self.backup = copy.deepcopy(self.flatland)
        self.speed = 0.1

    def init_draw(self):
        field_size = 10
        radius = 5
        offset = 5

        self.win = graphics.GraphWin('World', 10 * field_size, 10 * field_size)
        self.win.setBackground('white')

        self.agent = graphics.Circle(graphics.Point(offset + self.pos[0] * 10, offset + self.pos[1] * 10), radius)
        self.agent.setFill("Yellow")
        self.agent.draw(self.win)

        self.agent_dir = graphics.Line(self.agent.getCenter(),
            graphics.Point(offset + self.pos[0] * 10 + 10 * self.dir[0], offset + self.pos[1] * 10 + 10 * self.dir[1]))
        self.agent_dir.draw(self.win)

        self.circles = [[None for x in range(self.n)] for x in range(self.n)]
        for x in range(self.n):
            for y in range(self.n):
                if self.flatland[x][y] != 0:
                    self.circles[x][y] = graphics.Circle(graphics.Point(offset + x * 10, offset + y * 10), radius)
                    if self.flatland[x][y] == 1:
                        self.circles[x][y].setFill("Green")
                    else:
                        self.circles[x][y].setFill("Red")
                    self.circles[x][y].draw(self.win)

    def reset_pos(self):
        self.pos = (5,5)
        self.dir = (0,-1)

    def get_right(self):
        if self.pos[0] - self.dir[1] < 0:
            return self.flatland[self.n - 1][self.pos[1] - self.dir[0]]
        if self.pos[0] - self.dir[1] >= self.n:
            return self.flatland[0][self.pos[1] - self.dir[0]]
        if self.pos[1] - self.dir[0] < 0:
            return self.flatland[self.pos[0] - self.dir[1]][self.n - 1]
        if self.pos[1] - self.dir[0] >= self.n:
            return self.flatland[self.pos[0] - self.dir[1]][0]
        return self.flatland[self.pos[0] - self.dir[1]][self.pos[1] - self.dir[0]]

    def get_left(self):
        if self.pos[0] + self.dir[1] < 0:
            return self.flatland[self.n - 1][self.pos[1] + self.dir[0]]
        if self.pos[0] + self.dir[1] >= self.n:
            return self.flatland[0][self.pos[1] + self.dir[0]]
        if self.pos[1] + self.dir[0] < 0:
            return self.flatland[self.pos[0] + self.dir[1]][self.n - 1]
        if self.pos[1] + self.dir[0] >= self.n:
            return self.flatland[self.pos[0] + self.dir[1]][0]
        return self.flatland[self.pos[0] + self.dir[1]][self.pos[1] + self.dir[0]]

    def get_forward(self):
        if self.pos[0] + self.dir[0] < 0:
            return self.flatland[self.n - 1][self.pos[1] + self.dir[1]]
        if self.pos[0] + self.dir[0] >= self.n:
            return self.flatland[0][self.pos[1] + self.dir[1]]
        if self.pos[1] + self.dir[1] < 0:
            return self.flatland[self.pos[0] + self.dir[0]][self.n - 1]
        if self.pos[1] + self.dir[1] >= self.n:
            return self.flatland[self.pos[0] + self.dir[0]][0]
        return self.flatland[self.pos[0] + self.dir[0]][self.pos[1] + self.dir[1]]

    def set_new_pos(self, motor):
        new_dir = 0
        best = motor[0]
        for i in range(1,3):
            if motor[i] > best:
                new_dir = i
                best = motor[i]

        if new_dir == 0: #forward
            self.pos = tuple(map(add, self.pos, self.dir))
        if new_dir == 1: #left
            #multiplicate dir with   0 1
            #                       -1 0
            self.dir = (self.dir[1],self.dir[0] * (-1))
            self.pos = tuple(map(add, self.pos, self.dir))
        if new_dir == 2: #right
            # multiplicate dir with     0 -1
            #                           1  0
            self.dir = (self.dir[1] * (-1), self.dir[0])
            self.pos = tuple(map(add, self.pos, self.dir))

        # torroidal grid -> if agents leaves it, he comes in again from the other side
        if self.pos[0] >= self.n:
            self.pos = (0, self.pos[1])
        if self.pos[0] < 0:
            self.pos = (self.n - 1, self.pos[1])
        if self.pos[1] >= self.n:
            self.pos = (self.pos[0], 0)
        if self.pos[1] < 0:
            self.pos = (self.pos[0], self.n - 1)

    def undraw_circle(self,x,y):
        self.circles[x][y].undraw()

    def update_drawing(self):
        offset = 5
        self.agent.move(offset + (self.pos[0] * 10) - self.agent.getCenter().getX(),
                        offset + (self.pos[1] * 10) - self.agent.getCenter().getY())
        self.agent_dir.undraw()
        self.agent_dir = graphics.Line(self.agent.getCenter(),
                                        graphics.Point(offset + self.pos[0] * 10 + 10 * self.dir[0],
                                                       offset + self.pos[1] * 10 + 10 * self.dir[1]))
        self.agent_dir.draw(self.win)
        time.sleep(self.speed)