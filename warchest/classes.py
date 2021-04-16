#!/usr/bin/env python3

import logging as log

import json

import numpy as np

class Game(object):


    def __init__(self, player1, player2, draft='random'):
        # Board initialization
        self.board = [(x-3, y-3, x-y) for x in range(7) for y in range(7) if abs(x-y) <=3]
        self.PLAYER_1 = 0
        self.PLAYER_2 = 1

        # load data
        self._load_units()
        self._load_bases()


        # Initialize player bases, units, hands, bag, etc. ...
        self.p = [player1, player2]
        self.p[self.PLAYER_1].add_base(self.bases_map[:2])
        self.p[self.PLAYER_2].add_base(self.bases_map[-2:])
        if draft == 'random':
            self.p[self.PLAYER_1]._initialize_player(self._draw_units_draft(), self.units)
            self.p[self.PLAYER_2]._initialize_player(self._draw_units_draft(), self.units)
        elif draft == 'manual':
            assert(draft == 'random'), "Manual draft not yet implemented"
        elif type(draft) == list:
            try:
                draft_p1 = draft[:4]
                draft_p2 = draft[4:]
            except IndexError as e:
                print(f"draft variable should be list of 8 integers: {e}")

            self.p[self.PLAYER_1]._initialize_player(draft_p1, self.units)
            self.p[self.PLAYER_2]._initialize_player(draft_p2, self.units)



        # Set initiative
        self.player_turn = np.random.choice([self.PLAYER_1, self.PLAYER_2])
        self.p[self.PLAYER_1].init_available = not self.player_turn
        self.p[self.PLAYER_2].init_available = self.player_turn
        self.p[self.PLAYER_1].draw_bag_end_turn()
        self.p[self.PLAYER_2].draw_bag_end_turn()
        self.action_todo = 1
        self.initiative = 0


    def proceed_game(self):


        if self.action_todo:
            self.action_todo = 0
            return self.PLAYER_1
        else:
            self.action_todo = 1
        # Draw 1st player
            if self.p[self.player_turn].hand == []:
                self.p[self.player_turn].draw_bag_end_turn()
                change_init = not self.p[self.player_turn].init_available \
                    and not self.p[not self.player_turn].init_available
                if change_init and len(self.p[not self.player_turn].hand) == 3:
                    self.p[not self.player_turn].init_available = 1
                    self.player_turn = not self.player_turn










        # if self.player_turn == self.PLAYER_1:
        #     if self.action_todo:
        #         self.action_todo = 0
        #         return 0
        #     else:
        #         self.action_todo = 1
        #     # Draw 1st player
        #         if self.p[self.PLAYER_1].hand == []:
        #             self.p[self.PLAYER_1].draw_bag_end_turn()
        #             if not self.p[self.PLAYER_2].init_available and len(self.p[self.PLAYER_2].hand) == 3:
        #                 log.info('P1: change turn')
        #                 self.p[self.PLAYER_2].init_available = 1
        #                 self.player_turn = not self.player_turn
        # else:
        #     if self.action_todo:
        #         self.action_todo = 0
        #         return 0
        #     else:
        #         self.action_todo = 1
        #     # Draw 2nd player
        #         if self.p[self.PLAYER_2].hand == []:
        #             self.p[self.PLAYER_2].draw_bag_end_turn()
        #             if not self.p[self.PLAYER_1].init_available and len(self.p[self.PLAYER_1].hand) == 3:
        #                 log.info('P2: change turn')
        #                 self.p[self.PLAYER_1].init_available = 1
        #                 self.player_turn = not self.player_turn

        self.player_turn = not self.player_turn




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

    def render(self, p):
        info_p = f'''Player {p.name}:
        supply: {p.supply}
        bag: {p.bag}
        hand: {p.hand}
        discard: {p.discard}
        bases: {p.bases}
        '''
        print(info_p)

class Player(object):

    def __init__(self, name):
        self.name = name
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
        self.init_available = 0

    def _initialize_player(self, unit_list, unit_dictionary):
        self.unit_dictionary = unit_dictionary
        royal_seal_coin = {'id': 16,
                      'name': 'Royal seal coin',
                      'quantity': 1}
        self.unit_dictionary.append(royal_seal_coin)
        self.unit_draft = unit_list

        for unit_id in self.unit_draft:
            # fill bag
            self.bag.append(unit_id)
            self.bag.append(unit_id)
            # fill supply minus 2 card moved to the bag
            for n in range(unit_dictionary[unit_id]['quantity']-2):
                self.supply.append(unit_id)

        self.bag.append(16) # 16: Royal seal coin

    def add_base(self, base):
        [self.bases.append(b) for b in base]

    def remove_base(self, base):
        self.bases.remove(base)

    def discard2bag(self):
        self.bag = self.bag + self.discard
        self.discard = []

    def draw_bag_end_turn(self):
        n_coins = len(self.bag)
        if n_coins >= 3:
            # When drawing 3 coins in a row
            self.draw_bag(3)
            self.flag_partial_hand = 0
        else:
            # When drawing 1 or 2 coins
            self.draw_bag(n_coins)
            self.flag_partial_hand = 1

        if self.flag_partial_hand:
            self.discard2bag()
            self.draw_bag(3-len(self.hand))
            if len(self.hand) < 3:
                self.flag_partial_hand = 0
            else:
                self.flag_partial_hand = 1
        else:
            self.discard2bag()


    def draw_bag(self, n_coins):
        coins = list(np.random.choice(self.bag, n_coins, replace=False))
        for c in coins:
            self.hand.append(c)
            self.bag.remove(c)

    #######################
    ### Actions modules ###
    #######################

    def recruit(self, coin):
        # TODO: add mercenary exception
        self.hand.remove(coin)
        self.discard.append(coin)
        self.supply.remove(coin)


    def pass_move(self, coin):
        self.hand.remove(coin)
        self.discard.append(coin)

    def take_initiative(self, coin):
        self.hand.remove(coin)
        self.init_available = 0
        return 1

    def deploy(self, coin, position):
        raise NotImplementedError("This action is not yet implemented")
        # self.hand.remove(coin)



    def make_move(self):
        # Random moves for now with random coins
        i = np.random.choice(len(self.open_moves))
        move, argmove = self.open_moves[i]
        log.info('Action: '+ move.__name__ + ' with coin ' + self.unit_dictionary[argmove]['name'])
        return move(argmove) # return 1 if the player take the initiative

    def get_open_moves(self):

        # Add list of pass possibilities
        self.open_moves = [(self.pass_move, coin) for coin in self.hand]

        # Add list of initiative possibilities
        if self.init_available:
            init_moves = [(self.take_initiative, coin) for coin in self.hand]
            self.open_moves = self.open_moves + init_moves

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
