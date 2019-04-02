#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json
import logging.handlers
import os
import time
from math import sqrt

from neural import Neuron, Input
from genetic.algo_genetic_by_functions import *
from genetic.individual import genome

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/test.log",
                                                 when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(filename)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

# Absolute path to the folder location of this python file
FOLDER_ABSOLUTE_PATH = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))
NUMBER_OF_DINO = 50


class DinoNeurons(Individual):

    def __init__(self, input_list, gen: genome):
        """

        :param input_list:
        """
        super().__init__(gen)
        self.input_list = input_list
        self.neuron_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)
        self.neuron_no_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)

        # Load the gnome
        index_gen = 0
        # jump neuron - 1 to remove the bias node
        for index_weight in range(self.neuron_jump.get_weight_len() - 1):
            self.neuron_jump.weight_liste[index_weight] = gen[index_gen]
            index_gen += 1
        # bias node for jump neuron
        self.neuron_jump.set_threshold(gen[index_gen])
        index_gen += 1

        # no jump neuron - 1 to remove the bias node
        for index_weight in range(self.neuron_no_jump.get_weight_len() - 1):
            self.neuron_no_jump.weight_liste[index_weight] = gen[index_gen]
            index_gen += 1

        # bias node for jump neuron
        self.neuron_no_jump.set_threshold(gen[index_gen])
        self.dino_score = None

    def set_score(self, score):
        self.dino_score = score

    def need_to_jump(self):

        return self.neuron_jump.compute() > self.neuron_no_jump.compute()

    def get_score(self):

        if self.dino_score is None:
            raise ValueError("The score is not set")
        return self.dino_score


class DinoFactory(IndividualFactory):

    def __init__(self, inputs_list):
        """

        :param inputs_list:
        """
        self.inputs_list = inputs_list

    def create_individual(self, gen: genome):

        return DinoNeurons(self.inputs_list, gen)


def write_best_genom(d_population, scores, nb_iteration):
    best_score = 0
    best_score_index = -1
    for i in range(len(d_population) - 1):
        best_score_index += 1
        PYTHON_LOGGER.info("Score de {} = {}".format(i, scores[i]))
        if scores[i] > best_score:
            best_score = scores[i]
    data = {}
    data['score'] = []
    data['genom'] = []
    data['score'].append(best_score)
    data['genom'].append(d_population[best_score_index].genome)
    with open('best_score{}.txt'.format(nb_iteration), 'w') as outfile:
        json.dump(data, outfile)


if __name__ == "__main__":
    from neural import sigmoid
    from dino_game import GameController, width

    game_speed = Input(value=0)
    distance_next_obstacle = Input(value=0)
    gap_between_obstacles = Input(value=0)
    input_list = [game_speed, distance_next_obstacle, gap_between_obstacles]
    # dino_neurones_list = [DinoNeurons(input_list) for _ in range(10)]
    genetic = AlgoGeneticByFunctions(population_size=NUMBER_OF_DINO,
                                     genome_size=(len(input_list) + 1) * 2,
                                     mutate_ratio=0.1,
                                     factory=DinoFactory(input_list),
                                     init_population_fun=random_uniform_init,
                                     select_mates_fun=generic_selection_couple,
                                     reproduction_fun=uniform_crossover,
                                     mutation_fun=mutation_gaussian,
                                     crossover_ratio=0.9,
                                     range_min=-1.0,
                                     range_max=1.0)
    dino_population = genetic.init_population()
    controller = GameController(numbers_of_dino=NUMBER_OF_DINO)
    while True:
        if controller.game_is_over():
            averageScore = 0
            variance = 0
            minScore = -1
            maxScore = 0

            random.seed(None)  # Reset the seed to be pseudo-random
            dino_score = controller.get_saved_scores()
            for dino_id, dino_neurons in enumerate(dino_population):
                dino_neurons.set_score(dino_score[dino_id])
                averageScore += dino_score[dino_id]
                if dino_score[dino_id] > maxScore:
                    maxScore = dino_score[dino_id]
                if dino_score[dino_id] < minScore or minScore == -1:
                    minScore = dino_score[dino_id]
            write_best_genom(dino_population, dino_score, controller.get_nb_iteration())
            averageScore = averageScore/NUMBER_OF_DINO
            print("average score = {}".format(averageScore))
            etendue = maxScore-minScore
            for dino_id, dino_neurons in enumerate(dino_population):
                variance += (dino_score[dino_id]-averageScore)*(dino_score[dino_id]-averageScore)
            variance = variance/NUMBER_OF_DINO
            standart_deviation = sqrt(variance)
            print("standart deviation = {}".format(standart_deviation))

            ## REFLEXIVITYYY ##
            if standart_deviation > 20:
                mutate_ratio = 0    # There is a good improvement so we don't want to loose him
            elif standart_deviation < 5:
                mutate_ratio = 0.3  # we want to change something
            else:
                mutate_ratio = 0.1  # Standart

            AlgoGeneticByFunctions(population_size=NUMBER_OF_DINO,
                                   genome_size=(len(input_list) + 1) * 2,
                                   mutate_ratio=mutate_ratio,
                                   factory=DinoFactory(input_list),
                                   init_population_fun=random_uniform_init,
                                   select_mates_fun=generic_selection_couple,
                                   reproduction_fun=uniform_crossover,
                                   mutation_fun=mutation_gaussian,
                                   crossover_ratio=0.9,
                                   range_min=-1.0,
                                   range_max=1.0)



            dino_population = genetic.step_paralleled(dino_population)
            controller.restart_game(NUMBER_OF_DINO)
            random.seed(42)
        else:
            # update inputs
            game_speed.set_value(controller.get_speed() / 100.0)
            distance_next_obstacle.set_value(controller.get_distance_of_first_obstacle() / float(width))
            gap_between_obstacles.set_value(controller.get_distance_between_first_and_second_obstacle() / float(width))

            for dino_id, dino_neurons in enumerate(dino_population):
                if not controller.is_dead(dino_id) and dino_neurons.need_to_jump():
                    controller.jump(dino_id)
            time.sleep(0.01)
