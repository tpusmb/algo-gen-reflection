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

if __name__ == "__main__":
    from neural import sigmoid
    from dino_game import GameController, width

    game_speed = Input(value=0)
    distance_next_obstacle = Input(value=0)
    gap_between_obstacles = Input(value=0)
    input_list = [game_speed, distance_next_obstacle, gap_between_obstacles]
    neuron_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)
    neuron_no_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)

    controller = GameController(numbers_of_dino=1)
    while True:
        if controller.game_is_over():
            neuron_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)
            neuron_no_jump = Neuron(input_liste=input_list, max_value=1.0, activation_function=sigmoid)
            controller.restart_game()
        else:
            game_speed.set_value(controller.get_speed() / 100.0)
            distance_next_obstacle.set_value(controller.get_distance_of_first_obstacle() / float(width))
            gap_between_obstacles.set_value(controller.get_distance_between_first_and_second_obstacle() / float(width))
            if neuron_jump.compute() > neuron_no_jump.compute():
                controller.jump(dino_id=0)
            time.sleep(0.1)
