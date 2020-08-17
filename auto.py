from main import Tetris, AI

import numpy
from time import time
from sys import argv
import matplotlib.pyplot as plt
import concurrent.futures as futures


class virtualPlayer:

    def __init__(self):
        self.evolveSpeed = 1.1
        self.data = [[], [], [], []]
        self.cicles = 0
        self.games = 0
        self.drawing = False

    def calculate_regression(self, points, ncicles):
        model = numpy.poly1d(numpy.polyfit(points, ncicles, 2))
        line = numpy.linspace(0, len(ncicles)-1)
        return line, model(line)

    def plotData(self, save=False):
        ncicle = range(self.cicles)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        xreg, yreg = self.calculate_regression(self.data[0], ncicle)
        ax1.plot(ncicle, self.data[0], "b", xreg, yreg, "r")
        ax1.set_xlabel("cicle")
        ax1.set_ylabel("points")
        ax1.legend(('points', 'regression'))
        ax2.plot(ncicle, self.data[1], "r", ncicle,
                 self.data[2], "g", ncicle, self.data[3], "b")
        ax2.set_xlabel("cicle")
        ax2.set_ylabel("value")
        ax2.legend(('holes', 'lines', 'heights'))
        if save:
            plt.savefig("files/lastplot.svg", format="svg")
        plt.show()

    def saveDataToFile(self, filename):
        with open("files/"+filename+".csv", "w") as file:
            file.write("Cicle,Points,Holesfactors,Linesfactor,Heigthfactor\n")
            for inx in range(self.cicles):
                file.write(
                    f"{inx},{self.data[0][inx]},{self.data[1][inx]},{self.data[2][inx]},{self.data[3][inx]}\n")

    def startAi(self, cicles: int, games: int, drawing=False):
        self.cicles = cicles
        self.games = games
        self.drawing = drawing
        factors = [0, 1, 1, 1]
        start_time = time()
        try:
            with open("files/setup.txt", "r") as file:
                factors[0] = float(file.readline())
                factors[1] = float(file.readline())
                factors[2] = float(file.readline())
                factors[3] = float(file.readline())
        except:
            print("factors not loaded from file")

        factors = self.evolve(factors)

        with open("files/setup.txt", "w") as file:
            for i in factors:
                file.write(str(i))
                file.write("\n")
        print(f"Process ended running time = {time()-start_time}s")

    def generation(self, holesFactor, linesFactor, heightFactor):
        points = 0
        '''gamesList = []
        with futures.ThreadPoolExecutor() as executor:'''
        for x in range(self.games):
            points += Tetris().start(AI(holesFactor, linesFactor, heightFactor), self.drawing)
        return (points/self.games, holesFactor, linesFactor, heightFactor)

    def mt_generation(self, factors):  # multithread generation
        gens = []
        with futures.ThreadPoolExecutor() as executor:
            gens.append(executor.submit(
                self.generation, factors[1]*self.evolveSpeed, factors[2], factors[3]))
            gens.append(executor.submit(
                self.generation, factors[1], factors[2]*self.evolveSpeed, factors[3]))
            gens.append(executor.submit(
                self.generation, factors[1], factors[2], factors[3]*self.evolveSpeed))
            gens.append(executor.submit(
                self.generation, factors[1]/self.evolveSpeed, factors[2], factors[3]))
            gens.append(executor.submit(
                self.generation, factors[1], factors[2]/self.evolveSpeed, factors[3]))
            gens.append(executor.submit(
                self.generation, factors[1], factors[2], factors[3]/self.evolveSpeed))

            gens = list(map(lambda g: g.result(), gens))
            scores = list(map(lambda g: g[0], gens))
            return gens[scores.index(max(scores))]

    def evolve(self, factors):
        for x in range(self.cicles):
            t = time()

            # gen1 = self.generation(factors[1]*self.evolveSpeed,factors[2],factors[3])
            # gen2 = self.generation(factors[1],factors[2]*self.evolveSpeed,factors[3])
            # gen3 = self.generation(factors[1],factors[2],factors[3]*self.evolveSpeed)

            factors = self.mt_generation(factors)
            # debug
            print(f"cicle {x} time {time()-t}s for {self.games*6} games")

            for x in range(4):
                self.data[x].append(factors[x])
        return factors


vp = virtualPlayer()

if len(argv) >= 3:
    vp.startAi(int(argv[1]), int(argv[2]))
else:
    vp.startAi(5, 1, True)
vp.plotData(argv[3] if len(argv) == 4 else False)
vp.saveDataToFile('data')
