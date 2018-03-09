from Tkinter import *
from graphics import *
from random import *
from math import *
import time
from operator import *

#size of the world
x_max = 1000
y_max = 500


boid_radius = 5

max_velo = 2
max_velo_p = 3

obstacles = []
predators = []

win = GraphWin('World', x_max, y_max) # give title and dimensions

class Obstacle:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius
        self.circle = Circle(self.position, self.radius)
        self.circle.setFill("Black")
        self.circle.draw(win)

class Boid:
        def __init__(self, position):
            self.position = position
            self.velocity = (0,0)
            self.redraw = 0

        #separation force
        def calc_sep_force(self,n, r):
            f = (0,0)
            for i in n:
                fac = dist(i.position, self.position)
                d = dist_vec(self.position, i.position)
                fac -= r + boid_radius
                fac /= r
                fac = pow(fac,2)
                d = map (mul, d, (fac,fac))
                f = map(add, f ,d)
            return f

        #alignment force
        def calc_align_force(self,n):
            f = (0,0)
            for i in n:
                f = map(add, f, i.velocity)
            if f != (0,0):
                norm_vec(f)
            return f

        #cohesion force
        def calc_coh_force(self,n):
            if len(n) == 0:
                return (0,0)
            c = (0,0)
            for i in n:
                c = map (add, c, (i.position.x, i.position.y))
            c[0] /= len(n)
            c[1] /= len(n)
            return norm_vec(map(sub,c,(self.position.x,self.position.y)))

        #obstacle avoidance force
        def calc_obs_force(self,o,r):
            if len(o) == 0 or r == 0:
                return (0,0)
            f = (0,0)
            for i in o:
                fac = dist(i.position, self.position)
                d = dist_vec(self.position, i.position)
                fac -= r + i.radius
                fac /= r
                fac = pow(fac,2)
                d = map (mul, d, (fac,fac))
                f = map(add, f ,d)
            return f

        def calc_fear_force(self,o,r):
            if len(o) == 0 or r == 0:
                return (0,0)
            f = (0,0)
            for i in o:
                fac = dist(i.position, self.position)
                d = dist_vec(self.position, i.position)
                fac -= r + boid_radius
                fac /= r
                #fac *= 10
                fac = pow(fac,2)
               # d = norm_vec(d)
                d = map (mul, d, (fac,fac))
                f = map(add, f ,d)
            #if f != (0,0):
             #   f = norm_vec(f)
            return f

        def updateBoid (self, sep_weight, align_weight, coh_weight, neighbors,
                r, obstacles, obs_weight, hunters, fear_weight):
            #neighbors = boids closer than r

            #calculate forces
            self.sep = self.calc_sep_force(neighbors, r)
            self.sep = map (mul, self.sep, (sep_weight, sep_weight))

            self.align = self.calc_align_force(neighbors)
            self.align = map (mul, self.align, (align_weight, align_weight))

            self.coh = self.calc_coh_force(neighbors)
            self.coh = map (mul, self.coh, (coh_weight, coh_weight))

            self.obs = self.calc_obs_force(obstacles, r)
            self.obs = map (mul, self.obs, (obs_weight,obs_weight))

            self.fear = self.calc_fear_force(hunters, r)
            self.fear = map (mul, self.fear, (fear_weight, fear_weight))

            #sum up forces
            v = self.sep
            v = map(add, v, self.sep)
            v = map(add, v, self.align)
            v = map(add, v, self.coh)
            v = map(add, v, self.obs)
            v = map(add, v, self.fear)
            self.velocity = map(add, self.velocity, norm_vec(v))

            #limit to max velocity
            if self.velocity[0] > max_velo:
                self.velocity[0] = max_velo
            elif self.velocity[0] < max_velo*(-1):
                self.velocity[0] = max_velo*(-1)
            if self.velocity[1] > max_velo:
                self.velocity[1] = max_velo
            elif self.velocity[1] < max_velo*(-1):
                self.velocity[1] = max_velo*(-1)

            #update position
            self.position.x += self.velocity[0]
            self.position.y += self.velocity[1]

            #set redraw if out of world limits
            if self.position.x + boid_radius < 0:
                self.position.x = x_max + boid_radius
                self.redraw = 1
            if self.position.x - boid_radius > x_max:
                self.position.x = 0 - boid_radius
                self.redraw = 1
            if self.position.y + boid_radius < 0:
                self.position.y = y_max + boid_radius
                self.redraw = 1
            if self.position.y -boid_radius > y_max:
                self.position.y = 0 - boid_radius
                self.redraw = 1

