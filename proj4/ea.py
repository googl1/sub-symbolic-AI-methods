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
from Beer import *
from ctrnn import *
from Creature import *
from Population import *

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
        self.crossoverSlider.set(0.5)

        Label(self.mainframe, text="mutation ratio:").grid(column=2, row=9)
        self.mutationvar = tk.DoubleVar()
        self.mutationSlider = tk.Scale(self.mainframe, from_=0, to=1, resolution=0.02, orient=tk.HORIZONTAL)
        self.mutationSlider.grid(column=3, row=9)
        self.mutationSlider.set(0.5)

        self.problemvar = tk.StringVar()
        self.problemChooser = Combobox(self.mainframe, textvariable=self.problemvar, state='readonly')
        self.problemChooser.grid(row=0, column=0)
        self.problemChooser['values'] = ('One-Max Problem', 'LOLZ Prefix Problem', 'Surprising Sequences', 'ENN', 'CTRNN')
        self.problemChooser.bind('<<ComboboxSelected>>', self.problemChanged)
        self.problemChooser.set('CTRNN')

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
        self.popEntry.insert(0, '1400')

        Label(self.mainframe, text="parent selection: ").grid(column=0, row=4)
        self.parent_selvar = tk.StringVar()
        self.parent_selChooser = Combobox(self.mainframe, textvariable=self.parent_selvar, state='readonly')
        self.parent_selChooser.grid(row=4, column=1)
        self.parent_selChooser['values'] = ('Fitness-proportionate', 'Sigma-scaling', 'Tournament selection', 'Rank selection')
        self.parent_selChooser.bind('<<ComboboxSelected>>', self.parent_selection_changed)
        self.parent_selChooser.set('Tournament selection')

        Label(self.mainframe, text="e (randomnes): ").grid(column=0, row=5)
        self.evar = tk.DoubleVar()
        self.e_slider = tk.Scale( self.mainframe, resolution=0.01, from_=0, to_=1, orient=tk.HORIZONTAL)
        self.e_slider.set(0.65)
        self.e_slider.grid(column=1, row=5)
        #self.e_slider.config(state=tk.DISABLED)

        Label(self.mainframe, text="K: ").grid(column=2, row=5)
        self.kvar = tk.IntVar()
        self.k_entry = tk.Entry( self.mainframe, textvariable=self.kvar)
        self.k_entry.grid(row=5, column=3)
        self.k_entry.delete(0, tk.END)
        self.k_entry.insert(0, '100')
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
        self.scenChooser['values'] = ('standard', 'pull', 'no-wrap')
        self.scenChooser.bind('<<ComboboxSelected>>', self.parent_selection_changed)
        self.scenChooser.set('standard')

        Label(self.mainframe, text="number of children:").grid(column=0, row=3)
        self.childvar = tk.IntVar()
        self.childChooser = Entry(self.mainframe, textvariable=self.childvar)
        self.childChooser.grid(row=3, column=1)
        self.childChooser.delete(0, tk.END)
        self.childChooser.insert(0, '2000')
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
        self.gen_entry.insert(0, '15')

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
        seed()
        print getstate()
        #setstate((3, (2147483648L, 296489613L, 1076397952L, 2428418361L, 45459062L, 1894483670L, 335329768L, 2031380552L, 3076418855L, 2429538835L, 4272262773L, 3361056106L, 903222629L, 1463737370L, 2438095269L, 3537576437L, 3587979514L, 338959731L, 3301545455L, 4162878228L, 2727219174L, 2828247338L, 3139713768L, 944944906L, 1818897910L, 2136338968L, 1791336164L, 529670059L, 1511456287L, 1080001583L, 1010484399L, 1159557510L, 2135101481L, 3309558473L, 458446266L, 471555446L, 1131446030L, 374829882L, 2525505144L, 357980591L, 710051289L, 4041890438L, 863602231L, 2260840414L, 732950156L, 2242467305L, 3240455185L, 4242845042L, 1035601784L, 888073371L, 745976109L, 2888085200L, 513813626L, 580728588L, 3089375272L, 1678859731L, 1896609040L, 1341579711L, 913731810L, 795675889L, 1254139396L, 160946699L, 3351778545L, 384852267L, 813931920L, 2901252324L, 1462253865L, 3082505375L, 3369804621L, 4276133704L, 4076155479L, 4226083476L, 2766361988L, 4086021408L, 3319301019L, 1681754794L, 4271745887L, 3764179698L, 2634161832L, 3263267522L, 1457550409L, 2784672950L, 1030349984L, 3922143354L, 3775649292L, 936514494L, 4023627221L, 3746616037L, 1681410722L, 2198527549L, 2643326818L, 3932104911L, 3765424459L, 74532732L, 4033781069L, 2849840771L, 420233014L, 3920131272L, 2949171524L, 665105041L, 110692541L, 4029051427L, 176152677L, 3828021145L, 2737581850L, 1848531483L, 1701334227L, 3043446287L, 539626391L, 450994959L, 2752658320L, 4045076415L, 3894163553L, 528052409L, 1541630849L, 90111319L, 1714519487L, 1053387177L, 3116134934L, 1917343855L, 2943553281L, 2380452740L, 2647132919L, 2445188486L, 2065643890L, 1592449267L, 2005770974L, 2595399025L, 4043856577L, 4242388507L, 2840395119L, 1988116546L, 226741931L, 3231068597L, 2758645778L, 2721051147L, 2193494512L, 4050167403L, 953683528L, 89491065L, 3510168649L, 3665946817L, 3484830971L, 3663326187L, 2232858394L, 2475989710L, 3801783926L, 1419935705L, 2401007477L, 3888698199L, 3631170318L, 630497120L, 3280396670L, 1477404870L, 2009126239L, 506393634L, 3648388931L, 3861732513L, 2541368369L, 708074070L, 1045669246L, 2921513746L, 1016931056L, 3060025899L, 1612833169L, 1587161433L, 3012079186L, 1336394408L, 285522929L, 1483700454L, 1145828568L, 1055202854L, 722334833L, 3300020215L, 3926485562L, 1458063445L, 3500325977L, 3410558543L, 1405181501L, 2585230622L, 2091839455L, 1962892045L, 2825924975L, 2880889958L, 1055634064L, 402151200L, 492066687L, 3282370138L, 761336355L, 1570664574L, 1606771072L, 2946769406L, 2021617035L, 1563024843L, 201231423L, 2417995457L, 2374369362L, 124357927L, 3708995763L, 4184439420L, 54406553L, 1284386211L, 1892712130L, 2780333930L, 3476938786L, 643081341L, 2177684939L, 2454559716L, 472260776L, 2142219757L, 515814517L, 1644075634L, 2597785247L, 421874836L, 2435910256L, 730613196L, 2051876400L, 2761865125L, 2905336699L, 940753185L, 1806979914L, 2988264214L, 1708069325L, 1578491181L, 4265891567L, 3535681485L, 1011573532L, 1127860221L, 2369750117L, 1557142715L, 3015469853L, 3153386217L, 659660386L, 946321509L, 1684422314L, 3108200065L, 3252589278L, 2338055373L, 682324187L, 1478256646L, 2491600249L, 1293771954L, 631109587L, 1356374539L, 1659486369L, 1572539875L, 2351065669L, 461382493L, 2157768364L, 2299725674L, 885902376L, 712025517L, 894752919L, 3257204977L, 2709081950L, 1770414917L, 1612092295L, 4093147226L, 806805391L, 2476757881L, 3462598493L, 2895282721L, 155515314L, 3396733069L, 584142389L, 2941522672L, 657830982L, 2083946526L, 1896790575L, 414423124L, 3114530423L, 3197489031L, 1245420872L, 4257892118L, 3308019879L, 1900581035L, 4059405065L, 2588625159L, 1061969252L, 685529856L, 589800941L, 3543964217L, 2072442928L, 1014301028L, 3354378493L, 2499749131L, 4262054023L, 3854137482L, 1164035331L, 2025017024L, 2479794547L, 1193338768L, 2151991823L, 65870803L, 1842515185L, 1176758181L, 2645595900L, 285424395L, 2317203563L, 1948315664L, 1804602296L, 1846373695L, 88928536L, 70302679L, 94857980L, 2927489630L, 874991508L, 3035147698L, 3183241842L, 630643891L, 1093989519L, 3092466885L, 858285148L, 2802226591L, 945678387L, 1346092795L, 4264545097L, 2101884816L, 1231365038L, 3539150396L, 379497944L, 1821213779L, 854368988L, 2225449445L, 4029144465L, 4035070226L, 3642026821L, 2505520045L, 2380323811L, 183944691L, 573550018L, 3513765693L, 4106329336L, 490942319L, 2422050883L, 2798673218L, 832609312L, 809764146L, 178859688L, 2632300695L, 1034703130L, 2299353619L, 1325430759L, 1784968302L, 950994149L, 1767327074L, 1548735876L, 2005531969L, 973066190L, 2146575728L, 215452092L, 3302300559L, 2556694737L, 855112424L, 393731042L, 2936506359L, 1850530765L, 4263363954L, 2180953072L, 1414985206L, 2791415137L, 3665082835L, 921356466L, 3647908995L, 3873429611L, 3959399841L, 2747514229L, 2745465653L, 1586234542L, 1822002558L, 2331227933L, 2984189586L, 524814439L, 854112419L, 3060876624L, 2731314840L, 2906487961L, 365369696L, 3912973427L, 4277179309L, 3550075398L, 3899453550L, 968806638L, 2673156476L, 2068282407L, 1486820728L, 1143840840L, 692742027L, 3131685634L, 1216336427L, 2114651124L, 480621632L, 3573796683L, 2298338259L, 285047319L, 2777468633L, 3556068804L, 3636362091L, 2346060026L, 1371264304L, 3356086994L, 1563685637L, 3229714244L, 1554274069L, 1746093445L, 3222974435L, 773492520L, 3154168855L, 747773860L, 2565118822L, 2397697647L, 2414671504L, 1787289293L, 1878609129L, 2662857003L, 2630003359L, 1749900624L, 2940958638L, 2806869589L, 1877466378L, 3689455348L, 1440408297L, 783834965L, 3065031157L, 732558370L, 1612761755L, 3623318454L, 2653396251L, 145182106L, 2063573351L, 3941715322L, 91934863L, 428517736L, 2891542919L, 307467381L, 489504965L, 1492852190L, 3880980093L, 2613262157L, 1084657249L, 89297116L, 1860495082L, 974774039L, 1229728471L, 246143902L, 1826124197L, 4184586872L, 3173713546L, 1558749838L, 2906074114L, 1565932105L, 2327192896L, 4175001314L, 3316024724L, 2674802589L, 2848106059L, 1788248333L, 2558570748L, 1489820142L, 3142826519L, 495402832L, 2742030248L, 192436669L, 3885236311L, 919912143L, 1126919318L, 2479942910L, 2515383015L, 307529895L, 2260591000L, 3942861389L, 2524516779L, 3875752808L, 458189487L, 1683640547L, 2714305786L, 3285555915L, 4283156956L, 102911768L, 2875532113L, 1263816151L, 2224647157L, 170068894L, 644397944L, 406385417L, 2405947881L, 4076310907L, 1106651450L, 4055730571L, 4004675029L, 1897833762L, 3875370846L, 3597552139L, 3699518616L, 740934580L, 1863322649L, 4137970641L, 230705433L, 3843343181L, 152121916L, 2902509023L, 3091462914L, 2177094988L, 822757827L, 1715633524L, 1001440903L, 2709886890L, 2765931407L, 1916743023L, 1067630573L, 2863440637L, 455639349L, 459873852L, 635866217L, 15534980L, 2252177297L, 1151143130L, 3394557411L, 2889024216L, 3275391761L, 2184055842L, 4238024134L, 221601852L, 2883033574L, 198237267L, 4209396083L, 3561017639L, 1437387142L, 2836958874L, 200869549L, 3059480808L, 635598588L, 1656707379L, 3101912734L, 1109534876L, 2346769702L, 3131927741L, 2586021206L, 607772473L, 1523147738L, 434533690L, 1923834505L, 2167570695L, 2163222026L, 1254173097L, 317503906L, 500992324L, 4200759153L, 3728816749L, 203756920L, 2758577022L, 1368953930L, 3815843339L, 2832858564L, 3782264381L, 166687219L, 2068666068L, 3983199620L, 3416705226L, 2814379091L, 2727060588L, 4186733926L, 1003049353L, 315965454L, 948937512L, 192275764L, 3435344598L, 4216283788L, 3460675236L, 252014836L, 541171547L, 241183597L, 2624417270L, 4074648958L, 4200664953L, 583184365L, 3754302388L, 4209205806L, 3229376606L, 3575738381L, 825439633L, 119885922L, 2374149902L, 631762527L, 186251379L, 1290133225L, 3253756224L, 3031029402L, 1973541139L, 2538069704L, 390708732L, 1028937503L, 3573815456L, 2203700113L, 276572908L, 54836601L, 3102861442L, 1269093013L, 195789408L, 1875006169L, 3737573796L, 3882097917L, 2534270240L, 2839599838L, 859058554L, 481879324L, 617526235L, 1177179229L, 3098495432L, 1406947181L, 692243007L, 1793393363L, 1735224996L, 4110441220L, 2877394320L, 128539971L, 843402433L, 2486970426L, 4190878869L, 3476387003L, 3430707982L, 521719431L, 1693637956L, 1037930504L, 624L), None))
        if self.selectionChooser.get() == 'Full Generational Replacement':
            childs = int(self.popEntry.get())
        else:
            childs = int(self.childChooser.get())

        self.population = Population(int(self.popEntry.get()), int(self.lengthChooser.get()), childs, int(self.zEntry.get()),
                                int(self.lChooser.get()), int(self.sChooser.get()), self.problemChooser.get(),
                                int(self.neurons_entry.get()), int(self.layers_entry.get()), int(self.acc_entry.get()),
                                self.scenChooser.get(), float(self.threshold_entry.get()), int(self.elitism_entry.get()))
        self.population.log_init()
        if self.problemChooser.get() == 'ENN':
            self.population.set_new_scenario(int(self.set_entry.get()))
        generation_counter = 0
        #print "e: " + str(self.e_slider.get())
        while 1:
            #generate scenario
            if self.scenChooser.get() == 'dynamic' and self.problemChooser.get() == 'ENN':
                self.population.set_new_scenario(int(self.set_entry.get()))
            else:
                self.population.scenarios = [None]
            self.population.fitness(self.problemChooser.get(), self.globlocChooser.get())
            self.population.adult_selection(self.selectionChooser.get())
            self.population.log()

            if self.population.best.fitness >= 0.5 or generation_counter == int(self.gen_entry.get()) - 1:
                break
            generation_counter += 1
            self.population.parent_selection(self.parent_selChooser.get(), self.k_entry.get(), self.e_slider.get())
            #self.population.adults.sort(key=attrgetter('fitness'), reverse=True)
            self.population.make_love(float(self.mutationSlider.get()), float(self.crossoverSlider.get()))
            #print len(self.population.children)

        if self.visChooser.get() == "no":
            self.quit()
            return

        # f, axarr = plt.subplots(3, sharex=True)
        # axarr[0].plot(self.population.log_best_fitness)
        # axarr[0].set_title('best fitness', fontsize=12)
        # axarr[1].plot(self.population.log_avg)
        # axarr[1].set_title('average fitness', fontsize=12)
        # axarr[2].plot(self.population.log_sd)
        # axarr[2].set_title('standard deviation of fitness', fontsize=12)

        # visualize
        if self.problemChooser.get() == 'ENN' or self.problemChooser.get() == 'CTRNN':
            self.playwin = tk.Tk()
            self.playwin.title("Control Visualization")
            playframe = Frame(self.playwin)
            playframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
            playframe.columnconfigure(0, weight=1)
            playframe.rowconfigure(0, weight=1)
            Button(playframe, text="Generate random map", command=self.random_visualization).grid(column=0, row=0, sticky=tk.W)
            Button(playframe, text="Quit", command=self.quit).grid(column=1, row=0, sticky=tk.W)

            Label(playframe, text="speed: ").grid(column=0, row=1)
            speed_slider = tk.Scale(playframe, resolution=0.01, from_=0.0, to_=1, orient=tk.HORIZONTAL)
            speed_slider.set(0.5)
            speed_slider.grid(column=1, row=1)


            while (self.run):
                if self.problemChooser.get() == 'ENN':
                    if self.scenChooser.get() == 'dynamic':
                        self.population.set_new_scenario(1)
                    for s in self.population.scenarios:
                        s.speed = speed_slider.get()
                self.population.best.fitness_fun(self.problemChooser.get(), self.population.z, True, self.population.scenarios, True, speed_slider.get())
                print "score " + str(self.population.best.fitness)

        #plt.show()


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






GUI()