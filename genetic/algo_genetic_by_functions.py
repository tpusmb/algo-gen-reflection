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
