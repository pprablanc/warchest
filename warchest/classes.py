#!/usr/bin/env python3

import logging as log

import json

import pandas as pd
import numpy as np

class Game(object):

    global PLAYER_1
    global PLAYER_2
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self, player1, player2, draft='random'):
        # Board initialization
        self.board = [(x-3, y-3, x-y) for x in range(7) for y in range(7) if abs(x-y) <=3]

        # load data
        self._load_units()
        self._load_bases()


        # Initialize player bases, units, hands, bag, etc. ...
        self.p1 = player1
        self.p1.add_base(self.bases_map[:2])
        self.p2 = player2
        self.p2.add_base(self.bases_map[-2:])
        if draft == 'random':
            player1._initialize_player(self._draw_units_draft(), self.units)
            player2._initialize_player(self._draw_units_draft(), self.units)
        elif draft == 'manual':
            assert(draft == 'random'), "Manual draft not yet implemented"
        elif type(draft) == list:
            try:
                draft_p1 = draft[:4]
                draft_p2 = draft[4:]
            except IndexError as e:
                print(f"draft variable should be list of 8 integers: {e}")

            player1._initialize_player(draft_p1, self.units)
            player2._initialize_player(draft_p2, self.units)



        # Set initiative
        self.initiative = np.random.randint(PLAYER_1, PLAYER_2) # if 0: Player 2 has initiative
        self.player_turn = self.initiative
        self.state = 'hand'

    def proceed_game(self):
        while 1:
            # TODO: Not finished yet. Continue when "action" methods are written in Player object

            if self.state == 'hand':
                # check if any hand is empty
                # if empty, move to bag
                # else move to initiative
                if self.p1.hand == [] or self.p2.hand == []:
                    log.info('Move to draw state.')
                    self.state = 'draw'
                else:
                    log.info('Move to initiative state.')
                    self.state = 'play'



            elif self.state == 'bag':
                # check if bag is empty
                # if empty, fill the bag with discard and finish draw if necessary
                # else move to initiative
                if self.p1.bag == []:
                    self.p1.discard2bag()
                    log.info('p1 move discard to bag.')
                elif self.p2.bag == []:
                    self.p2.discard2bag()
                    log.info('p2 move discard to bag.')
                log.info('Move to draw state.')
                self.state = 'draw'

            # elif self.state == 'initiative':
            #     self.player_turn = self.initiative
            #     log.info(f'Player {self.player_turn + 1} has initiative')
            #     self.state = 'play'



            elif self.state == 'draw':
                # Draw from state hand (empty hand)
                # Or draw when incomplete hand
                if self.p1.hand == [] or self.p1.flag_partial_hand:
                    if self.p1.draw_bag_multiple():
                        self.state = 'bag'
                elif self.p2.hand == [] or self.p2.flag_partial_hand:
                    if self.p2.draw_bag_multiple():
                        self.state = 'bag'
                else:
                    self.state = 'play'

                # Change initiative when it occurs
                if self.initiative == PLAYER_1:
                    self.player_turn = PLAYER_1
                else:
                    self.player_turn = PLAYER_2



            elif self.state == 'play':

                if self.player_turn == PLAYER_1:
                    self.p1.get_open_moves()
                    self.p1.make_move()
                    log.info('Player 1 turn')
                elif self.player_turn == PLAYER_2: # Not necessary but for readability
                    self.p2.get_open_moves()
                    self.p2.make_move()
                    log.info('Player 2 turn')
                self.state = 'win'
                # TODO: Uncomment the break when RL part is ready
                # break



            elif self.state == 'win':
                if len(self.p1.bases) > 5:
                    log.info('Player 1 win the game.')
                    break
                elif len(self.p2.bases) > 5:
                    log.info('Player 2 win the game.')
                    break
                else:
                    self.player_turn = not self.player_turn
                    self.state = 'hand'
            self.render()


    def _load_units(self):
        filename = 'resources/units.json'
        try:
            with open(filename, 'r') as f:
                self.units = json.load(f)
                self.available_units = np.arange(len(self.units))
        except:
            print("units.json file was not found.")


    def _load_bases(self):
        filename = 'resources/bases.json'
        try:
            with open(filename, 'r') as f:
                self.bases_map = json.load(f)
        except:
            print("bases.json file was not found.")

    def _draw_units_draft(self, n_units=4):
        units_draft = np.random.choice(self.available_units, n_units, replace=False)
        for i in units_draft:
            self.available_units = np.delete(self.available_units,
                                             np.where(self.available_units == i)
                                             )
        return units_draft

    def render(self):
        print(f'Next state: {self.state}')
        info_p1 = f'''Player 1:
        supply: {self.p1.supply}
        bag: {self.p1.bag}
        hand: {self.p1.hand}
        discard: {self.p1.discard}
        bases: {self.p1.bases}
        '''
        print(info_p1)
        info_p2 = f'''Player 2:
        supply: {self.p2.supply}
        bag: {self.p2.bag}
        hand: {self.p2.hand}
        discard: {self.p2.discard}
        bases: {self.p2.bases}
        '''
        print(info_p2)

