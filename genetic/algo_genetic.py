from abc import abstractmethod
from multiprocessing.pool import ThreadPool

from genetic.individual import *

population = List[Individual]


class AlgoGenetic:

    def __init__(self, population_size: int, genome_size: int, mutate_ratio: float, crossover_ratio: float,
                 factory: IndividualFactory, range_min=-1, range_max=1):
        assert genome_size != 0
        self.population_size = population_size
        self.genome_size = genome_size
        self.mutate_ratio = mutate_ratio
        self.crossover_ratio = crossover_ratio
        self.factory = factory
        self.range_min = range_min
        self.range_max = range_max

        self.pool = ThreadPool(processes=4)

    @abstractmethod
    def init_population(self) -> population:
        pass

    @abstractmethod
    def select_mates(self, potential_mates_pool) -> [Individual, Individual]:
        """
        Select two different mates based on their fitness
        :param potential_mates_pool: the population you want individual to be pick up from
        :return: a couple from potential_mates_pool, ready to reproduce
        """
        pass

    @abstractmethod
    def reproduction(self, mate1, mate2) -> [Individual, Individual]:
        """
        Simulate the reproduction from 2 mates
        no mutation is done, therefore no gene is lost
        :return: 2 children from the reproduction
        """
        pass

    @abstractmethod
    def mutation(self, population) -> population:
        """
        Mutate a population by changing his genome
        this method keep the population size
        :return: a mutated population
        """
        pass

    def step(self, previous_population: population) -> population:
        """
        Bring the population a step forward evolution
        """
        children = []
        while len(children) < self.population_size:
            mate1, mate2 = self.select_mates(previous_population)
            child1, child2 = self.reproduction(mate1, mate2)
            children.append(child1)
            children.append(child2)
        if len(children) == self.population_size + 1:
            children.pop()
        return self.mutation(children)

    def step_paralleled(self, previous_population: population) -> population:
        return self.pool.apply(self.step, [previous_population])
