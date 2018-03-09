import Flatland
import collections
import random
import copy
import math


class QLearning:
    def __init__(self, k, lvl, learning_rt, discount_rt, t_max, t, x):
        self.k = k
        self.levelfile = lvl
        self.learning_rt = learning_rt
        self.discount_rt = discount_rt
        self.trace_decay_fac = t
        self.x = x
        self.t = 0
        self.t_max = t_max
        self.temp_step = self.t_max / float(self.k)
        self.path_factor = 25
        random.seed()

    def simulated_annealing(self):
        if self.t < self.t_max:
            self.t += self.temp_step
        return math.exp(-1.0 / (self.t))

    def run(self, draw_it, p, debug):
        self.flatland = Flatland.Flatland(draw_it, self.levelfile)
        state = (self.flatland.pos, 0)
        self.new_state = copy.deepcopy(state)
        self.all_states = list()
        j = 1
        if debug:
            steps = 0
        while self.flatland.game_finished != 2:
            if debug:
                steps += 1
            _p = p[len(p) - j]
            if _p != 1:
                _p *= 1
            if j < len(p):
                j += 1
            state = copy.deepcopy(self.new_state)
            a = self.select_action(state, self.q, _p, True)
            r = self.flatland.set_new_pos(a, self)
            self.new_state = (self.flatland.pos, self.new_state[1])
            if r > 0:
                new_num = self.new_state[1]
                new_num *= 10
                new_num += r
                new_num = int("".join(sorted(str(new_num))))
                self.new_state = (self.new_state[0], new_num)
                r = 5 # REWARD for food
            elif r == -2:
                r = 5 # reward for coming back to start
            elif r == -1:
                r = -5 # reward for poison
            if r == 0:
                r = -0.001 # reward for empty field
            self.all_states.append((state, a))
            self.update_q_array(self.q, state, a, r)
            self.all_states.append((state, a))
            if len(self.all_states) > self.x:
                self.all_states.remove(self.all_states[0])
        if debug:
            print "timesteps: " + str(steps)
            print "poison eaten: " + str(self.flatland.poison_score)

    def learn(self):
        self.q = collections.defaultdict(int)
        p = list()

        for i in range(self.k):
            if (i * 100.0 / self.k) % 1 == 0:
                print str(i * 100.0 / self.k) + " %"
            p.append(self.simulated_annealing())

            self.run(False, p, False)

    def update_q_array(self, q, state, a, r):
        d = r + self.discount_rt * self.get_best_rate((self.new_state[0], state[1]), q) - q[(state, a)]
        self.trace_decay(d, self.x)
        add = d
        add *= self.learning_rt
        q[(state, a)] += add

    def trace_decay(self, d, x):
        if d < 0:
            return
        e_s = 1
        for state in reversed(self.all_states):
            e_s *= self.discount_rt * self.trace_decay_fac
            self.q[state] += d * e_s * self.learning_rt
            x -= 1
            if x <= 0:
                break

    def get_best_rate(self, state, q):
        best = - float("inf")
        for q_entry in (q[(state, (0,1))], q[(state, (0,-1))], q[(state, (1,0))], q[(state, (-1,0))]):
            if q_entry > best:
                best = q_entry
        return best

    def select_action(self, state, q, p, rand):
        tournament = list()

        tournament.append((q[(state, (0,1))], (0,1)))
        tournament.append((q[(state, (0,-1))], (0,-1)))
        tournament.append((q[(state, (1,0))], (1,0)))
        tournament.append((q[(state, (-1,0))], (-1,0)))

        # if all actions are 0, choose randomly
        # if not, choose best with a probability of p
        # or randomly with probability (1-p)
        same = 0
        for t in tournament:
            if t[0] == 0:
                same += 1
        if same == len(tournament) or random.uniform(0,1) > p:
            if not rand:
                return (0,0)
            return tournament[random.randint(0, len(tournament) - 1)][1]

        #otherwise, choose the best
        tournament.sort(None, None, True)

        m = max(tournament)[1]
        return m