class Predator(Boid):
    def __init__(self, position):
            self.position = position
            self.velocity = (0,0)
            self.redraw = 0

    def updatePred (self, sep_weight, coh_weight, neighbors,
                r, obstacles, obs_weight, prey):
            #neighbors = predators closer than r
            self.sep = self.calc_sep_force(neighbors, r)
            self.sep = map (mul, self.sep, (sep_weight, sep_weight))

            self.coh = self.calc_coh_force(prey)
            self.coh = map (mul, self.coh, (coh_weight, coh_weight))

            self.obs = self.calc_obs_force(obstacles, r)
            self.obs = map (mul, self.obs, (obs_weight,obs_weight))

            self.velocity = map(add, self.velocity, self.sep)
            self.velocity = map(add, self.velocity, self.coh)
            self.velocity = map(add, self.velocity, self.obs)

            #self.velocity = norm_vec(self.velocity)

            if self.velocity[0] > max_velo_p:
                self.velocity[0] = max_velo_p
            elif self.velocity[0] < max_velo_p*(-1):
                self.velocity[0] = max_velo_p*(-1)
            if self.velocity[1] > max_velo_p:
                self.velocity[1] = max_velo_p
            elif self.velocity[1] < max_velo_p*(-1):
                self.velocity[1] = max_velo_p*(-1)

            self.position.x += self.velocity[0]
            self.position.y += self.velocity[1]
            if self.position.x + boid_radius < 0:
                self.position.x = x_max + boid_radius
                self.redraw = 1
            if self.position.x - boid_radius > x_max:
                self.position.x = 0 - boid_radius
                self.redraw = 1
            if self.position.y + boid_radius < 0:
                self.position.y = y_max + boid_radius
                self.redraw = 1
            if self.position.y -boid_radius > y_max:
                self.position.y = 0 - boid_radius
                self.redraw = 1

#distance of two Point instances
def dist(a,b):
    x = pow(a.getX() - b.getX(),2)
    y = pow(a.getY() - b.getY(),2)
    return sqrt(x+y)

#distance vector between two Point instances
def dist_vec(a,b):
    x = a.getX() - b.getX()
    y = a.getY() - b.getY()
    return (x,y)

#normalize 2D vector
def norm_vec(v):
    norm = sqrt(pow(v[0],2) + pow(v[1],2))
    if norm == 0:
        return v
    return (v[0] / norm, v[1] / norm)

#adds a random obstacle
def add_obs():
    obstacles.append(Obstacle(Point(randint(0,x_max),randint(0,y_max)),randint(3,15)))

#removes all obstacles
def rem_obs():
    for o in obstacles:
        o.circle.undraw()
    del obstacles[:]

#adds a random predator
def add_pred():
    p = Predator(Point(randint(0,x_max),randint(0,y_max)))
    p.circle = Circle(p.position, boid_radius)
    p.circle.setFill("Red")
    p.circle.draw(win)
    p.line = Line(p.position, 
                 Point(p.position.getX() + p.velocity[0], 
                 p.position.getY() + p.velocity[1]))
    p.line.setWidth(1)
    p.line.draw(win)
    predators.append(p)

#removes all predators
def rem_pred():
    for o in predators:
        o.circle.undraw()
        o.line.undraw()
    del predators[:]

#compute angle between 2 2D vectors
def angle(a,b):
    if a == [0,0] or b == (0,0):
        return 3
    z = a[0] * b[0] + a[1] * b[1]
    n = sqrt(pow(a[0],2) + pow(a[1],2)) * sqrt(pow(b[0],2) + pow(b[1],2))
    return acos(z/n)

