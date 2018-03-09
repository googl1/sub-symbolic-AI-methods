import math

class CTRNN:
    def __init__(self, phenotype, pull, no_wrap):
        self.pull = pull
        self.no_wrap = no_wrap

        if pull:
            self.n = 5
        else:
            self.n = 4
        self.y = [0] * self.n
        if no_wrap:
            self.n_input = 7
        else:
            self.n_input = 5

        if pull:
            self.bias_weights = phenotype[0:5]
            self.weights = phenotype[5:34]
            self.gains = phenotype[34:39]
            self.time_constants = phenotype[39:44]
        elif no_wrap:
            self.bias_weights = phenotype[0:5]
            self.weights = phenotype[5:31]
            self.gains = phenotype[31:35]
            self.time_constants = phenotype[35:39]
        else:
            self.bias_weights = phenotype[0:5]
            self.weights = phenotype[5:27]
            self.gains = phenotype[27:31]
            self.time_constants = phenotype[31:35]
        self.outputs = [0] * self.n
        return

    def evaluate(self, inputs):
        self.inputs = inputs

        for i in range(self.n):
            self.update_y(i)
            self.outputs[i] = self.o(i)

        if self.pull:
            return self.outputs[2:5]
        else:
            return self.outputs[2:4]


    def s(self, i):
        s = 0
        if i < 2:
            inputs = 2
            s += self.get_inputs(i)
        else:
            inputs = self.n
        for j in range(inputs):
            s += self.o(j) * self.w(i,j)
        return s

    def get_inputs(self, i):
        if i > 1:
            return 0
        inputs = 0
        for j in range (self.n_input):
            inputs += self.inputs[j] * self.input_weight(j*(i+1))

        return inputs

    def input_weight(self, j):
        if j > self.n_input * 2:
            print "error: asked for a non-existing input weight"
        return self.weights[j]

    def w(self, i, j):

        if i < 2:
            weight = 2 * self.n_input + i * 2 + j
        else:
            if self.pull:
                weight = 2 * self.n_input + 4 + (i - 2) * 5 + j
            else:
                weight = 2 * self.n_input + 4 + (i - 2) * 4 + j
        #print "from " +str(j) + " to " + str(i) + " I take weight " + str(weight)
        return self.weights[weight]

    def dy(self, i):
        dy = self.s(i) + self.bias_weights[i] - self.y[i]
        if self.time_constants[i] == 0:
            return 0
        return dy / self.time_constants[i]

    def o(self, i):
        o = math.exp(-1 * self.gains[i] * self.y[i]) + 1.0
        return 1.0 / o

    def update_y(self, i):
        self.y[i] += self.dy(i)