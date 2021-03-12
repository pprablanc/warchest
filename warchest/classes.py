#!/usr/bin/env python3

import pandas as pd
import random

class Board(object):

    def __init__(self, player1, player2, draft='random'):
        # load data
        self._board_initialization()
        self._load_units()

        # make draft
        if draft == 'random':
            (unit_set, remaining_unit_list) = self._random_unit_set()
            player1.set_unit_set(unit_set)
            (unit_set, _) = self._random_unit_set(remaining_unit_list)
            player2.set_unit_set(unit_set)
        else:
            assert(draft == 'random'), "Manual draft not yet implemented"

        # Set initiative
        self.initiative = random.randint(0, 1) # 0: Player 2 has initiative


    def _board_initialization(self):
        filename = '../resources/board.csv'
        try:
            self.hexagon = pd.read_csv(filename, sep='\t')
        except:
            print("board.csv file was not found.")

    def _load_units(self):
        filename = '../resources/units.csv'
        try:
            self.units = pd.read_csv(filename, sep='\t')
        except:
            print("units.csv file was not found.")

    def _random_unit_set(self, remaining_unit_list=[]):
        if remaining_unit_list:
            unit_list = remaining_unit_list
        else:
            unit_list = list(self.units['id'])
        unit_set = random.sample(unit_list, 4)
        remaining_unit_list = list(set(unit_list) - set(unit_set))
        return (unit_set, remaining_unit_list)

    # other function interacting with players ?

class Player(object):

    def __init__(self):
        self.unit_set = []

    def set_unit_set(self, unit_list):
        self.unit_set = unit_list
