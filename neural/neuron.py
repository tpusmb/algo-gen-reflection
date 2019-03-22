#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import random
import logging.handlers
from neural import Input

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

    def __init__(self, input_liste, max_value, activation_function):

        for given_input in input_liste:
            if type(given_input) != Input:
                raise TypeError("Given input is not Type Input")

        # We append the bias node with allway +1 value
        self.input_liste = input_liste
        # Generate the input weight + 1 we ad the bias node
        self.weight_liste = [random.uniform(-max_value, max_value) for _ in range(len(self.input_liste) + 1)]
        # Add the bias node
        self.activation_function = activation_function
        self.threshold = len(self.input_liste) * self.weight_liste[-1]

    def compute(self):
        """

        :return:
        """
        res = -self.threshold
        for given_input, weight in zip(input_list, self.weight_liste):
            res += given_input.get_value() * weight

        return self.activation_function(res)


if __name__ == "__main__":
    from neural import classic_thread_shot
    a = Input(0)
    b = Input(0)
    input_list = [a, b]
    neuron = Neuron(input_list, 1.0, classic_thread_shot)
    neuron.compute()
    print("dd")
