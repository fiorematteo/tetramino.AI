from main import Tetris
from time import time
import concurrent.futures as future

class virtualPlayer:

    def __init__(self):
        self.evolveSpeed = 0.1
        self.data = []
        self.cicles = 0

    def plotData(self):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(ncicle, data[0], label="points")
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
                file.write(f"|points = {data[0][inx]} | holef = {data[1][inx]} | linef = {data[2][inx]} | heightf = {data[3][inx]} |\n")

    def startAi(self, cicles):
        start_value = [0,1,1,1]
        start_time = time()
        try:
            with open("setup.txt","r") as file:
                ai[0] = float(file.readline())
                ai[1] = float(file.readline())
                ai[2] = float(file.readline())
                ai[3] = float(file.readline())
        except:
            print("ai not loaded from file")

        ai = evolve(ai)

        with open("setup.txt","w") as file:
            for i in ai:
                file.write(str(i))
                file.write("\n")
        print(f"Process ended running time = {time()-start_time}s")

            