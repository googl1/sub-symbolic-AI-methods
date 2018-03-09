import graphics
import operator
import thread
import time


def getch():
    p = input()
    return p

char = None


def keypress():
    global char
    while 1:
        char = getch()

thread.start_new_thread(keypress, ())


class Flatland:
    def __init__(self, draw_it, file):
        f = open(file, 'r')
        line = f.readline()
        nums = [int(n) for n in line.split()]

        self.field_size = 20
        self.width = nums[0]
        self.height = nums[1]
        self.pos = (nums[2], nums[3])
        self.n_food = nums[4]
        self.score = 0
        self.poison_score = 0

        self.game_finished = 0
        self.draw_it = draw_it

        self.flatland = [[0 for x in range(self.width)] for x in range(self.height)]

        for y in range(self.height):
            line = f.readline()
            self.flatland[y] = [int(n) for n in line.split()]


        if draw_it:
            self.init_draw()
        self.speed = 0.5

    def __del__(self):
        if self.draw_it:
            self.win.close()

    def init_draw(self):
        radius = 10
        offset = 10

        self.win = graphics.GraphWin('World', self.width * self.field_size, self.height * self.field_size)
        self.win.setBackground('white')

        self.arrows = [None] * self.height * self.width

        self.agent = graphics.Circle(graphics.Point(offset + self.pos[0] * self.field_size, offset + self.pos[1] * self.field_size), radius)
        self.agent.setFill("Yellow")
        self.agent.draw(self.win)

        self.circles = [[None for x in range(self.width)] for y in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                if self.flatland[y][x] != 0:
                    if self.flatland[y][x] == -2:
                        rect = graphics.Rectangle(graphics.Point(x * self.field_size, y * self.field_size),
                                           graphics.Point((x+1) * self.field_size, (y+1) * self.field_size))
                        rect.setFill("Blue")
                        rect.setOutline("White")
                        rect.draw(self.win)
                    else:
                        self.circles[y][x] = graphics.Circle(graphics.Point(offset + x * self.field_size, offset + y * self.field_size), radius)
                        if self.flatland[y][x] > 0:
                            self.circles[y][x].setFill("Green")
                        else:
                            self.circles[y][x].setFill("Red")
                        self.circles[y][x].draw(self.win)

    def get_right(self):
        if self.pos[0] + 1 >= self.width:
            return self.flatland[self.pos[1]][0]
        return self.flatland[self.pos[1]][self.pos[0] + 1]

    def get_left(self):
        if self.pos[0] - 1 < 0:
            return self.flatland[self.pos[1]][self.width - 1]
        return self.flatland[self.pos[1]][self.pos[0] - 1]

    def get_up(self):
        if self.pos[1] - 1 < 0:
            return self.flatland[self.height - 1][self.pos[0]]
        return self.flatland[self.pos[1] - 1][self.pos[0]]

    def get_down(self):
        if self.pos[1] + 1 >= self.height:
            return self.flatland[0][self.pos[0]]
        return self.flatland[self.pos[1] + 1][self.pos[0]]

    def set_new_pos(self, a, learner):
        self.pos = tuple(map(operator.add, self.pos, a))

        # torroidal grid -> if agents leaves it, he comes in again from the other side
        if self.pos[0] >= self.width:
            self.pos = (0, self.pos[1])
        if self.pos[0] < 0:
            self.pos = (self.width - 1, self.pos[1])
        if self.pos[1] >= self.height:
            self.pos = (self.pos[0], 0)
        if self.pos[1] < 0:
            self.pos = (self.pos[0], self.height - 1)

        r = self.flatland[self.pos[1]][self.pos[0]]
        if r > 0:
            self.n_food -= 1
            self.flatland[self.pos[1]][self.pos[0]] = 0
            self.score += 1
            if self.draw_it:
                print "food: " + str(self.score)

            if self.n_food == 0:
                self.game_finished = 1
        elif r < 0:
            if r == -2:
                if self.game_finished == 1:
                    self.game_finished = 2
                else:
                    r = 0
            else:
                self.flatland[self.pos[1]][self.pos[0]] = 0
                self.poison_score += 1
                if self.draw_it:
                    print "poison: " + str(self.poison_score)

        if self.draw_it:

            self.update_arrows(learner)
            self.undraw_circle(self.pos[1], self.pos[0])
            self.update_drawing()

        return r

    def update_arrows(self, learner):
        for y in range(self.height):
            for x in range(self.width):
                if self.arrows[x + y*self.width] is not None:
                    self.arrows[x + y*self.width].undraw()
                a = learner.select_action(((x, y), learner.new_state[1]), learner.q, 1, False)
                self.arrows[x + y*self.width] = graphics.Line(graphics.Point((x + 0.5) * self.field_size, (y + 0.5) * self.field_size),
                                                              graphics.Point((x + 0.5) * self.field_size + a[0] * self.field_size,
                                                                             (y + 0.5) * self.field_size + a[1] * self.field_size))
                self.arrows[x + y*self.width].setArrow("last")
                self.arrows[x + y*self.width].draw(self.win)

    def undraw_circle(self,x,y):
        if self.circles[x][y] is not None:
            self.circles[x][y].undraw()

    def update_drawing(self):
        offset = 10
        self.agent.move(offset + (self.pos[0] * self.field_size) - self.agent.getCenter().getX(),
                        offset + (self.pos[1] * self.field_size) - self.agent.getCenter().getY())

        time.sleep(self.speed)

        if char is not None:
            try:
                speed = int(char)
                if speed >= 0 and speed <=9:
                    self.speed = 0.9 - speed / 10.0
            except:
                print "enter a number between 0 and 9 to set the game speed"