class Player(object):

    def __init__(self):
        self.unit_dictionary = []
        self.unit_draft = []
        self.hand = []
        self.supply = []
        self.discard = []
        self.eliminated = []
        self.bag = []
        self.bases = []
        self.flag_partial_hand = 0
        self.open_moves= []

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

    def add_base(self, base):
        [self.bases.append(b) for b in base]

    def remove_base(self, base):
        self.bases.remove(base)

    def discard2bag(self):
        self.bag = self.bag + self.discard
        self.discard = []

    def draw_bag_multiple(self):
        """
        returns:
                0: Drawing complete
                1: Drawing incomplete
        """
        n_coins = len(self.bag)
        if self.hand:
            # When finishing drawing after partial draw
            self.draw_bag(3-len(self.hand))
            self.flag_partial_hand = 0
            return 0
        elif n_coins >= 3:
            # When drawing 3 coins in a row
            self.draw_bag(3)
            self.flag_partial_hand = 0
            return 0
        else:
            # When drawing 1 or 2 coins
            self.draw_bag(n_coins)
            self.flag_partial_hand = 1
            return 1

    def draw_bag(self, n_coins):
        coins = list(np.random.choice(self.bag, n_coins, replace=False))
        for c in coins:
            self.hand.append(c)
            self.bag.remove(c)

    #######################
    ### Actions modules ###
    #######################

    def recruit(self, coin):
        self.hand.remove(coin)
        self.discard.append(coin)
        self.supply.remove(coin)
        return 0


    def pass_move(self, coin):
        self.hand.remove(coin)
        self.discard.append(coin)
        return 0

    def take_initiative(self, coin):
        self.hand.remove(coin)
        self.initiative
        return 1


    def make_move(self):
        # Random moves for now
        i = np.random.choice(len(self.open_moves))
        move, argmove = self.open_moves[i]
        move(argmove)

    def get_open_moves(self):

        # Add list of pass possibilities
        self.open_moves = [(self.pass_move, coin) for coin in self.hand]

        # # Add list of initiative possibilities
        # self.open_moves = self.open_moves + [(self.take_initiative)]

        # if len(self.supply) > 0:
        #     self.open_moves.append('recruit')

        # Filter based on hand and board state
        # After the basics, implement tactics

        # Based on first filter, exhaustive search of legal actions

# Useful functions for later to get neighbors boxes
def neighbors_1(x, y, z):
    res = set()
    for i in [-1, 1]:
        res.update({(x, y-i, z+i), (x+i, y+i, z), (x+i, y, z+i)})
    return {box for box in res if box in board}


def neighbors_2(x, y, z):
    res = set()
    for a, b, c in neighbors_1(x, y, z):
        res.update(neighbors_1(a, b, c))
    res.discard((x, y, z))
    return {box for box in res if box in board}
