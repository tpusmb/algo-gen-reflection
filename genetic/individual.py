from typing import List

genome: List[float]  # each genome is between 0 and 1


class individual:

    def __init__(self, score: float, gen: genome):
        self.score = score
        self.genome = gen

