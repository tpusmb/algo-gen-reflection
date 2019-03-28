from abc import abstractmethod
from typing import List

genome = List[object]


class Individual:
    """Inherit this class to implement your own individual"""

    def __init__(self, gen: genome):
        self.genome = gen


    @abstractmethod
    def get_score(self) -> float:
        """
        The score allow the algo to classify individual's fitness
        :return: a score between 0 (bad fitness) and 1 (outstanding fitness)
        """
        pass


class IndividualFactory:
    """Inherit this class to allow genetic algorithms to create your own individual"""

    def create_individual(self, gen: genome) -> Individual:
        return Individual(gen)


