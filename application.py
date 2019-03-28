#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main app

Usage:
   application.py < [--manual]

Options:
    -h --help     Show this screen.
    --manual      Manual mode (you play the game)

"""

from __future__ import absolute_import

import logging.handlers
import os
import configparser

from docopt import docopt

from dino_game import start_game, Game

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


class DinoGen:

    def __init__(self, absolute_path_config_path):
        """

        :param absolute_path_config_path: (string) absolute path of the config file
        """
        pass

if __name__ == "__main__":
    args = docopt(__doc__)

    if args["--manual"]:
        start_game()
    else:
        game = Game()
        game.game_loop()
