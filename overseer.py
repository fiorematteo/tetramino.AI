from main import *
import matplotlib.pyplot as plt
import concurrent.futures

evolve_speed = 1.1

def max(a,b,c):
    if a[0] > b[0]:
        if a[0] > c[0]:
            return a
    if b[0] > a[0]:
        if b[0] > c[0]:
            return b
    return c
def plot(gens):
    ncicle = range(len(gens))
    data = [[],[],[],[]]
    for x in ncicle:
        data[0].append(gens[x][0])
        data[1].append(gens[x][1])
        data[2].append(gens[x][2])
        data[3].append(gens[x][3])
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(ncicle, data[0], label="points")
    ax1.set_xlabel("cicle")
    ax1.set_ylabel("points")
    ax2.plot(ncicle, data[1], "r", ncicle, data[2], "g", ncicle, data[3], "b")
    ax2.set_xlabel("cicle")
    ax2.set_ylabel("value")
    ax2.legend(('holes','lines','heights'))
    plt.show()

def generation(holesFactor,linesFactor,heightFactor,generation):
    points = []
    for x in range(1):
        points.append(game(holesFactor,linesFactor,heightFactor))
        reset()
    print(f"Generation {generation}: ho={holesFactor},l={linesFactor},he={heightFactor},p={sum(points)/len(points)}")
    return (sum(points) / len(points), holesFactor, linesFactor, heightFactor)

def evolve(bestGen, cicles):
    gens = []
    for r in range(cicles):
        print("------------------")
        with concurrent.futures.ThreadPoolExecutor() as ex:
            gen1 = ex.submit(generation,bestGen[1]*evolve_speed,bestGen[2],bestGen[3],1)
            gen2 = ex.submit(generation,bestGen[1],bestGen[2]*evolve_speed,bestGen[3],2)
            gen3 = ex.submit(generation,bestGen[1],bestGen[2],bestGen[3]*evolve_speed,3)
            gen1 = gen1.result()
            gen2 = gen2.result()
            gen3 = gen3.result()
        bestGen = max(gen1,gen2,gen3)
        gens.append(bestGen)
        print(f"cicle = {r}")
    print("------------------")
    plot(gens)
    return bestGen

def load_ai():
    ai = [0,1,1,1]
    try:
        with open("score.txt","r") as file:
            ai[0] = float(file.readline())
            ai[1] = float(file.readline())
            ai[2] = float(file.readline())
            ai[3] = float(file.readline())
    except:
        pass
    ai = evolve(ai, 5)
    with open("score.txt","w") as file:
        for i in ai:
            file.write(str(i))
            file.write("\n")
    print(f"end -> {ai}")

load_ai()
