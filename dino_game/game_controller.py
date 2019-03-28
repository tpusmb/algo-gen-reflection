#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
from threading import Thread
from dino_game import Game
import os
import timeit
import logging.handlers

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
    def __init__(self):
        self.game = Game()
        thread = Thread(target=self.game.game_loop, args=())
        thread.start()

    def jump(self):
        self.game.jump()

    def duck(self):
        self.game.duck()

    def stop_duck(self):
        self.game.stop_duck()

    def restart_game(self):
        self.game.restart_game()

    def get_speed(self):
        return self.game.get_speed()

    def is_ducking(self):
        return self.game.is_ducking()

    def get_distance_of_first_obstacle(self):
        return self.game.get_distance_of_first_obstacle()

    def get_distance_between_first_and_second_obstacle(self):
        return self.game.get_distance_between_first_and_second_obstacle()

    def game_is_over(self):
        return self.game.game_is_over()


if __name__ == "__main__":
    controller = GameController()
    while True:
        if controller.game_is_over():
            controller.restart_game()
        else:
            if controller.is_ducking():
                controller.stop_duck()
            else:
                controller.duck()
            controller.jump()
            time.sleep(0.1)

