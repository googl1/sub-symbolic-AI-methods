import Flatland
import sys
import getopt
import QLearning


def usage():
    print "\nusage: Main.py [arguments]"
    print "\n-h:\t\t\t\t\tprint the help"
    print "-l <level file>:\tspecify flatland level file"
    print "-a <int>:\t\t\tlearning rate"
    print "-y <int>:\t\t\tdiscount rate"
    print "-k <int>:\t\t\tnum of iterations in Q-Learning"
    print "-m <int>:\t\t\tmaximum temperature for simulated annealing"
    print "-t <int>:\t\t\ttrace-decay factor"


def merge_dicts(d1, d2):
    for k in d2.iterkeys():
        d1[k] += d2[k]
    return d1

if len(sys.argv) == 1:
    usage()
levelfile = 'lvls/2-still-simple.txt'
k = 600
a = 0.6
y = 0.4
m = 64*32
t = 0.2
x = 20
try:
  opts, args = getopt.getopt(sys.argv[1:],"hl:a:y:k:m:t:x:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        usage()
        sys.exit()
    elif opt in ("-l"):
        print "-l seen"
        levelfile = arg
    elif opt in ("-k"):
        k = int(arg)
    elif opt in ("-a"):
        a = arg
    elif opt in ("-y"):
        y = arg
    elif opt in ("-m"):
        m = arg
    elif opt in ("-t"):
        t = arg
    elif opt in ("-x"):
        x = arg

try:
    flatland = Flatland.Flatland(0, levelfile)
except:
    print "problem loading level file"
    usage()
    sys.exit(2)

q = QLearning.QLearning(k, levelfile, a, y, m, t, x)
q.learn()
q.run(False, [1.0], True)
while 1:
    q.run(True, [1.0], True)