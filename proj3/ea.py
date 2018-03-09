import Tkinter as tk
from ttk import *
import array
from random import *
from operator import attrgetter, add
import copy
import math
from statistics import *
from bitstring import BitArray
import graphics
import time
import matplotlib.pyplot as plt

class GUI:
    def problemChanged(self, event):
        self.problemvar = self.problemChooser.get()
        if self.problemvar != "LOLZ Prefix Problem":
            self.zEntry.config(state=tk.DISABLED)
        else:
            self.zEntry.config(state=tk.NORMAL)
        if self.problemvar != 'Surprising Sequences':
            self.sChooser.config(state=tk.DISABLED)
            self.lChooser.config(state=tk.DISABLED)
        else:
            self.sChooser.config(state=tk.NORMAL)
            self.lChooser.config(state=tk.NORMAL)

        return

    def selectionChanged(self, event):
        self.selectionvar = self.selectionChooser.get()
        if self.selectionvar == 'Full Generational Replacement':
            self.childChooser.config(state=tk.DISABLED)
        else:
            self.childChooser.config(state=tk.NORMAL)
        return

    def globloc_selection_changed(self, event):
        self.globlocvar = self.globlocChooser.get()
        return

    def parent_selection_changed(self, event):
        self.parent_selvar = self.parent_selChooser.get()
        if self.parent_selvar == 'Tournament selection':
            self.e_slider.config(state=tk.NORMAL)
            self.k_entry.config(state=tk.NORMAL)
        else:
            self.e_slider.config(state=tk.DISABLED)
            self.k_entry.config(state=tk.DISABLED)
        return

    def __init__(self):
        self.run = True
        seed()
        self.root = tk.Tk()
        self.root.title("Evolutionary Algorithm")

        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        Button(self.mainframe, text="Start", command=self.start).grid(column=3, row=11, sticky=tk.W)

        Label(self.mainframe, text="crossover ratio (vs. copy):").grid(column=0, row=9)
        self.crossovervar = tk.DoubleVar()
        self.crossoverSlider = tk.Scale(self.mainframe, from_=0, to=1, resolution=0.02, orient=tk.HORIZONTAL)
        self.crossoverSlider.grid(column=1, row=9)
        self.crossoverSlider.set(0.58)

        Label(self.mainframe, text="mutation ratio:").grid(column=2, row=9)
        self.mutationvar = tk.DoubleVar()
        self.mutationSlider = tk.Scale(self.mainframe, from_=0, to=1, resolution=0.02, orient=tk.HORIZONTAL)
        self.mutationSlider.grid(column=3, row=9)
        self.mutationSlider.set(0.6)

        self.problemvar = tk.StringVar()
        self.problemChooser = Combobox(self.mainframe, textvariable=self.problemvar, state='readonly')
        self.problemChooser.grid(row=0, column=0)
        self.problemChooser['values'] = ('One-Max Problem', 'LOLZ Prefix Problem', 'Surprising Sequences', 'ENN')
        self.problemChooser.bind('<<ComboboxSelected>>', self.problemChanged)
        self.problemChooser.set('ENN')

        Label(self.mainframe, text="z:").grid(column=2, row=1)
        self.zvar = tk.IntVar()
        self.zEntry = Entry(self.mainframe, textvariable=self.zvar)
        self.zEntry.grid(row=1, column=3)
        self.zEntry.delete(0, tk.END)
        self.zEntry.insert(0, '5')

        Label(self.mainframe, text="genotype length:").grid(column=0, row=1)
        self.lengthvar = tk.IntVar()
        self.lengthChooser = Entry(self.mainframe, textvariable=self.lengthvar)
        self.lengthChooser.grid(row=1, column=1)
        self.lengthChooser.delete(0, tk.END)
        self.lengthChooser.insert(0, '10')

        Label(self.mainframe, text="adult selection: ").grid(column=0, row=2)
        self.selectionvar = tk.StringVar()
        self.selectionChooser = Combobox(self.mainframe, textvariable=self.selectionvar, state='readonly')
        self.selectionChooser.grid(row=2, column=1)
        self.selectionChooser['values'] = ('Full Generational Replacement', 'Over-production', 'Generational Mixing')
        self.selectionChooser.bind('<<ComboboxSelected>>', self.selectionChanged)
        self.selectionChooser.set('Over-production')

        Label(self.mainframe, text="S:").grid(column=2, row=2)
        self.svar = tk.IntVar()
        self.sChooser = Entry(self.mainframe, textvariable=self.svar)
        self.sChooser.grid(row=2, column=3)
        self.sChooser.delete(0, tk.END)
        self.sChooser.insert(0, '4')

        Label(self.mainframe, text="L:").grid(column=2, row=3)
        self.lvar = tk.IntVar()
        self.lChooser = Entry(self.mainframe, textvariable=self.lvar)
        self.lChooser.grid(row=3, column=3)
        self.lChooser.delete(0, tk.END)
        self.lChooser.insert(0, '20')

        self.globlocvar = tk.StringVar()
        self.globlocChooser = Combobox(self.mainframe, textvariable=self.globlocvar, state='readonly', width=24)
        self.globlocChooser.grid(row=4, column=3)
        self.globlocChooser['values'] = ('Globally surprising sequences', 'Locally surprising sequences')
        self.globlocChooser.bind('<<ComboboxSelected>>', self.globloc_selection_changed)
        self.globlocChooser.set('Globally surprising sequences')

        Label(self.mainframe, text="population size:").grid(column=1, row=0)
        self.popvar = tk.IntVar()
        self.popEntry = Entry(self.mainframe, textvariable=self.popvar)
        self.popEntry.grid(row=0, column=3)
        self.popEntry.delete(0, tk.END)
        self.popEntry.insert(0, '800')

        Label(self.mainframe, text="parent selection: ").grid(column=0, row=4)
        self.parent_selvar = tk.StringVar()
        self.parent_selChooser = Combobox(self.mainframe, textvariable=self.parent_selvar, state='readonly')
        self.parent_selChooser.grid(row=4, column=1)
        self.parent_selChooser['values'] = ('Fitness-proportionate', 'Sigma-scaling', 'Tournament selection', 'Rank selection')
        self.parent_selChooser.bind('<<ComboboxSelected>>', self.parent_selection_changed)
        self.parent_selChooser.set('Tournament selection')

        Label(self.mainframe, text="e: ").grid(column=0, row=5)
        self.evar = tk.DoubleVar()
        self.e_slider = tk.Scale( self.mainframe, resolution=0.01, from_=0, to_=1,       orient=tk.HORIZONTAL)
        self.e_slider.set(0.66)
        self.e_slider.grid(column=1, row=5)
        #self.e_slider.config(state=tk.DISABLED)

        Label(self.mainframe, text="K: ").grid(column=2, row=5)
        self.kvar = tk.IntVar()
        self.k_entry = tk.Entry( self.mainframe, textvariable=self.kvar)
        self.k_entry.grid(row=5, column=3)
        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, '10')
        #self.k_entry.config(state=tk.DISABLED)

        Label(self.mainframe, text="layers: ").grid(column=0, row=6)
        self.layersvar = tk.IntVar()
        self.layers_entry = tk.Entry( self.mainframe, textvariable=self.layersvar)
        self.layers_entry.grid(row=6, column=1)
        self.layers_entry.delete(0, tk.END)
        self.layers_entry.insert(0, '0')

        Label(self.mainframe, text="neurons per layer: ").grid(column=2, row=6)
        self.neuronsvar = tk.IntVar()
        self.neurons_entry = tk.Entry( self.mainframe, textvariable=self.neuronsvar)
        self.neurons_entry.grid(row=6, column=3)
        self.neurons_entry.delete(0, tk.END)
        self.neurons_entry.insert(0, '0')

        Label(self.mainframe, text="weight accuracy: ").grid(column=0, row=7)
        self.accvar = tk.IntVar()
        self.acc_entry = tk.Entry( self.mainframe, textvariable=self.accvar)
        self.acc_entry.grid(row=7, column=1)
        self.acc_entry.delete(0, tk.END)
        self.acc_entry.insert(0, '8')

        Label(self.mainframe, text="scenario: ").grid(column=2, row=7)
        self.scenvar = tk.StringVar()
        self.scenChooser = Combobox( self.mainframe, textvariable=self.scenvar, state='readonly')
        self.scenChooser.grid(row=7, column=3)
        self.scenChooser['values'] = ('dynamic', 'static')
        self.scenChooser.bind('<<ComboboxSelected>>', self.parent_selection_changed)
        self.scenChooser.set('static')

        Label(self.mainframe, text="number of children:").grid(column=0, row=3)
        self.childvar = tk.IntVar()
        self.childChooser = Entry(self.mainframe, textvariable=self.childvar)
        self.childChooser.grid(row=3, column=1)
        self.childChooser.delete(0, tk.END)
        self.childChooser.insert(0, '1600')
        #self.childChooser.config(state=tk.DISABLED)

        Label(self.mainframe, text="threshold:").grid(column=0, row=8)
        self.thresholdvar = tk.IntVar()
        self.threshold_entry = Entry(self.mainframe, textvariable=self.thresholdvar)
        self.threshold_entry.grid(row=8, column=1)
        self.threshold_entry.delete(0, tk.END)
        self.threshold_entry.insert(0, '0.2')

        Label(self.mainframe, text="direct copies:").grid(column=2, row=8)
        self.elitismvar = tk.IntVar()
        self.elitism_entry = Entry(self.mainframe, textvariable=self.elitismvar)
        self.elitism_entry.grid(row=8, column=3)
        self.elitism_entry.delete(0, tk.END)
        self.elitism_entry.insert(0, '1')

        Label(self.mainframe, text="visualization: ").grid(column=0, row=10)
        self.visualvar = tk.StringVar()
        self.visChooser = Combobox( self.mainframe, textvariable=self.visualvar, state='readonly')
        self.visChooser.grid(row=10, column=1)
        self.visChooser['values'] = ('yes', 'no')
        self.visChooser.set('no')

        Label(self.mainframe, text="max generations:").grid(column=2, row=10)
        self.genvar = tk.IntVar()
        self.gen_entry = Entry(self.mainframe, textvariable=self.genvar)
        self.gen_entry.grid(row=10, column=3)
        self.gen_entry.delete(0, tk.END)
        self.gen_entry.insert(0, '50')

        Label(self.mainframe, text="testset size:").grid(column=0, row=11)
        self.setvar = tk.IntVar()
        self.set_entry = Entry(self.mainframe, textvariable=self.setvar)
        self.set_entry.grid(row=11, column=1)
        self.set_entry.delete(0, tk.END)
        self.set_entry.insert(0, '5')

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.root.bind('<Return>', self.start)

        self.root.mainloop()

    def start(self, *args):
        if self.selectionChooser.get() == 'Full Generational Replacement':
            childs = int(self.popEntry.get())
        else:
            childs = int(self.childChooser.get())

        self.population = Population(int(self.popEntry.get()), int(self.lengthChooser.get()), childs, int(self.zEntry.get()),
                                int(self.lChooser.get()), int(self.sChooser.get()), self.problemChooser.get(),
                                int(self.neurons_entry.get()), int(self.layers_entry.get()), int(self.acc_entry.get()),
                                self.scenChooser.get(), float(self.threshold_entry.get()), int(self.elitism_entry.get()))
        self.population.log_init()
        self.population.set_new_scenario(int(self.set_entry.get()))
        generation_counter = 0
        while 1:
            #generate scenario
            if self.scenChooser.get() == 'dynamic':
                self.population.set_new_scenario(int(self.set_entry.get()))
            self.population.fitness(self.problemChooser.get(), self.globlocChooser.get())
            self.population.adult_selection(self.selectionChooser.get())
            self.population.log()

            if self.population.best.fitness == 1 or generation_counter == int(self.gen_entry.get()) - 1:
                break
            generation_counter += 1
            self.population.parent_selection(self.parent_selChooser.get(), self.k_entry.get(), self.e_slider.get())
            #self.population.adults.sort(key=attrgetter('fitness'), reverse=True)
            self.population.make_love(float(self.mutationSlider.get()), float(self.crossoverSlider.get()))

        if self.visChooser.get() == "no":
            self.quit()
            return

        f, axarr = plt.subplots(3, sharex=True)
        axarr[0].plot(self.population.log_best_fitness)
        axarr[0].set_title('best fitness', fontsize=12)
        axarr[1].plot(self.population.log_avg)
        axarr[1].set_title('average fitness', fontsize=12)
        axarr[2].plot(self.population.log_sd)
        axarr[2].set_title('standard deviation of fitness', fontsize=12)

        # bf = plt.subplot()
        # af = plt.subplot()
        # sdf = plt.subplot()
        #
        # bf = plt.plot(self.population.log_best_fitness)
        # #bf.ylabel('best fitness')
        # #bf.xlabel('round')
        # #plt.show()
        #
        # af = plt.plot(self.population.log_avg)
        # #af.ylabel('average fitness')
        # #af.xlabel('round')
        # #plt.show()
        #
        # sdf = plt.plot(self.population.log_sd)
        # #sdf.ylabel('SD of fitness')
        # #sdf.xlabel('round')

        # visualize
        self.playwin = tk.Tk()
        self.playwin.title("Control Visualization")
        playframe = Frame(self.playwin)
        playframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        playframe.columnconfigure(0, weight=1)
        playframe.rowconfigure(0, weight=1)
        Button(playframe, text="Generate random flatland", command=self.random_visualization).grid(column=0, row=0, sticky=tk.W)
        Button(playframe, text="Quit", command=self.quit).grid(column=1, row=0, sticky=tk.W)

        Label(playframe, text="speed: ").grid(column=0, row=1)
        speed_slider = tk.Scale(playframe, resolution=0.1, from_=0.1, to_=1, orient=tk.HORIZONTAL)
        speed_slider.set(0.1)
        speed_slider.grid(column=1, row=1)


        while (self.run):
            if self.scenChooser.get() == 'dynamic':
                self.population.set_new_scenario(1)
            for s in self.population.scenarios:
                s.speed = speed_slider.get()
            self.population.best.fitness_fun(self.problemChooser.get(), self.population.z, True, self.population.scenarios, True)

        plt.show()


    def quit(self):
        print "Quit"
        self.root.destroy()
        try:
            self.playwin.destroy()
            self.playwin.quit()
        except:
            pass
        self.root.quit()
        self.run = False
        return

    def random_visualization(self):
        self.population.scenarios = list()
        self.population.scenarios.append(Flatland(True))
        #self.population.best.fitness_fun(self.problemChooser.get(), self.population.z, True, self.population.scenarios, True)

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

    def generate_genotype(self, s, l):
        self.s = s
        self.l = l
        self.genotype = array.array('B', [0] * self.len)
        self.phenotype = [None] * l
        for i in range(self.len):
            self.genotype[i] = randint(0,1)
        self.generate_phenotype(s,l)

    def set_genotype2(self, g, s, l):
        self.genotype = g
        self.l = l
        self.s = s
        self.phenotype = [None] * self.l
        self.generate_phenotype(self.s,self.l)

    def set_genotype(self, g):
        self.genotype = g

    def fitness_fun(self, problem, z, d, scenarios, draw_it):
        if problem == 'One-Max Problem':
            self.fitness_count_ones()
        if problem == 'LOLZ Prefix Problem':
            self.fitness_lolz(z)
        if problem == 'Surprising Sequences':
            self.fitness_surprising(d)
        if problem == 'ENN':
            self.fitness_flatland(scenarios, draw_it)

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


