

from genetic import *

'''

'''
populationSize = 10
genomeSize = 5
mutateRatio = 0.1
nbSteps = 5

class myIndividual(individual):
    idealScore = 5

    def getScore(self) -> float:
        rawScore = abs(sum(self.genome) - self.idealScore)  # range : 0-5
        return 1 - rawScore / genomeSize


def main():

    myGeneticAglo = algo_genetic(populationSize, genomeSize, mutateRatio)


    myPopulation = myGeneticAglo.init_population()

    for i in range(0, nbSteps):
        fitness(myPopulation)
        myGeneticAglo.step(myPopulation)
        #print(f"etape num {i}")
    for individu in myPopulation:
        print(f"score de l'individu{individu} = {individu.score}")






if __name__ == '__main__':
    main()
