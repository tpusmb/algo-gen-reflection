#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import random
import logging.handlers

from neural.input import Input

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/neuron.log",
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


class Neuron:

    def __init__(self, input_liste, activation_function):

        for given_input in input_list:
            if type(given_input) != Input:
                raise TypeError("Given input is not Type Input")

        # We append the bias node with allway +1 value
        self.input_liste = input_liste.append(Input())
        # Generate the input weight
        self.weight_liste = [random.random() for _ in range(len(self.input_liste))]
        self.activation_function = activation_function
        self.output = None

    def compute(self):
        """

        :return:
        """
        res = 0.0
        for given_input, weight in zip(input_list, self.weight_liste):
            res += given_input.get_value() * weight

        self.output = res

    def get_output(self):

        return self.output


if __name__ == "__main__":

    input_list = [1, 2, 3, 4]
    neuron = Neuron(input_list, 10)
    pass

