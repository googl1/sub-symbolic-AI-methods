import Tkinter as tk
from ttk import *
import array
from random import *
from operator import attrgetter
import copy
import math
from statistics import *
from bitstring import BitArray
#import matplotlib.pyplot as plt

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
        seed()
        root = tk.Tk()
        root.title("Evolutionary Algorithm")

        self.mainframe = Frame(root)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        Button(self.mainframe, text="Start", command=self.start).grid(column=3, row=8, sticky=tk.W)

        Label(self.mainframe, text="crossover ratio (vs. copy):").grid(column=0, row=7)
        self.crossovervar = tk.DoubleVar()
        self.crossoverSlider = tk.Scale(self.mainframe, from_=0, to=1, resolution=0.02, orient=tk.HORIZONTAL)
        self.crossoverSlider.grid(column=1, row=7)
        self.crossoverSlider.set(0.5)

        Label(self.mainframe, text="mutation ratio:").grid(column=2, row=7)
        self.mutationvar = tk.DoubleVar()
        self.mutationSlider = tk.Scale(self.mainframe, from_=0, to=1, resolution=0.02, orient=tk.HORIZONTAL)
        self.mutationSlider.grid(column=3, row=7)
        self.mutationSlider.set(0.5)

        self.problemvar = tk.StringVar()
        self.problemChooser = Combobox(self.mainframe, textvariable=self.problemvar, state='readonly')
        self.problemChooser.grid(row=0, column=0)
        self.problemChooser['values'] = ('One-Max Problem', 'LOLZ Prefix Problem', 'Surprising Sequences')
        self.problemChooser.bind('<<ComboboxSelected>>', self.problemChanged)
        self.problemChooser.set('Surprising Sequences')

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
        self.selectionChooser.set('Generational Mixing')

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
        self.popEntry.insert(0, '100')

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
        self.e_slider.set(0.5)
        self.e_slider.grid(column=1, row=5)
        #self.e_slider.config(state=tk.DISABLED)

        Label(self.mainframe, text="K: ").grid(column=2, row=5)
        self.kvar = tk.IntVar()
        self.k_entry = tk.Entry( self.mainframe, textvariable=self.kvar)
        self.k_entry.grid(row=5, column=3)
        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, '10')
        #self.k_entry.config(state=tk.DISABLED)


        Label(self.mainframe, text="number of children:").grid(column=0, row=3)
        self.childvar = tk.IntVar()
        self.childChooser = Entry(self.mainframe, textvariable=self.childvar)
        self.childChooser.grid(row=3, column=1)
        self.childChooser.delete(0, tk.END)
        self.childChooser.insert(0, '100')
        #self.childChooser.config(state=tk.DISABLED)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        root.bind('<Return>', self.start)

        root.mainloop()

    def start(self, *args):
        if self.selectionChooser.get() == 'Full Generational Replacement':
            childs = int(self.popEntry.get())
        else:
            childs = int(self.childChooser.get())

        population = Population(int(self.popEntry.get()), int(self.lengthChooser.get()), childs, int(self.zEntry.get()),
                                int(self.lChooser.get()), int(self.sChooser.get()), self.problemChooser.get())
        population.log_init()
        while 1:
            population.fitness(self.problemChooser.get(), self.globlocChooser.get())
            population.adult_selection(self.selectionChooser.get())
            population.log()
            if population.best.fitness == 1:
                break
            population.parent_selection(self.parent_selChooser.get(), self.k_entry.get(), self.e_slider.get())
            population.make_love(float(self.mutationSlider.get()), float(self.crossoverSlider.get()))
   #     plt.plot(population.log_best_fitness)
    #    plt.ylabel('best fitness')
     #   plt.xlabel('round')
      #  plt.show()

      #  plt.plot(population.log_avg)
      #  plt.ylabel('average fitness')
      #  plt.xlabel('round')
      #  plt.show()

       # plt.plot(population.log_sd)
       # plt.ylabel('SD of fitness')
       # plt.xlabel('round')
       # plt.show()

class Creature:
    def __init__(self, l):
        self.len = l

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

    def set_genotype(self, g):
        self.genotype = g

    def fitness_fun(self, problem, z, d):
        if problem == 'One-Max Problem':
            self.fitness_count_ones()
        if problem == 'LOLZ Prefix Problem':
            self.fitness_lolz(z)
        if problem == 'Surprising Sequences':
            self.fitness_surprising(d)

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

class Population:
    #creates a set of n random genotypes of size l
    def __init__(self, n, len, childs, z, l, s, prob):
        self.size = n
        self.z = int(z)
        if prob == 'Surprising Sequences':
            self.length = int(math.ceil(math.log(s, 2)))
            self.length *= int(l)
        else:
            self.length = len
            s = 0
        self.children = []
        self.num_childs = childs
        for c in range(childs):
            new_c = Creature(self.length)
            new_c.generate_genotype(s,l)
            self.children.append(new_c)
        self.adults = []
        self.round = 0

    def make_love(self, mutation_rate, crossover_rate):
        self.children = []
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
            c.fitness_fun(problem, self.z, d)

    def roulette(self):
        roulette = []
        parents = []
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
        k = int(_k)
        if k > self.size:
            k = self.size

        #randomly choose method
        r = uniform(0,1)

        parents = []
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
            a.scaling = a.scaling / avg
        return

    def rank_selection(self):
        #sort population
        self.adults.sort(cmp, key=attrgetter('fitness'))

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