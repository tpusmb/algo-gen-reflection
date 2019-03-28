import math
import operator
import random
import sys
from collections import OrderedDict
from typing import Callable

from genetic import *
from genetic.algogenetic import population, IndividualFactory


class AlgoGeneticByFunctions(AlgoGenetic):

    def __init__(self, population_size: int, genome_size: int, mutate_ratio: float,
                 factory: IndividualFactory, init_population_fun: Callable, select_mates_fun: Callable,
                 reproduction_fun: Callable, mutation_fun: Callable, crossover_ratio=0.5):
        super().__init__(population_size, genome_size, mutate_ratio, crossover_ratio, factory),
        self.init_population_fun = init_population_fun
        self.select_mates_fun = select_mates_fun
        self.reproduction_fun = reproduction_fun
        self.mutation_fun = mutation_fun

    def init_population(self) -> 'population':
        return self.init_population_fun(self.population_size, self.genome_size, self.factory)

    def select_mates(self, potential_mates_pool) -> 'population':
        """
        Select two different mates based on their fitness
        :param potential_mates_pool: the population you want individual to be pick up from
        :return: a couple from potential_mates_pool, ready to reproduce
        """
        return self.select_mates_fun(potential_mates_pool)

    def reproduction(self, mate1, mate2) -> 'population':
        """
        Simulate the reproduction from 2 mates
        no mutation is done, therefore no gene is lost
        :return: 2 children from the reproduction
        """
        return self.reproduction_fun(mate1=mate1, mate2=mate2, factory=self.factory,
                                     crossover_ratio=self.crossover_ratio)

    def mutation(self, population) -> 'population':
        """
        Mutate a population by changing his genome
        this method keep the population size
        :return: a mutated population
        """
        return self.mutation_fun(population, self.mutate_ratio)


def random_uniform_init(population_size: int, genome_size: int, factory: IndividualFactory):
    """
    Initialize a population by giving them random genome
    :param population_size: the size of the population created
    :param genome_size: the size of genome of each individual
    :param factory: the factory used to create all individual of the population
    :return:
    """
    res = []
    for i in range(population_size):
        genome = []
        for j in range(genome_size):
            genome.append(random.uniform(0, 1))
        res.append(factory.create_individual(genome))
    return res


def generic_selection_individual(potential_mates_pool: population) -> Individual:
    """
    Generic selection as defined by : https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)
    :param potential_mates_pool:
    :return:
    """
    total_score = 0
    for ind in potential_mates_pool:
        total_score += ind.get_score()

    my_pool = {}  # we retrieve all score and normalized them
    for ind in potential_mates_pool:
        my_pool[ind] = ind.get_score() / total_score

    # sort pool by fitness (descending)
    my_ordered_pool = OrderedDict(sorted(my_pool.items(), key=operator.itemgetter(1), reverse=True))

    # build a histogram
    pool_sum = 0
    for ind in my_ordered_pool:
        my_ordered_pool[ind] += pool_sum
        pool_sum = my_ordered_pool[ind]
    assert math.isclose(pool_sum, 1)

    R = random.random()
    for ind, fitness_sum in my_ordered_pool.items():
        if fitness_sum > R:
            return ind
    print("ERROR, no value found", file=sys.stderr)


def generic_selection_couple(potential_mates_pool: population) -> [Individual, Individual]:
    assert len(potential_mates_pool) >= 2
    mate1 = generic_selection_individual(potential_mates_pool)
    mate2 = generic_selection_individual(potential_mates_pool)
    while mate2 == mate1:
        mate2 = generic_selection_individual(potential_mates_pool)
    return mate1, mate2


def uniform_crossover(**kwargs)-> [Individual, Individual]:
    mate1 = kwargs.get('mate1')
    mate2 = kwargs.get('mate2')
    factory = kwargs.get('factory')
    genome1 = []
    genome2 = []
    assert len(mate1.genome) == len(mate2.genome)
    for i in range(len(mate1.genome)):
        if random.choice([mate1, mate2]) == mate1:
            genome1.append(mate1.genome[i])
            genome2.append(mate2.genome[i])
        else:
            genome1.append(mate2.genome[i])
            genome2.append(mate1.genome[i])
    return factory.create_individual(genome1), factory.create_individual(genome2)


def uniform_crossover_with_ratio(**kwargs)-> [Individual, Individual]:
    mate1 = kwargs.get('mate1')
    mate2 = kwargs.get('mate2')
    factory = kwargs.get('factory')
    crossover_ratio= kwargs.get('crossover_ratio')
    genome1 = []
    genome2 = []
    assert len(mate1.genome) == len(mate2.genome)
    for i in range(len(mate1.genome)):
        # child 1 inherit from parent1 according to crossover_ratio
        if random.uniform(0, 1) < crossover_ratio:
            genome1.append(mate1.genome[i])
            genome2.append(mate2.genome[i])
        else:
            genome1.append(mate2.genome[i])
            genome2.append(mate1.genome[i])
    return factory.create_individual(genome1), factory.create_individual(genome2)


def single_point_crossover(**kwargs)-> [Individual, Individual]:
    mate1 = kwargs.get('mate1')
    mate2 = kwargs.get('mate2')
    factory = kwargs.get('factory')
    genome1 = []
    genome2 = []
    assert len(mate1.genome) == len(mate2.genome)
    k = random.randint(0, len(mate1.genome))    # crossover point
    for i in range(0, k):
        genome1.append(mate2.genome[i])
        genome2.append(mate1.genome[i])
    for i in range(k, len(mate1.genome)):
        genome1.append(mate1.genome[i])
        genome2.append(mate2.genome[i])
    return factory.create_individual(genome1), factory.create_individual(genome2)


def dumb_crossover(**kwargs)-> [Individual, Individual]:
    mate1 = kwargs.get('mate1')
    mate2 = kwargs.get('mate2')
    factory = kwargs.get('factory')
    return factory.create_individual(mate1.genome), factory.create_individual(mate2.genome)



def mutation_uniform(population: population, mutate_ratio=0.1) -> population:
    for ind in population:
        for i in range(len(ind.genome)):
            if random.uniform(0, 1) <= mutate_ratio:
                ind.genome[i] = random.uniform(0, 1)
    return population


def mutation_gaussian(population: population, mutate_ratio=0.1, standard_deviation=0.25) -> population:
    for ind in population:
        for i in range(len(ind.genome)):
            if random.uniform(0, 1) <= mutate_ratio:
                new_value = random.gauss(ind.genome[i], standard_deviation)
                ind.genome[i] = max(min(new_value, 0), 1)  # clamp the value between 0 and 1
    return population