#tells if i is in range of b's radius
def in_obs(i,o):
    x = i.position.getX()
    y = i.position.getY()
    x1 = o.position.getX()
    y1 = o.position.getY()
    r = o.radius + boid_radius

    if x < x1 + r and x > x1 - r and y > y1 - r and y < y1 + r:
        return TRUE
    return FALSE

def main():
    #number of boids
    b = 50

    boids = []
    seed()

    #create the boids
    for i in range(b):
         boids.append(Boid(Point(randint(0, x_max),randint(0,y_max))))
         boids[i].circle = Circle(boids[i].position, boid_radius)
         boids[i].circle.setFill("Green")
         boids[i].circle.draw(win)

         boids[i].line = Line(boids[i].position, 
                 Point(boids[i].position.getX() + boids[i].velocity[0], 
                 boids[i].position.getY() + boids[i].velocity[1]))
         boids[i].line.setWidth(1)
         boids[i].line.draw(win)

    #the scale window
    top = Tk()

    align_weight = DoubleVar()
    align_scale = Scale( top, variable = align_weight, from_=0, to_=20,
            resolution=0.01,
            orient=HORIZONTAL, length=500)
    align_scale.pack(anchor=CENTER)
    align_scale.set(0.1)
    
    align_label = Label(top, text="align weight", relief=RAISED )
    align_label.pack(anchor=CENTER)

    sep_weight = DoubleVar()
    sep_scale = Scale( top, variable = sep_weight, from_=0, to_=20, resolution=0.1,
            orient=HORIZONTAL, length=500)
    sep_scale.pack(anchor=CENTER)
    sep_scale.set(0.3)
    
    sep_label = Label(top, text="separation weight", relief=RAISED )
    sep_label.pack(anchor=CENTER)

    coh_weight = DoubleVar()
    coh_scale = Scale( top, variable = coh_weight, from_=0, to_=20, resolution=0.1,
            orient=HORIZONTAL, length=500)
    coh_scale.pack(anchor=CENTER)
    coh_scale.set(2)

    coh_label = Label(top, text="cohesion weight", relief=RAISED )
    coh_label.pack(anchor=CENTER)

    obs_weight = DoubleVar()
    obs_scale = Scale( top, variable = obs_weight, from_=0, to_=20, resolution=0.01,
            orient=HORIZONTAL, length=500)
    obs_scale.pack(anchor=CENTER)
    obs_scale.set(0.39)

    obs_label = Label(top, text="obstacle avoidance weight", relief=RAISED )
    obs_label.pack(anchor=CENTER)

    fear_weight = DoubleVar()
    fear_scale = Scale( top, variable = fear_weight, from_=0, to_=20, resolution=0.1,
            orient=HORIZONTAL, length=500)
    fear_scale.pack(anchor=CENTER)
    fear_scale.set(20)

    fear_label = Label(top, text="fear for predators weight", relief=RAISED )
    fear_label.pack(anchor=CENTER)

    r_weight = IntVar()
    r_scale = Scale( top, variable = r_weight, from_=0, to_=1000, resolution=1,
            orient=HORIZONTAL, length=500)
    r_scale.pack(anchor=CENTER)
    r_scale.set(49)

    r_label = Label(top, text="neighbor radius", relief=RAISED )
    r_label.pack(anchor=CENTER)

    #predator scales
    pred_sep_weight = DoubleVar()
    pred_sep_scale = Scale( top, variable = pred_sep_weight, from_=0, to_=20,
            resolution=0.01,
            orient=HORIZONTAL, length=500)
    pred_sep_scale.pack(anchor=CENTER)
    pred_sep_scale.set(8.33)
    
    pred_sep_label = Label(top, text="predator separation weight", relief=RAISED )
    pred_sep_label.pack(anchor=CENTER)

    pred_hunt_weight = DoubleVar()
    pred_hunt_scale = Scale( top, variable = pred_hunt_weight, from_=0, to_=20, resolution=0.1,
            orient=HORIZONTAL, length=500)
    pred_hunt_scale.pack(anchor=CENTER)
    pred_hunt_scale.set(20)
    
    pred_hunt_label = Label(top, text="predator hunting weight", relief=RAISED )
    pred_hunt_label.pack(anchor=CENTER)

    pred_obs_weight = DoubleVar()
    pred_obs_scale = Scale( top, variable = pred_obs_weight, from_=0, to_=20, resolution=0.1,
            orient=HORIZONTAL, length=500)
    pred_obs_scale.pack(anchor=CENTER)
    pred_obs_scale.set(2.3)
    
    pred_obs_label = Label(top, text="predator obstacle avoidance weight", relief=RAISED )
    pred_obs_label.pack(anchor=CENTER)

    pred_r = DoubleVar()
    pred_r_scale = Scale( top, variable = pred_r, from_=0, to_=1000, resolution=1,
            orient=HORIZONTAL, length=500)
    pred_r_scale.pack(anchor=CENTER)
    pred_r_scale.set(100)
    
    pred_r_label = Label(top, text="predator radius", relief=RAISED )
    pred_r_label.pack(anchor=CENTER)

    pred_btn = Button(top, text="Add predator", command=add_pred)
    pred_btn.pack(side=LEFT)

    rpred_btn = Button(top, text="Remove predators", command=rem_pred)
    rpred_btn.pack(side=RIGHT)

    obs_btn = Button(top, text="Add obstacle", command=add_obs)
    obs_btn.pack(side=LEFT)

    robs_btn = Button(top, text="Remove obstacles", command=rem_obs)
    robs_btn.pack(side=RIGHT)

    #main loop
    while 1:
        for i in boids:
            neighbors = []
            hunters = []
            near_obstacles = []

            #find neighbors
            for j in boids:
                if j != i and dist(i.position, j.position) < r_scale.get():
                    neighbors.append(j)

            #find obstacles that are in the boids way
            for o in obstacles:
                if dist(i.position, o.position) < r_scale.get()\
                        and (angle(i.velocity, dist_vec(o.position,i.position))
                                 < atan((o.radius+boid_radius)/dist(o.position,i.position)) or in_obs(i,o)):
                    near_obstacles.append(o)

            #find nearby predators
            for h in predators:
                if dist(i.position, h.position) < r_scale.get():
                    hunters.append(h)

            #update the boids velocity and position
            i.updateBoid(sep_scale.get(), align_scale.get(),
                    coh_scale.get(), neighbors, r_scale.get(), near_obstacles,
                    obs_scale.get(), hunters, fear_scale.get())

            #update graphics
            i.line.undraw()
            i.line = Line(i.position,
                 Point(i.position.getX() + 10 * i.velocity[0],
                 i.position.getY() + 10 * i.velocity[1]))
            i.line.setWidth(1)
            i.line.draw(win)
            if i.redraw:
                i.circle.undraw()
                i.circle = Circle(i.position, boid_radius)
                i.circle.setFill('Green')
                i.circle.draw(win)
                i.redraw = 0
            else:
                i.circle.move(i.velocity[0], i.velocity[1])

        #update predators
        for p in predators:
            neighbors = []
            prey = []
            near_obstacles = []

            #find predator neighbors
            for n in predators:
                if dist(p.position, n.position) < pred_r_scale.get():
                    neighbors.append(n)

            #find prey
            for b in boids:
                if dist(p.position, b.position) < pred_r_scale.get():
                    prey.append(b)

            #detect obstacles that block the way
            for o in obstacles:
                if dist(p.position, o.position) < pred_r_scale.get():
                    near_obstacles.append(o)

            #update velocity and position
            p.updatePred (pred_sep_scale.get(), pred_hunt_scale.get(),
                    neighbors,
                pred_r_scale.get(), near_obstacles, pred_obs_scale.get(), prey)

            #update graphics
            p.line.undraw()
            p.line = Line(p.position, 
                 Point(p.position.getX() + 10 * p.velocity[0], 
                 p.position.getY() + 10 * p.velocity[1]))
            p.line.setWidth(1)
            p.line.draw(win)
            if p.redraw:
                p.circle.undraw()
                p.circle = Circle(p.position, boid_radius)
                p.circle.setFill('Red')
                p.circle.draw(win)
                p.redraw = 0
            else:
                p.circle.move(p.velocity[0], p.velocity[1])
        #time.sleep(0.0001)


main()
