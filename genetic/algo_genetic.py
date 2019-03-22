from genetic.individual import *

population: List[individual]


class algo_genetic:

    def __init__(self, population_size: int, genome_size: int, mutate_ratio: float):
        self.population_size = population_size
        self.genome_size = genome_size
        self.mutate_ratio = mutate_ratio

    def init_population(self) -> population:
        pass

    def init_genome(self) -> genome:
        pass

    """
    return a subset of the mates_pool, ready to reproduce
    """
    def select_mates(self, potential_mates_pool: population) -> population:
        pass

    def reproduction(self, mates: population) -> population:
        pass

    """
    mutate a population by changing his genome
    this method keep the population size
    """
    def mutation(self, population: population) -> population:
        pass

    def step(self, previous_population: population) -> population:
        mates = self.select_mates(previous_population)
        children = self.reproduction(mates)
        return self.mutation(children)
