from main import *

def max(a,b,c):
    if a[0] > b[0]:
        if a[0] > c[0]:
            return a
    if b[0] > a[0]:
        if b[0] > c[0]:
            return b
    return c

def generation(holesFactor,linesFactor,heightFactor):

    points = []
    for x in range(10):
        points.append(game(holesFactor,linesFactor,heightFactor))
        reset()
        print(str(x)+': '+str(points[x]))
    return (sum(points) / len(points)), holesFactor, linesFactor, heightFactor

def evolve(bestGen):

    gen1 = generation(bestGen[1]+100,bestGen[2],bestGen[3])
    gen2 = generation(bestGen[1],bestGen[2]+100,bestGen[3])
    gen3 = generation(bestGen[1],bestGen[2],bestGen[3]+100)

    bestGen = max(gen1,gen2,gen3)
    evolve(bestGen)

evolve((0,1,1,1))
