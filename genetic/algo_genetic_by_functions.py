import operator
import random
from genetic.algo_genetic import *


class algo_genetic_by_functions(algo_genetic):

    def __init__(self, population_size: int, genome_size: int, mutate_ratio: float, init_population_fun, select_mates_fun,
                 reproduction_fun, mutation_fun):
        super().__init__(population_size, genome_size, mutate_ratio),
        self.init_population_fun = init_population_fun
        self.select_mates_fun = select_mates_fun
        self.reproduction_fun = reproduction_fun
        self.mutation_fun = mutation_fun

    def init_population(self) -> 'population':
        return self.init_population_fun()

    """
    return a subset of the mates_pool, ready to reproduce
    """
    def select_mates(self, potential_mates_pool) -> 'population':
        return self.select_mates_fun(potential_mates_pool)

    def reproduction(self, mates) -> 'population':
        return self.reproduction_fun(mates)

    """
    mutate a population by changing his genome
    this method keep the population size
    """
    def mutation(self, population) -> 'population':
        return self.mutation_fun(population)


def generic_selection(potential_mates_pool: population) -> population:
    """
    Generic selection as defined by : https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)
    :param potential_mates_pool:
    :return:
    """
    total_score = 0
    for ind in potential_mates_pool:
        total_score += ind.getScore()

    my_pool = {}
    for ind in potential_mates_pool:
        my_pool[ind] = ind.getScore() / total_score

    # sort pool by fitness
    my_pool = sorted(my_pool.items(), key=operator.itemgetter(1), reverse=True)

    # build a histogram
    pool_sum = 0
    for ind in my_pool:
        my_pool[ind] += pool_sum
        pool_sum = my_pool[ind]
    assert pool_sum == 1

    R = random.random()
    for ind in my_pool:
        if my_pool[ind] > R:
            return [ind]  # TODO return more than 1
    print("ERROR, no value found")

