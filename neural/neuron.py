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
        """

        :param input_liste: (list of Inputs) Input for the neuron
        :param max_value: (float) Max value for the weight
        :param activation_function: (function with one parameter)
                Activation function see the activation_function.py file
        """
        for given_input in input_liste:
            if type(given_input) != Input:
                raise TypeError("Given input is not Type Input")

        # We append the bias node with allway +1 value
        self.input_liste = input_liste
        # Generate the input weight
        self.weight_liste = [random.uniform(-max_value, max_value) for _ in range(len(self.input_liste))]
        # Add the bias node
        self.activation_function = activation_function
        self.bias_weight = random.uniform(-max_value, max_value)
        self.threshold = len(self.input_liste) * self.bias_weight

    def get_weight_len(self):
        """

        :return:
        """
        #  + 1 for the bias
        return len(self.input_liste) + 1

    def set_threshold(self, bias_weight):
        """

        :return:
        """
        self.bias_weight = bias_weight
        self.threshold = len(self.input_liste) * self.bias_weight

    def compute(self):
        """
        Compute the neurone with the input list and use the activation function
        :return:(float) Out put of the neurone
        """
        # Set bias node
        res = -self.threshold
        for given_input, weight in zip(self.input_liste, self.weight_liste):
            res += given_input.get_value() * weight
        return self.activation_function(res)


if __name__ == "__main__":
    from neural import classic_thread_shot
    # Creat inputs
    a = Input(value=0)
    b = Input(value=0)
    # Set in the list
    input_list = [a, b]
    # Give the pointer if the inputs
    neuron = Neuron(input_liste=input_list, max_value=1.0, activation_function=classic_thread_shot)
    print(neuron.compute())
