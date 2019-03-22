

from genetic import *

'''

'''
populationSize = 10
genomeSize = 5
mutateRatio = 0.1
nbSteps = 5

def main():

    myGeneticAglo = algo_genetic(populationSize, genomeSize, mutateRatio)


    myPopulation = myGeneticAglo.init_population()

    for i in range(0, nbSteps):
        fitness(myPopulation)
        myGeneticAglo.step(myPopulation)
        #print(f"etape num {i}")
    for individu in myPopulation:
        print(f"score de l'individu{individu} = {individu.score}")




def fitness(population):
    idealScore = 5

    for individu in population:
        rawScore = abs(sum(individu.genom) - idealScore) # range : 0-5
        individu.score = 1 - rawScore/genomeSize




if __name__ == '__main__':
    main()
