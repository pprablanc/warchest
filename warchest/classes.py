#!/usr/bin/env python3

import logging as log

import json

import pandas as pd
import numpy as np

class Game(object):
    # TODO: Replace csv by json, pandas by list of dicts

    def __init__(self, player1, player2, draft='random'):
        # load data
        self.board = []
        self.units = []
        self.available_units = []
        self._board_initialization()
        self._load_units()

        # Initialize player units, hands, bag, etc. ...
        self.p1 = player1
        self.p2 = player2
        if draft == 'random':
            player1._initialize_player(self._draw_units_draft(), self.units)
            player2._initialize_player(self._draw_units_draft(), self.units)
        else:
            assert(draft == 'random'), "Manual draft not yet implemented"

        # Set initiative
        self.initiative = np.random.randint(0, 1) # if 0: Player 2 has initiative
        self.player_turn = self.initiative
        self.state = 'hand'

    def proceed_game(self):
    #def next_turn ?(self, ):
        while(1):
            # TODO: Not finished yet. Continue when "action" methods are written in Player object
            if self.state == 'hand':
                # check if any hand is empty
                # if empty, move to bag
                # else move to initiative
                if self.p1.hand == [] or self.p2.hand == []:
                    self.state = 'draw'
                else:
                    self.state = 'initiative'

            elif self.state == 'bag':
                # check if bag is empty
                # if empty, fill the bag with discard and finish draw if necessary
                # else move to initiative
                if self.p1.bag == []:
                    self.p1.discard2bag()
                    self.state = 'draw'
                elif self.p2.bag == []:
                    self.p2.discard2bag()
                    self.state = 'draw'
                else:
                    self.state = 'draw'

            elif self.state == 'initiative':
                self.player_turn = self.initiative
                self.state = 'play'

            elif self.state == 'draw':
                # Draw from state hand (empty hand)
                # Or draw when incomplete hand
                if self.p1.hand == []:
                    if self.p1.draw_bag_multiple():
                        self.state = 'bag'
                elif self.p2.hand == []:
                    if self.p2.draw_bag_multiple():
                        self.state = 'bag'
                else:
                    self.state = 'play'

            elif self.state == 'play':

                print('Play action')
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
        # TODO: x,y,z implementation of the board.
        filename = '../resources/board.csv'
        try:
            self.board = pd.read_csv(filename, sep='\t')
        except:
            print("board.csv file was not found.")

    def _load_units(self):
        filename = '../resources/units.json'
        try:
            with open(filename, 'r') as f:
                self.units = json.load(f)
                self.available_units = np.arange(len(self.units))
        except:
            print("units.json file was not found.")

    def _draw_units_draft(self, n_units=4):
        units_draft = np.random.choice(self.available_units, n_units, replace=False)
        for i in units_draft:
            self.available_units = np.delete(self.available_units, np.where(self.available_units==i))
        return units_draft

class Player(object):

    def __init__(self):
        self.unit_dictionary = []
        self.unit_draft = []
        self.hand = []
        self.supply = []
        self.discard = []
        self.eliminated = []
        self.bag = []

    def _initialize_player(self, unit_list, unit_dictionary):
        self.unit_dictionary = unit_dictionary
        self.unit_draft = unit_list

        for unit_id in self.unit_draft:
            # fill bag
            self.bag.append(unit_id)
            self.bag.append(unit_id)
            # fill supply minus 2 card moved to the bag
            for n in range(unit_dictionary[unit_id]['quantity']-2):
                self.supply.append(unit_id)

        self.bag.append(16) # 16: Royal coin

    def discard2bag(self):
        assert(self.bag.empty())
        self.bag = self.discard[:]

    def draw_bag_multiple(self):
        n_coins = len(self.bag)
        if self.hand:
            self.draw_bag(3-len(self.hand))
            return 1
        elif n_coins >= 3:
            self.draw_bag(3)
            return 1
        else:
            self.draw_bag(n_coins)
            return 0

    def draw_supply(self, unit):
        self.discard.append(unit)
        self.supply.remove(unit)

    def draw_bag(self, n_coins):
        coins = list(np.random.choice(self.bag, n_coins, replace=False))
        for c in coins:
            self.hand.append(c)
            self.bag.remove(c)

    def recruit(self, id):
        pass


    def make_action(self):
        pass

    def get_legal_actions(self, game):

        # First filter
        self.open_moves = ['pass']

        if 'royal-seal' in list(self.bag['name']):
            self.open_moves.append('initiative')

        if self.supply['quantity'].sum() > 0:
            self.open_moves.append('recruit')

        # Filter based on hand and board state
        # After the basics, implement tactics

        # Based on first filter, exhaustive search of legal actions
