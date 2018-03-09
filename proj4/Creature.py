import math
from bitstring import BitArray
from random import *
import array
import copy
from Beer import *
from ctrnn import *

class Creature:
    def __init__(self, l, layers, neurons, weight_acc, scenario, threshold):
        self.len = l
        self.layers = layers
        self.neurons = neurons
        self.weight_acc = weight_acc
        self.scenario = scenario
        self.threshold = threshold

    def generate_phenotype(self, s, l):
        if s == 0:
            self.phenotype = self.genotype[:]
            return True
        len_s = int(math.ceil(math.log(s,2)))
        for i in range(0,l):
            b = BitArray(self.genotype[i*len_s:i*len_s+len_s])
            self.phenotype[i] = b.uint

            while self.phenotype[i] >= s:
                low = math.ceil(math.log(s,2))*i
                up = math.ceil(math.log(s,2))*(i+1) - 1
                self.genotype[randint(low,up)] = 0
                b = BitArray(self.genotype[i*len_s:i*len_s+len_s])
                self.phenotype[i] = b.uint

        return True

    def generate_genotype(self, s, l, prob):
        self.s = s
        self.l = l
        self.genotype = array.array('B', [0] * self.len)
        self.phenotype = [None] * l
        for i in range(self.len):
            self.genotype[i] = randint(0,1)
        if prob == 'CTRNN':
            self.generate_phenotype_ctrnn(s,l)
            return
        self.generate_phenotype(s,l)

    def generate_phenotype_ctrnn(self,s,l):
        len_s = int(math.ceil(math.log(s,2)))

        # 4 bias weights between -10 and 0
        num_bias = 4
        for i in range(num_bias):
            b = BitArray(self.genotype[i*len_s:i*len_s+len_s])
            val256 = b.uint
            self.phenotype[i] = val256 /256.0 * 10 * (-1)
        offset = num_bias
        bin_offset = offset * len_s

        if self.scenario == 'pull':
            # 22 + 8 weights between -5 and 5
            num_weights = 22 + 8
        elif self.scenario == 'no-wrap':
            num_weights = 22 + 4
        else:
            # 22 weights between -5 and 5
            num_weights = 22
        for i in range(num_weights):
            b = BitArray(self.genotype[bin_offset + i*len_s: bin_offset + i*len_s+len_s])
            val256 = b.uint
            #if self.scenario == 'no-wrap' and (i >:

            self.phenotype[i + offset] = (val256 /256.0 * 10) - 5
        offset += num_weights
        bin_offset = offset * len_s

        # 4 gains between 1 and 5
        num_gains = 4
        if self.scenario == 'pull':
            num_gains = 5
        for i in range(num_gains):
            b = BitArray(self.genotype[bin_offset + i*len_s: bin_offset + i*len_s+len_s])
            val256 = b.uint
            self.phenotype[i + offset] = (val256 /256.0 * 4) + 1
        offset += num_gains
        bin_offset = offset * len_s

        # 4 time constants between 1 and 2
        num_taus = 5
        if self.scenario == 'pull':
            num_taus += 1
        for i in range(num_taus):
            b = BitArray(self.genotype[bin_offset + i*len_s: bin_offset + i*len_s+len_s])
            val256 = b.uint
            self.phenotype[i + offset] = (val256 /256.0) + 1

    def set_genotype(self, g):
        self.genotype = g

    def fitness_fun(self, problem, z, d, scenarios, draw_it, speed):
        if problem == 'CTRNN':
            self.fitness_ctrnn(draw_it, speed)
        elif problem == 'One-Max Problem':
            self.fitness_count_ones()
        elif problem == 'LOLZ Prefix Problem':
            self.fitness_lolz(z)
        elif problem == 'Surprising Sequences':
            self.fitness_surprising(d)
        elif problem == 'ENN':
            self.fitness_flatland(scenarios, draw_it)
        else:
            print "error, non-existant problem"

    def activation(self, x, threshold):
        return self.activation_logistic(x, threshold, 64)

    def activation_identity(self, x):
        return x

    def activation_step(self, x, threshold):
        if x > threshold:
            return 1
        return 0

    def activation_logistic(self, x, threshold, steepness):
        return 1/ (1 + math.exp(- steepness * (x-threshold)))

    def fitness_ctrnn(self, draw_it, speed):
        score = 0
        no_wrap = (self.scenario == 'no-wrap')
        beer = Beer(draw_it, not no_wrap)
        timesteps = 600
        if self.scenario == 'standard':
            ctrnn = CTRNN(self.phenotype, False, False)
        elif self.scenario == 'pull':
            ctrnn = CTRNN(self.phenotype, True, False)
        elif no_wrap:
            ctrnn = CTRNN(self.phenotype, False, True)
        else:
            print "oooups, error in scenario chosen"

        for i in range(timesteps):
            motor = ctrnn.evaluate(beer.get_sensors())

            # map motor neuron output to movement
            movement = motor[1] * 4 - motor[0] * 4
            if self.scenario == 'pull':
                if motor[2] > motor[0] and motor[2] > motor[1]:
                    beer.pull()
                else:
                    beer.move(int(round(movement)))
            beer.move(int(round(movement)))

            self.fitness = beer.timestep(speed) / 200.0

        return self.fitness

    def fitness_flatland(self, flatlands, draw_it):
        score_sum = 0
        for flatland in flatlands:
            flatland.flatland = copy.deepcopy(flatland.backup)
            flatland.pos = (5,5)
            flatland.dir = (0, -1)
            score = 0
            if draw_it:
                flatland.init_draw()

            for i in range(60):
                forward = flatland.get_forward()
                right = flatland.get_right()
                left = flatland.get_left()

                food = [0] * 3
                poison = [0] * 3

                if forward == 1:
                    food[0] = 1
                elif forward == 2:
                    poison[0] = 1
                if left == 1:
                    food[1] = 1
                elif left == 2:
                    poison[1] = 1
                if right == 1:
                    food[2] = 1
                elif right == 2:
                    poison[2] = 1

                motor = self.evaluate_nn(food, poison)

                if motor != [0,0,0]:
                    flatland.set_new_pos(motor)

                    if flatland.flatland[flatland.pos[0]][flatland.pos[1]] == 1:
                        score += 1
                        flatland.flatland[flatland.pos[0]][flatland.pos[1]] = 0
                        if draw_it:
                            flatland.undraw_circle(flatland.pos[0], flatland.pos[1])
                    elif flatland.flatland[flatland.pos[0]][flatland.pos[1]] == 2:
                        score -= 2
                        flatland.flatland[flatland.pos[0]][flatland.pos[1]] = 0
                        if draw_it:
                            flatland.undraw_circle(flatland.pos[0], flatland.pos[1])

                if draw_it:
                    flatland.update_drawing()

            if score < 0:
                score = 0
            score /= float(flatland.foods)
            score_sum += score
            if draw_it:
                flatland.win.close()

        self.fitness = score_sum / len(flatlands)
        return score

    def evaluate_nn(self, food, poison):
            motor = [0] * 3
            if self.neurons != 0 and self.layers != 0:
                nn = [[0 for x in range(self.neurons)] for x in range(self.layers)]
                for n in range(self.neurons):
                    nn[0][n] += self.phenotype[len(self.phenotype) - 1 - n] # bias neuron
                    for c in range(3):
                        nn[0][n] += food[c] * self.phenotype[6 * n + c]
                    for c in range(3):
                        nn[0][n] += poison[c] * self.phenotype[6 * n + c + 3]
                    nn[0][n] /= pow(2, self.weight_acc) * 7.0
                    nn[0][n] = self.activation(nn[0][n], self.threshold)

                for l in range(1,len(nn)):
                    for n in range(self.neurons):
                        nn[l][n] = 0
                        for c in range(self.neurons):
                            nn[l][n] += nn[l-1][c] * self.phenotype[self.neurons * 6 + (l-1) * self.neurons * self.neurons + self.neurons * n + c]
                        nn[l][n] /= pow(2, self.weight_acc) * float(self.neurons)
                        nn[l][n] = self.activation(nn[l][n], self.threshold)

                for o in range(len(motor)):
                    motor[o] = 0
                    for c in range(self.neurons):
                        motor[o] += nn[self.layers - 1][c] * self.phenotype[self.neurons * 6 + (self.layers - 1) * self.neurons * self.neurons + o * self.neurons + c]
            else: #if no hidden layers
                for o in range(len(motor)):
                    motor[o] = 0
                    motor[o] += self.phenotype[len(self.phenotype) - 1 - o] # bias neuron
                    for c in range(3):
                        motor[o] += food[c] * self.phenotype[6 * o + c]
                    for c in range(3):
                        motor[o] += poison[c] * self.phenotype[6 * o + c + 3]
            return motor

    def fitness_surprising(self, d):
        sequences = list()
        fails = 0
        for i in range(len(self.phenotype)):
            if d:
                end = len(self.phenotype)
            else:
                end = min(i + 2, len(self.phenotype))
            for j in range(i+1, end):
                seq = (self.phenotype[i], self.phenotype[j], j-i-1)
                if seq in sequences:
                    fails += 1
                else:
                    sequences.append(seq)

        self.fitness = 1.0 / (1.0 + fails)
        return self.fitness

    def fitness_lolz(self,z_max):
        o = 0
        z = 0
        max_o = 0
        max_z = 0
        for i in range(self.len):
            if self.genotype[i] == 0:
                z += 1
                o = 0
                if z > max_z:
                    max_z = z
            else:
                o += 1
                z = 0
                if o > max_o:
                    max_o = o
        if max_z > z_max:
            max_z = z_max

        self.fitness = float(max(max_z, max_o))/self.len
        return self.fitness

    def fitness_count_ones(self):
        self.fitness = 0.0
        for i in range(self.len):
            self.fitness += self.genotype[i]
        self.fitness /= self.len

    def mutate(self):
        tmp_g_type = self.genotype[:]
        r = randint(0, self.len - 1)
        if self.genotype[r] == 1:
            self.genotype[r] = 0
        else:
            self.genotype[r] = 1
        while (not self.generate_phenotype(self.s, self.l)):
            self.genotype = tmp_g_type[:]
            r = randint(0, self.len - 1)
            if self.genotype[r] == 1:
                self.genotype[r] = 0
            else:
                self.genotype[r] = 1

    def crossover(self, partner):
        r = randint(0,1)
        if r == 0:
            self.single_point_crossover(partner)
            while not self.generate_phenotype(self.s, self.l):
                self.single_point_crossover(partner)
        else:
            self.two_point_crossover(partner)
            while not self.generate_phenotype(self.s, self.l):
                self.two_point_crossover(partner)


    def single_point_crossover(self, partner):
        r = randint(0,self.len)
        g = self.genotype[0:r]
        g.extend(partner.genotype[r:])
        self.genotype = g[:]

    def two_point_crossover(self, partner):
        r = randint(0,self.len - 1)
        r2 = randint(r, self.len)
        g = self.genotype[0:r]
        g.extend(partner.genotype[r:r2])
        g.extend(self.genotype[r2:])
        self.genotype = g[:]