class Population:
    #creates a set of n random genotypes of size l
    def __init__(self, n, len, childs, z, l, s, prob, neurons, layers, weight_acc, scenario, threshold, elitism_copies):
        self.size = n
        self.z = int(z)
        self.elitism_copies = elitism_copies
        if prob == 'Surprising Sequences':
            self.length = int(math.ceil(math.log(s, 2)))
            self.length *= int(l)
        elif prob == 'ENN':
            if neurons == 0 or layers == 0:
                # connections from input to output layer
                # + connections from bias neuron to output layer
                l = 7 * 3
            else:
                # connections from inputs to first layer
                # connections between layers
                # connections from last layer to outputs
                # bias neuron in input layer
                l = 6 * neurons \
                    + (layers - 1) * neurons * neurons \
                    + 3 * neurons \
                    + neurons
            self.length = l * weight_acc
            s = pow(2,weight_acc)
        else:
            self.length = len
            s = 0
        self.children = []
        self.num_childs = childs
        for c in range(childs):
            new_c = Creature(self.length, layers, neurons, weight_acc, scenario, threshold)
            # if prob == 'ENN':
            #     g = array.array('B', [0] * l*s)
            #     for i in range(1,l+1):
            #         g[8 * i -1] = 1
            #     new_c.set_genotype2(g, s, l)
            #else:
            new_c.generate_genotype(s,l)
            self.children.append(new_c)
        self.adults = []
        self.round = 0

    def set_new_scenario(self, set_size):
        self.scenarios = [None] * set_size
        for s in range(set_size):
            self.scenarios[s] = Flatland(False)

    def make_love(self, mutation_rate, crossover_rate):
        self.children = []
        self.adults.sort(key=attrgetter('fitness'), reverse=True)
        for i in range(self.elitism_copies):
            self.adults.sort(key=attrgetter('fitness'), reverse=True)
            self.children.append(copy.deepcopy(self.adults[i]))
        for a in self.adults:
            r = uniform(0,1)
            if r < crossover_rate: #crossover
                self.children.append(copy.deepcopy(a))
                r = randint(0, self.size - 1)
                self.children[len(self.children) - 1].crossover(self.adults[r])
            else: #copy a
                self.children.append(copy.deepcopy(a))
            r = uniform(0,1)
            if r < mutation_rate: #mutate
                self.children[len(self.children) - 1].mutate()

    def full_generation_replacement(self):
        self.adults = self.children[:]
        self.adults.sort(key=attrgetter('fitness'), reverse=True)

    def over_production(self):
        self.adults = self.children[:]
        self.children = []
        temp_pop = self.adults[:]
        temp_pop.sort(key=attrgetter('fitness'), reverse=True)
        self.adults = temp_pop[:self.size]
        return

    def generational_mixing(self):
        self.adults.extend(self.children)
        self.children = []
        temp_pop = self.adults[:]
        temp_pop.sort(key=attrgetter('fitness'), reverse=True)
        self.adults = temp_pop[:self.size]
        return

    def adult_selection(self, selection):
        if selection == 'Full Generational Replacement':
            self.full_generation_replacement()
        if selection == 'Over-production':
            self.over_production()
        if selection == 'Generational Mixing':
            self.generational_mixing()

    def fitness(self, problem, globloc):
        if globloc == 'Globally surprising sequences':
            d = True
        else:
            d = False
        for c in self.children:
            c.fitness_fun(problem, self.z, d, self.scenarios, False)

    def roulette(self):
        roulette = []
        parents = []

        # elitism copies
        for i in range(self.elitism_copies):
            parents.append(copy.deepcopy(self.adults[i]))

        #set accumulated probabilities
        roulette.append(self.adults[0].scaling)
        for i in range(1,self.size):
            roulette.append(roulette[i-1] + self.adults[i].scaling)

        #fix rounding error
        roulette[len(roulette)-1] = 1.0

        #spin the wheel
        while len(parents) < self.size:
            r = uniform(0,1)
            i = 0
            while r > roulette[i]:
                i += 1
            parents.append(copy.deepcopy(self.adults[i]))
        self.adults = parents[:]

    def fitness_proportionate(self):
        avg = 0.0
        for a in self.adults:
            avg += a.fitness
        for a in self.adults:
            if avg == 0:
                a.scaling = 0
            else:
                a.scaling = a.fitness / avg
        self.roulette()
        return

    def sigma_scaling(self):
        avg = 0.0
        for a in self.adults:
            avg += a.fitness
        avg /= self.size

        #calc std deviation
        std_deviation = pstdev([i.fitness for i in self.adults[:]])

        #set probabailities
        for a in self.adults:
            if std_deviation == 0:
                a.scaling = 1.0
            else:
                a.scaling = ((1.0 + ((a.fitness - avg) / (2*std_deviation))) / self.size)
        self.roulette()

    def tournament_selection(self, _k, e):
        parents = []

        for i in range(self.elitism_copies):
            #self.adults.sort(key=attrgetter('fitness'), reverse=True)
            parents.append(copy.deepcopy(self.adults[i]))
        k = int(_k)
        if k > self.size:
            k = self.size

        #randomly choose method
        r = uniform(0,1)

        tournament = []

        while len(parents) < self.size:
            #find k random participants
            tmp_adults = self.adults[:]
            tournament = []
            while len(tournament) < k:
                i = randint(0, len(tmp_adults) - 1)
                tournament.append(copy.deepcopy(tmp_adults.pop(i)))
            if r <= e:
                #random choice
                i = randint(0, len(tournament) - 1)
                parents.append(copy.deepcopy(tournament[i]))
            else:
                #choose best of random group of K parents
                parents.append(copy.deepcopy(max(tournament,key=attrgetter('fitness'))))

        self.adults = parents[:]
        return

    def normalize_scaling(self):
        avg = 0.0
        for a in self.adults:
            avg += a.scaling
        for a in self.adults:
            if avg == 0:
                a.scaling = 0
            else:
                a.scaling = a.scaling / avg
        return

    def rank_selection(self):
        #set probabilities
        for a in self.adults:
            a.scaling = self.adults[0].fitness + ((self.adults[len(self.adults) - 1].fitness - self.adults[0].fitness) * (float(self.adults.index(a))/(self.size - 1)))
        self.normalize_scaling()
        self.roulette()
        return

    def parent_selection(self, adult_sel_meth, k, e):
        if adult_sel_meth == 'Fitness-proportionate':
            self.fitness_proportionate()
        elif adult_sel_meth == 'Sigma-scaling':
            self.sigma_scaling()
        elif adult_sel_meth == 'Tournament selection':
            self.tournament_selection(k, e)
        elif adult_sel_meth == 'Rank selection':
            self.rank_selection()

    def log_init(self):
        print "#\tbest fitness\taverage fitness\tSD of fitness\tbest phenotype"
        print "------------------------------------------------------------------------"
        self.log_best_fitness = list()
        self.log_avg = list()
        self.log_sd = list()

    def log(self):
        self.round += 1
        self.best = self.adults[0]
        avg = 0.0
        for a in self.adults:
            if a.fitness > self.best.fitness:
                self.best = a
            avg += a.fitness

        avg /= self.size

        sd = pstdev([i.fitness for i in self.adults[:]])

        print "%d\t%f\t\t%f\t\t%f\t\t%s" % (self.round, self.best.fitness, avg, sd, ','.join(str(x) for x in self.best.phenotype))
        self.log_best_fitness.append(self.best.fitness)
        self.log_avg.append(avg)
        self.log_sd.append(sd)

GUI()