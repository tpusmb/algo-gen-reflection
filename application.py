#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main app

Usage:
   application.py <config-abs-path> [--manual]

Options:
    -h --help           Show this screen.
    --manual            Manual mode (you play the game)
    <config-abs-path>   Absolute path to the .ini config file

"""

from __future__ import absolute_import

import configparser
import json
import logging.handlers
import os
import time

from docopt import docopt
from math import sqrt

from dino_game import GameController, width
from genetic import Individual
from genetic.algo_genetic_by_functions import *
from genetic.individual import genome, IndividualFactory
from neural import sigmoid, Input, Neuron

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/application.log",
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


class ConfigReader:

    def __init__(self, absolute_path_config_file):
        """

        :param absolute_path_config_file:
        """
        self.config = configparser.ConfigParser()
        try:
            self.config.read(absolute_path_config_file)
        except Exception as e:
            raise FileExistsError("Error to read the config file: {}".format(e))

        try:
            self.__dict__.update(self.config)
        except Exception as e:
            PYTHON_LOGGER.error("Error to load the configurations: {}".format(e))


class DinoNeurons(Individual):

    def __init__(self, input_list, gen: genome):
        """

        :param input_list:
        """
        super().__init__(gen)
        self.input_list = input_list
        self.neuron_jump = Neuron(input_liste=input_list, max_value=5.0, activation_function=sigmoid)
        self.neuron_no_jump = Neuron(input_liste=input_list, max_value=5.0, activation_function=sigmoid)

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


class DinoGen:

    def __init__(self, config_reader):
        """

        :param config_reader: (ConfigReader)
        """
        self.game_speed = Input(value=0)
        self.distance_next_obstacle = Input(value=0)
        self.gap_between_obstacles = Input(value=0)
        self.config_reader = config_reader
        self.input_list = [self.game_speed, self.distance_next_obstacle, self.gap_between_obstacles]
        self.population_size = self.config_reader.General.getint("population_size")
        self.genetic = AlgoGeneticByFunctions(population_size=self.population_size,
                                              genome_size=(len(self.input_list) + 1) * 2,
                                              mutate_ratio=config_reader.Genetic.getfloat("mutate_ratio"),
                                              factory=DinoFactory(self.input_list),
                                              init_population_fun=eval(config_reader.Genetic["init_population_fun"]),
                                              select_mates_fun=eval(config_reader.Genetic["select_mates_fun"]),
                                              reproduction_fun=eval(
                                                  config_reader.Genetic["reproduction_fun"]),
                                              mutation_fun=eval(config_reader.Genetic["mutation_fun"]),
                                              crossover_ratio=config_reader.Genetic.getfloat("crossover_ratio"),
                                              range_min=-1.0,
                                              range_max=1.0)
        self.dino_population = self.genetic.init_population()
        self.app_finish = False
        self.variance = 0
        self.average_score = 0
        self.min_score = 0
        self.max_score = 0
        self.ecart_type = 0
        self.best_dino_id = None
        self.hight_score = -1

    @staticmethod
    def write_best_genom(dino_to_save, score_best_dino, nb_iteration):

        data = {'score': score_best_dino, 'genom': dino_to_save.genome}
        with open('best_score{}.txt'.format(nb_iteration), 'w') as outfile:
            json.dump(data, outfile)

    def state_analyse(self, dino_score):
        """

        :param dino_score: (list of int) all score of the dino population
        :return:
        """
        self.average_score = 0
        self.variance = 0
        self.min_score = -1
        self.max_score = 0
        self.ecart_type = 0
        for dino_id, dino_neurons in enumerate(self.dino_population):
            self.average_score += dino_score[dino_id]
            if dino_score[dino_id] > self.max_score:
                self.max_score = dino_score[dino_id]
                self.best_dino_id = dino_id
            if dino_score[dino_id] < self.min_score or self.min_score == -1:
                self.min_score = dino_score[dino_id]

        for dino_id, dino_neurons in enumerate(self.dino_population):
            self.variance += (dino_score[dino_id] - self.average_score) * (dino_score[dino_id] - self.average_score)

        self.average_score = self.average_score / self.population_size
        self.variance = self.variance / self.population_size
        self.ecart_type = sqrt(self.variance)
        PYTHON_LOGGER.info("Average score = {}".format(self.average_score))
        PYTHON_LOGGER.info("Ecart type = {}".format(self.ecart_type))
        PYTHON_LOGGER.info("Max Score = {}".format(self.max_score))
        PYTHON_LOGGER.info("Min Score = {}".format(self.min_score))
        PYTHON_LOGGER.info("Best Dino id = {}".format(self.best_dino_id))

    def run(self):

        controller = GameController(numbers_of_dino=self.population_size)

        while True:
            if controller.game_is_over():

                PYTHON_LOGGER.info("****End of iteration {}****".format(controller.get_nb_iteration()))
                dino_score = controller.get_saved_scores()
                for dino_id, dino_neurons in enumerate(self.dino_population):
                    dino_neurons.set_score(dino_score[dino_id])

                self.state_analyse(dino_score)
                if self.max_score > self.hight_score:
                    self.hight_score = self.max_score
                    self.write_best_genom(self.dino_population[self.best_dino_id], dino_score[self.best_dino_id],
                                          controller.get_nb_iteration())
                if self.config_reader.General.getboolean('use_multi_thread'):
                    self.dino_population = self.genetic.step_paralleled(self.dino_population)
                else:
                    self.dino_population = self.genetic.step(self.dino_population)
                controller.restart_game(self.population_size)
            else:
                # update inputs
                self.game_speed.set_value(controller.get_speed() / 100.0)
                self.distance_next_obstacle.set_value(controller.get_distance_of_first_obstacle() / float(width))
                self.gap_between_obstacles.set_value(
                    controller.get_distance_between_first_and_second_obstacle() / float(width))

                for dino_id, dino_neurons in enumerate(self.dino_population):
                    if not controller.is_dead(dino_id) and dino_neurons.need_to_jump():
                        controller.jump(dino_id)
                time.sleep(0.01)

    def stop(self):

        self.app_finish = True


if __name__ == "__main__":
    args = docopt(__doc__)
    config = ConfigReader(args["<config-abs-path>"])
    dino_gen = DinoGen(config)
    dino_gen.run()
