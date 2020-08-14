from main import Tetris, AI
from time import time
import matplotlib.pyplot as plt
import concurrent.futures as future

class virtualPlayer:

    def __init__(self):
        self.evolveSpeed = 1.1
        self.data = [[],[],[],[]]
        self.cicles = None
        self.games = 2

    def plotData(self):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(self.cicles, data[0], label="points")
        ax1.set_xlabel("cicle")
        ax1.set_ylabel("points")
        ax2.plot(ncicle, data[1], "r", ncicle, data[2], "g", ncicle, data[3], "b")
        ax2.set_xlabel("cicle")
        ax2.set_ylabel("value")
        ax2.legend(('holes','lines','heights'))
        plt.show()
    
    def saveDataToFile(self, filename):
        with open(filename+".txt","w") as file:
            for inx in range(self.cicles):
                file.write(f"|points = {self.data[0][inx]} | holef = {self.data[1][inx]} | linef = {self.data[2][inx]} | heightf = {self.data[3][inx]} |\n")

    def startAi(self, cicles):
        self.cicles = cicles
        factors = [0,1,1,1]
        start_time = time()
        try:
            with open("setup.txt","r") as file:
                factors[0] = float(file.readline())
                factors[1] = float(file.readline())
                factors[2] = float(file.readline())
                factors[3] = float(file.readline())
        except:
            print("factors not loaded from file")

        factors = self.evolve(factors)

        with open("setup.txt","w") as file:
            for i in factors:
                file.write(str(i))
                file.write("\n")
        print(f"Process ended running time = {time()-start_time}s")

    def generation(self,holesFactor,linesFactor,heightFactor):
        points = 0
        for x in range(self.games):
            points+=Tetris().start(AI(holesFactor,linesFactor,heightFactor),True)
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
            gen1 = self.generation(factors[1]*self.evolveSpeed,factors[2],factors[3])
            gen2 = self.generation(factors[1],factors[2]*self.evolveSpeed,factors[3])
            gen3 = self.generation(factors[1],factors[2],factors[3]*self.evolveSpeed)
            
            factors = max(gen1,gen2,gen3)

            for x in range(3):
                self.data[x].append(factors[x])
        return factors

vp = virtualPlayer()
vp.startAi(2)
#vp.saveDataToFile('puttana_madonna')
#vp.plotData()
