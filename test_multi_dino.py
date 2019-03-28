#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
import time

from neural import Neuron, Input

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
NUMBER_OF_DINO = 100


class DinoNeurons:

    def __init__(self, input_list):
        """

        :param input_list:
        """
        self.input_list = input_list
        self.neuron_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)
        self.neuron_no_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)

    def need_to_jump(self):

        return self.neuron_jump.compute() > self.neuron_no_jump.compute()

    def reset(self):

        self.neuron_jump = Neuron(input_liste=self.input_list, max_value=1.0, activation_function=sigmoid)
        self.neuron_no_jump = Neuron(input_liste=self.input_list, max_value=1.0, activation_function=sigmoid)


if __name__ == "__main__":
    from neural import sigmoid
    from dino_game import GameController, width

    game_speed = Input(value=0)
    distance_next_obstacle = Input(value=0)
    gap_between_obstacles = Input(value=0)
    input_list = [game_speed, distance_next_obstacle, gap_between_obstacles]

    dino_neurones_list = [DinoNeurons(input_list) for _ in range(10)]

    controller = GameController(numbers_of_dino=NUMBER_OF_DINO)
    while True:
        if controller.game_is_over():
            for dino_neurons in dino_neurones_list:
                dino_neurons.reset()
            controller.restart_game(NUMBER_OF_DINO)
        else:
            # update inputs
            game_speed.set_value(controller.get_speed() / 100.0)
            distance_next_obstacle.set_value(controller.get_distance_of_first_obstacle() / float(width))
            gap_between_obstacles.set_value(controller.get_distance_between_first_and_second_obstacle() / float(width))

            for dino_id, dino_neurons in enumerate(dino_neurones_list):

                if not controller.is_dead(dino_id) and dino_neurons.need_to_jump():
                    controller.jump(dino_id)
            time.sleep(0.1)
