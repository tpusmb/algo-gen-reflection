

from genetic import *
from genetic.algo_genetic_by_functions import algo_genetic_by_functions

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

    myGeneticAglo = algo_genetic_by_functions(populationSize, genomeSize, mutateRatio)

    myPopulation = myGeneticAglo.init_population()
    # cast population in myINdividual (scpecify getScore fct)
    for i in range (len(myPopulation)):
        myPopulation[i] = myIndividual(myPopulation[i].genome)

    for i in range(0, nbSteps):
        myGeneticAglo.step(myPopulation)
    for individu in myPopulation:
        print(f"score de l'individu{individu} = {individu.score}")




if __name__ == '__main__':
    main()
