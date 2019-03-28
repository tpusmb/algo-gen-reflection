from genetic.algo_genetic_by_functions import *
from genetic.individual import genome

populationSize = 100
genomeSize = 5
mutateRatio = 0.001
nbSteps = 1000


class MyIndividual(Individual):
    idealScore = genomeSize

    def get_score(self) -> float:
        raw_score = abs(sum(self.genome) - self.idealScore)  # range : 0-5
        return 1 - raw_score / genomeSize


class MyIndividualFactory(IndividualFactory):

    def create_individual(self, gen: genome):
        return MyIndividual(gen)


def main():
    my_factory = MyIndividualFactory()
    my_genetic_algo = AlgoGeneticByFunctions(populationSize, genomeSize, mutateRatio, my_factory, random_uniform_init,
                                             generic_selection_couple, uniform_crossover, mutation_gaussian)

    my_population = my_genetic_algo.init_population()

    for i in range(nbSteps):
        my_population = my_genetic_algo.step(my_population)
        mean_score = 0
        for individu in my_population:
            mean_score += individu.get_score()
        mean_score /= len(my_population)
        if ((i + 1) % 10) == 0:
            print(f"step {i + 1} : {mean_score}")
    for individu in my_population:
        print(f"individu's score {individu} = {individu.get_score()}")
    print("done")


if __name__ == '__main__':
    main()
