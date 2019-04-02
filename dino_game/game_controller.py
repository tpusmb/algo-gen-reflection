#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import logging.handlers
import os
import time
from threading import Thread

from dino_game import Game

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/game_controller.log",
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


class GameController:
    """
    Class to control actions in the games
    """

    def __init__(self, numbers_of_dino):
        """
        :param numbers_of_dino: (int) number of dino to creat in the game
        """
        # Start the game
        self.game = Game(numbers_of_dino)
        # Launch the game in one thread
        thread = Thread(target=self.game.game_loop, args=())
        thread.start()

    def jump(self, dino_id):
        """
        Do jump action on the select dino
        :param dino_id:(int) id of the dino to jump id between 0 and number of dino in the game -1
        """
        self.game.jump(dino_id)

    def duck(self, dino_id):
        """
        Make the select dino ducking
        :param dino_id:(int) id of the dino to duck id between 0 and number of dino in the game -1
        """
        self.game.duck(dino_id)

    def stop_duck(self, dino_id):
        """
        stop the select dino to duck
        :param dino_id:(int) id of the dino to stop ducking id between 0 and number of dino in the game -1
        """
        self.game.stop_duck(dino_id)

    def is_ducking(self, dino_id):
        """
        Get if the select dino is ducking
        :param dino_id:(int) id of the dino to get if is ducking id between 0 and number of dino in the game -1
        :return: (bool) True the dino is dunking else False
        """
        return self.game.is_ducking(dino_id)

    def is_dead(self, dino_id):
        """

        :param dino_id:
        :return:
        """
        self.game.dino_is_dead(dino_id)

    def restart_game(self, numbers_of_dino):
        self.game.restart_game(numbers_of_dino)

    def get_speed(self):
        return self.game.get_speed()

    def get_high_score(self):
        return self.game.get_high_score()

    def get_nb_iteration(self):
        return self.game.get_nb_iteration()

    def get_distance_of_first_obstacle(self):
        return self.game.get_distance_of_first_obstacle()

    def get_distance_between_first_and_second_obstacle(self):
        return self.game.get_distance_between_first_and_second_obstacle()

    def game_is_over(self):
        return self.game.game_is_over()

    def get_saved_scores(self):
        """

        :return:(dict) key dino id value score
        """
        return self.game.get_saved_scores()


if __name__ == "__main__":
    controller = GameController(2)
    while True:
        if controller.game_is_over():
            controller.restart_game(2)
        else:
            if controller.is_ducking(1):
                controller.stop_duck(1)
            else:
                controller.duck(1)
            controller.jump(1)
            time.sleep(0.1)
