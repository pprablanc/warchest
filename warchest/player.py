import numpy as np
import logging as log

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

    def initialize_player(self, unit_list, unit_dictionary):
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



    def make_move(self, move_argmove='random'):

        if move_argmove == 'random':
            # Random moves for now with random coins
            i = np.random.choice(len(self.open_moves))
            move, argmove = self.open_moves[i]
            log.info('Player '+ self.name +': Action: '+ move.__name__ + ' with coin ' + self.unit_dictionary[argmove]['name'])
            return move(argmove) # return 1 if the player take the initiative
        elif move_argmove in self.open_moves:
            move, argmove = move_argmove
            return move(argmove) # return 1 if the player take the initiative
        else:
            raise Exception(f'move {move_argmove[0]} with {move_argmove[1]} not available')

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
