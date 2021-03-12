#!/usr/bin/env python3

import pandas as pd
import random

class board(object):

    def __init__(self):
        self._board_initialization()

    def _board_initialization(self):
        filename = 'board.csv'
        try:
            self.hexagon = pd.read_csv(filename, sep='\t')
        except:
            print("board.csv file was not found.")

    # other function interacting with players ?

class player(object):

    def __init__(self, remaining_unit_list):
        self.units = self._load_units()
        (self.unit_set, self.remaining_unit_list) = self._random_unit_set(remaining_unit_list)

    def _load_units():
        filename = 'units.csv'
        try:
            units = pd.read_csv(filename, sep='\t')
        except:
            print("units.csv file was not found.")

    def _random_unit_set(self, remaining_unit_list):
        if remaining_unit_list:
            unit_list = remaining_unit_list
        else:
            unit_list = list(self.units['id_unit'])
        unit_set = random.sample(unit_list, 4)
        remaining_unit_list = list(set(unit_list) - set(unit_set))
        return (unit_set, remaining_unit_list)
