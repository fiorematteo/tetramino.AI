from main import Tetris, AI
from time import time
from sys import argv
import matplotlib.pyplot as plt
import concurrent.futures as future

class virtualPlayer:

    def __init__(self):
        self.evolveSpeed = 1.1
        self.data = [[],[],[],[]]
        self.cicles = 0
        self.games = 0
        self.drawing = False

    def plotData(self, save = False):
        ncicle = range(self.cicles)
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(ncicle, self.data[0], label="points")
        ax1.set_xlabel("cicle")
        ax1.set_ylabel("points")
        ax2.plot(ncicle, self.data[1], "r", ncicle, self.data[2], "g", ncicle, self.data[3], "b")
        ax2.set_xlabel("cicle")
        ax2.set_ylabel("value")
        ax2.legend(('holes','lines','heights'))
        if save:
            plt.savefig("files/lastplot.svg", format="svg")
        else:
            plt.show()
    
    def saveDataToFile(self, filename):
        with open("files/"+filename+".csv","w") as file:
            file.write("Cicle,Points,Holesfactors,Linesfactor,Heigthfactor\n")
            for inx in range(self.cicles):
                file.write(f"{inx},{self.data[0][inx]},{self.data[1][inx]},{self.data[2][inx]},{self.data[3][inx]}\n")

    def startAi(self, cicles : int, games: int, drawing = False):
        self.cicles = cicles
        self.games = games
        self.drawing = drawing
        factors = [0,1,1,1]
        start_time = time()
        try:
            with open("files/setup.txt","r") as file:
                factors[0] = float(file.readline())
                factors[1] = float(file.readline())
                factors[2] = float(file.readline())
                factors[3] = float(file.readline())
        except:
            print("factors not loaded from file")

        factors = self.evolve(factors)

        with open("files/setup.txt","w") as file:
            for i in factors:
                file.write(str(i))
                file.write("\n")
        print(f"Process ended running time = {time()-start_time}s")

    def generation(self,holesFactor,linesFactor,heightFactor):
        points = 0
        for x in range(self.games):
            points+=Tetris().start(AI(holesFactor,linesFactor,heightFactor),self.drawing)
        return (points/self.games,holesFactor,linesFactor,heightFactor)
        
    @staticmethod
    def max(a,b,c):
        if a[0] > b [0] and a[0] > c[0]:
            return a
        if b[0] > a[0] and b[0] > c[0]:
            return b
        return c

    def evolve(self,factors):
        for x in range(self.cicles):
            t = time()
            gen1 = self.generation(factors[1]*self.evolveSpeed,factors[2],factors[3])
            gen2 = self.generation(factors[1],factors[2]*self.evolveSpeed,factors[3])
            gen3 = self.generation(factors[1],factors[2],factors[3]*self.evolveSpeed)

            factors = max(gen1,gen2,gen3)
            print(f"cicle {x} time {time()-t}s for {self.games*3} games")#debug

            for x in range(4):
                self.data[x].append(factors[x])
        return factors

vp = virtualPlayer()

if len(argv) == 3:
    vp.startAi(int(argv[1]), int(argv[2]))
else:
    vp.startAi(5, 10, True)
vp.plotData()
vp.saveDataToFile('data')
