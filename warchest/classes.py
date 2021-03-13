#!/usr/bin/env python3

import pandas as pd
import random

class Game(object):

    def __init__(self, player1, player2, draft='random'):
        # load data
        self._board_initialization()
        self._load_units()

        # make draft
        if draft == 'random':
            (units_draft, remaining_units) = self._random_unit_draft()
            player1.set_unit_draft(units_draft)
            (units_draft, _) = self._random_unit_draft(remaining_units)
            player2.set_unit_draft(units_draft)
        else:
            assert(draft == 'random'), "Manual draft not yet implemented"

        # initialize supply


        # Set initiative
        self.initiative = random.randint(0, 1) # 0: Player 2 has initiative
        self.player_turn = self.initiative
        self.state = 'hand'

    def proceed_game(self, last_state):
    #def next_turn ?(self, ):
        while(1):
            if self.state == 'hand':
                pass
                # check if any hand is empty
                # if empty, move to bag
                # else move to initiative
            elif self.state == 'bag':
                pass
                # check if bag is empty
                # if empty, fill the bag with discard
                # else move to initiative
            elif self.state == 'initiative':
                self.player_turn = self.initiative
                self.state = 'play'
            elif self.state == 'draw':
                pass
            elif self.state == 'play':
                self.state = 'win'
                # turn is played outside this module
                return self.player_turn
            elif self.state == 'win':
                if self.player_turn == self.initiative:
                    self.player_turn = not self.player_turn
                    self.state ='play'
                else:
                    self.state = 'hand'



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

    def _random_unit_draft(self, remaining_units=pd.DataFrame()):
        if remaining_units.empty:
            remaining_units = self.units
        units_draft = remaining_units.sample(4)
        remaining_units = self.units[~self.units['id'].isin(units_draft['id'])]
        return (units_draft, remaining_units)

    # other function interacting with players ?

class Player(object):

    def __init__(self):
        self.unit_draft = []
        self.hand = []
        self.supply = []
        self.discard = []
        self.eliminated = []
        self.bag = []

    def set_unit_draft(self, unit_list):
        self.unit_draft = unit_list

    def set_supply(self, units, unit_draft):
        pass

    def draw(self):
        pass

    def make_action(self):
        pass

    def get_open_moves(self):
        pass
