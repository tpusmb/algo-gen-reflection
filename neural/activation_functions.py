#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import math
import os
import timeit
import logging.handlers

PYTHON_LOGGER = logging.getLogger(__name__)
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/activation_functions.log",
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


def sigmoid(value):
    """
    Fonction d'activation (courbe en S) pour les neurones
    :param value: las somme des produit des entrée avec poid du neuron
    :return: une valeur bornée entre 0 et 1
    """
    return 1.0 / (1.0 + math.exp(value * -4.9))


def classic_thread_shot(value):
    """
    Fonction seuil si value >= 0 on retour 1 sinon on retourn 0
    :param value: las somme des produit des entrée avec poid du neuron
    :return: 1 si value >= 0 sinon 0
    """
    return 1 if value >= 0 else 0