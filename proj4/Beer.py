from random import *
import graphics
import time

class Beer:
    def __init__(self, draw_it, wrap):
        self.width = 30
        self.height = 15
        self.posX = 14
        self.posY = self.height - 1
        self.score = 0
        self.draw_it = draw_it
        self.wrap = wrap
        self.dx = 0
        self.pulled = 0

        self.missed = -1
        self.killed = -4
        self.caught = 2
        self.avoided = 1

        if draw_it:
            self.init_draw()

        self.gen_block()

    def __del__(self):
        if self.draw_it:
            self.win.quit()

    def init_draw(self):
        self.blocksize = 20
        self.win = graphics.GraphWin('World', self.width * self.blocksize, self.height * self.blocksize)
        self.win.setBackground('white')

        self.agent = [None] * 5
        self.upperY = (self.posY) * self.blocksize
        self.lowerY = (self.posY + 1) * self.blocksize
        for i in range(len(self.agent)):
            self.agent[i] = graphics.Rectangle(graphics.Point(self.blocksize * (self.posX - 2 + i), self.upperY),
                                               graphics.Point(self.blocksize * (self.posX - 1 + i), self.lowerY))
            self.agent[i].setFill("Yellow")
            self.agent[i].draw(self.win)

    def gen_block(self):
        size = randint(1, 6)
        pos = [None] * 2
        pos[1] = 0
        pos[0] = randint(0, self.width - 1 - size)
        self.block = BeerBlock(size, pos)

        if self.draw_it:
            #draw block
            self.block_graphics = [None] * self.block.size
            for i in range(self.block.size):
                upperY = (self.block.pos[1]) * self.blocksize
                lowerY = (self.block.pos[1] + 1) * self.blocksize
                self.block_graphics[i] = graphics.Rectangle(graphics.Point(self.blocksize * (self.block.pos[0] + i), upperY),
                                                            graphics.Point(self.blocksize * (self.block.pos[0] + 1.0 + i),
                                                                           lowerY))
                if self.block.size <= 5:
                    self.block_graphics[i].setFill("Green")
                else:
                    self.block_graphics[i].setFill("Red")
                self.block_graphics[i].draw(self.win)

    def get_sensors(self):
        if self.wrap:
            n_sensors = 5
        else:
            n_sensors = 7
        sensors = [0] * n_sensors
        for i in range(5):
            if self.block.is_under(self.posX - 2 + i):
                sensors[i] = 1
        if not self.wrap:
            if self.posX == 2:
                sensors[5] = 1
            elif self.posX == self.width - 3:
                sensors[6] = 1
        return sensors

    def move_block(self, y):
        # move block
        if self.block.fall(y, self.posY):
            self.update_score()

    def pull(self):
        self.move_block(self.posY - self.block.pos[1])
        self.pulled = 1

    def timestep(self, speed):
        if not self.pulled:
            self.move_block(1)

        if self.draw_it:
            self.update_drawing(speed)

        # new block?
        if self.block.remove:
            self.gen_block()
            self.block.remove = False

        return self.score

    def update_drawing(self, sleep):
        if self.pulled == 1:
            self.agent[0].setFill("Orange")
            self.agent[4].setFill("Orange")
            self.pulled = 0
        else:
            self.agent[0].setFill("Yellow")
            self.agent[4].setFill("Yellow")
        #move agent
        for i in range(len(self.agent)):
            if self.wrap:
                self.agent[i].move((self.agent[i].getCenter().getX() + self.dx * self.blocksize) % (self.blocksize * self.width) - self.agent[i].getCenter().getX(), 0)
            else:
                self.agent[i].move(self.blocksize * (self.posX - self.old_posX), 0)

        if self.block.remove:
            for i in range(self.block.size):
                self.block_graphics[i].undraw()
        else:
            y = self.blocksize
            y += self.pulled * (self.blocksize * (self.posY - 1.5) - self.block_graphics[0].getCenter().getY())
            for i in range(self.block.size):
                self.block_graphics[i].move(0, y)

        time.sleep(sleep)

    def update_score(self):
        # if block is small
        if self.block.size <= 5:
            covered = self.block.size
            for i in range(5):
                if self.block.is_under(self.posX - 2 + i):
                    covered -= 1
            if covered == 0:
                self.score += self.caught
                return
            self.score += self.missed
            return
        # if block is big
        for i in range(5):
            if self.block.is_under(self.posX - 2 + i):
                self.score += self.killed
                return
        self.score += self.avoided

    def move(self, n):
        if not self.wrap:
            if self.posX - 2 + n < 0 or self.posX + 1 + n > self.width:
                self.dx = 0
                self.old_posX = self.posX
                return

        self.dx = n
        self.old_posX = self.posX
        self.posX += n

        if self.wrap:
            if self.posX < 0:
                self.posX = self.width + self.posX
            elif self.posX >= self.width:
                self.posX = self.posX - self.width



class BeerBlock:
    def __init__(self, size, pos):
        self.size = size
        self.pos = pos

    def fall(self, y, bottom):
        self.pos[1] += y

        # set remove flag if it hits the ground
        self.remove = (self.pos[1] == bottom)

        return self.remove

    def is_under(self, x):
        if x >= self.pos[0] and x < self.pos[0] + self.size:
            return True
        return False