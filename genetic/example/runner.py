from genetic.algo_genetic_by_functions import *
from genetic.individual import genome

populationSize = 100
genomeSize = 5
mutateRatio = 0.001
crossover_ratio = 0.7
nbSteps = 1000


class MyIndividual(Individual):
    idealScore = genomeSize
    score_dict = {}

    def get_score(self) -> float:
        sum_genome = sum(self.genome)
        if sum_genome not in self.score_dict:
            raw_score = abs(sum_genome - self.idealScore)  # range : 0-5
            self.score_dict[sum_genome] = 1 - raw_score / genomeSize
        return self.score_dict[sum_genome]


class MyIndividualFactory(IndividualFactory):

    def create_individual(self, gen: genome):
        return MyIndividual(gen)


def main():
    my_factory = MyIndividualFactory()
    my_genetic_algo = AlgoGeneticByFunctions(populationSize, genomeSize, mutateRatio, my_factory, random_uniform_init,
                                             generic_selection_couple, uniform_crossover_with_ratio, mutation_gaussian,
                                             crossover_ratio)

    my_population = my_genetic_algo.init_population()

    for i in range(nbSteps):
        my_population = my_genetic_algo.step_paralleled(my_population)
        mean_score = 0
        for individu in my_population:
            mean_score += individu.get_score()
        mean_score /= len(my_population)
        if ((i + 1) % 10) == 0:
            print(f"step {i + 1} : {mean_score}")   # display only multiple of 10 population
    for individu in my_population:
        print(f"individu's score {individu} = {individu.get_score()}")
    print("done")


if __name__ == '__main__':
    main()
