#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import timeit
import logging.handlers

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/input.log",
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


class Input:

    def __init__(self, value=1):
        """

        :param value: Value between 0 and 1
        """
        if value > 1 or value < 0:
            raise ValueError("The given value not between 0 and 1")
        self.value = value

    def get_value(self):
        return self.value

    def set_value(self, value):
        """

        :param value: value between 0 and 1
        :return:
        """
        if value > 1:
            value = 1.0
        elif value < 0:
            value = 0.0
        self.value = value
