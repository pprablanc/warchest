import numpy as np
import logging as log

class Player(object):

    def __init__(self, name, board, playerId):
        self.name = name
        self.board = board
        self.playerId = playerId
        self.unit_index = []
        self.unit_draft = []
        self.action_features_map = {}
        self.action_vector = []

        self.hand = []
        self.supply = []
        self.discard = Discard()
        self.eliminated = []
        self.bag = []

        self.flag_partial_hand = 0
        self.open_moves = []
        self.chosen_move = None
        self.init_available = 0
        self.open_moves = []
        self.royal_seal_coin = {'coinId': 16,
                      'name': 'Royal seal coin',
                      'quantity': 1}


    def initialize_player(self, unit_list, unit_index):
        self.set_unit_index(unit_index)
        self.set_bag_supply(unit_list)
        self.initialize_action_vector()

    def set_unit_index(self, unit_index):
        self.unit_index = unit_index[:]
        self.unit_index.append(self.royal_seal_coin)

    def set_bag_supply(self, unit_list):
        self.unit_draft = unit_list

        for unit_id in self.unit_draft:
            # fill bag
            self.bag.append(unit_id)
            self.bag.append(unit_id)
            # fill supply minus 2 card moved to the bag
            for _ in range(self.unit_index[unit_id]['quantity']-2):
                self.supply.append(unit_id)

        self.bag.append(self.royal_seal_coin['coinId'])

    def initialize_action_vector(self):
        n_uniq_coins = len(self.unit_index)
        n_units = n_uniq_coins - 1
        n_bases = len(self.board.bases)
        n_hexagons = len(self.board.board)

        list_action_args = [
            [self.pass_move, n_uniq_coins],
            [self.recruit, n_units, n_uniq_coins],
            [self.take_initiative, n_uniq_coins],
            [self.deploy, n_units, n_bases],
            [self.move_unit, n_units, n_hexagons, n_hexagons],
            [self.control, n_units, n_hexagons]
        ]

        offset = 0
        for elt in list_action_args:
            action = elt[0]
            self.action_features_map[action] = {
                'offset': offset,
                'args': elt[1:]
            }
            offset = offset + sum(elt[1:])

        self.action_vector = offset * [0]

    def get_action_vector(self):
        self.action_vector = [0 for elt in self.action_vector]
        action = self.chosen_move[0]
        args = self.chosen_move[1:]
        for arg in args:
            offset = self.action_features_map[action]['offset']
            arg = self.board.board[arg]['hexId'] if isinstance(arg, tuple) else arg
            self.action_vector[offset+arg] = 1

    def discard2bag(self):
        self.bag = self.bag + self.discard.empty()

    def hand2discard(self, coin, masked):
        self.hand.remove(coin)
        self.discard.append(coin, masked=masked)

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
        elif self.bag == []:
            self.discard2bag()


    def draw_bag(self, n_coins):
        # import pdb; pdb.set_trace()
        coins = list(np.random.choice(self.bag, n_coins, replace=False))
        for c in coins:
            self.hand.append(c)
            self.bag.remove(c)


    #######################
    ### Actions modules ###
    #######################

    def pass_move(self, args):
        coin = args[0]
        # print('pass')
        self.hand2discard(coin, masked=True)

    def take_initiative(self, args):
        coin = args[0]
        # print('take_init')
        self.hand2discard(coin, masked=True)
        self.init_available = 0

    def recruit(self, args):
        # TODO: add mercenary exception
        r_coin = args[0]
        h_coin = args[1]
        # print('recruit')
        self.hand2discard(h_coin, masked=True)
        self.discard.append(r_coin, masked=False)
        self.supply.remove(r_coin)

    def deploy(self, args):
        coin = args[0]
        hexagon = args[1]
        # print('deploy')
        self.hand.remove(coin)
        self.board.board[hexagon]['coinId'] = coin
        self.board.board[hexagon]['number'] = self.board.board[hexagon]['number'] + 1
        self.board.units_deployed[coin] = hexagon

    def move_unit(self, args):
        # TODO: add footman exception move 2 units
        coin = args[0]
        hexagon_source = args[1]
        hexagon_target = args[2]
        # print('move')

        # Update board
        self.board.board[hexagon_target]['coinId'] = self.board.board[hexagon_source]['coinId']
        self.board.board[hexagon_target]['number'] = self.board.board[hexagon_source]['number']
        self.board.board[hexagon_source]['coinId'] = None
        self.board.board[hexagon_source]['number'] = 0

        # Update quick access deployed units
        self.board.units_deployed[coin] = hexagon_target

        self.hand2discard(coin, masked=False)

    def attack(self, args):
        raise NotImplementedError

    def control(self, args):
        coin = args[0]
        hexagon = args[1]
        # print('control')

        self.board.add_base(hexagon, self.playerId)
        self.board.inc_base_count(self.playerId)
        self.hand2discard(coin, masked=False)

    def bolster(self, args):
        raise NotImplementedError


    ############################
    ### Parse action modules ###
    ############################


    def parse_pass(self):
        '''
        Add list of pass possibilities
        '''
        pass_moves = [(self.pass_move, coin) for coin in self.hand]
        self.open_moves = self.open_moves + pass_moves

    def parse_init(self):
        '''
        Add list of initiative possibilities
        '''
        if self.init_available:
            init_moves = [(self.take_initiative, coin) for coin in self.hand]
            self.open_moves = self.open_moves + init_moves

    def parse_recruit(self):
        '''
        Add list of recruit possibilities
        '''
        if len(self.supply) > 0:
            recruit_moves = [(self.recruit, s_coin, h_coin)
                             for s_coin in self.supply
                             for h_coin in self.hand]
            self.open_moves = self.open_moves + recruit_moves

    def parse_deploy(self):
        '''
        Add list of deploy possibilities
        '''
        # TODO: add footman exception (in the board ?)
        a_f_b = self.board.available_friendly_bases(self.playerId)
        hand = [c for c in self.hand if c != self.royal_seal_coin['coinId']]
        if a_f_b:
            deploy_moves = [(self.deploy, coin, hexagon)
                            for coin in hand
                            for hexagon in a_f_b
                            if not self.board.check_unit_deployed(coin)]
            self.open_moves = self.open_moves + deploy_moves

    def parse_move(self):
        '''
        Add list of move possibilities
        TODO: Footman exception
        '''
        move_moves = []
        for c in self.hand:
            for coinId, hexagon in self.board.units_deployed.items():
                if c == coinId:
                    neighbors = self.board.neighbors_1(hexagon)
                    if neighbors:
                        tmp = [(self.move_unit, c, hexagon, n)
                            for n in neighbors if self.board.board[n]['coinId'] is None]
                        move_moves = move_moves + tmp
        self.open_moves = self.open_moves + move_moves


    def parse_control(self):
        '''
        Add list of control possibilities
        '''
        unit_hex_on_base = [(unitId, hexagon) for unitId, hexagon in self.board.units_deployed.items()
                        if (hexagon in self.board.bases.keys())
                        and (self.board.bases[hexagon] != self.playerId)
                        and (unitId in self.hand)]

        control_moves = [(self.control, elt[0], elt[1]) for elt in unit_hex_on_base]
        self.open_moves = self.open_moves + control_moves


    def get_open_moves(self):

        self.open_moves = []

        self.parse_pass()
        self.parse_init()
        self.parse_recruit()
        self.parse_deploy()
        self.parse_move()
        self.parse_control()


    def make_move(self, move_argmove='random'):

        if move_argmove == 'random':
            # Random moves for now with random coins
            i = np.random.choice(len(self.open_moves))
            move = self.open_moves[i][0]
            argmove = self.open_moves[i][1:]
            # log.info('Player '+ self.name +': Action: '+ move.__name__ + ' with coin ' + self.unit_index[argmove]['name'])
            log.info('Player '+ self.name +': Action: '+ move.__name__)
            self.chosen_move = self.open_moves[i]
            return move(argmove) # return 1 if the player take the initiative
        elif move_argmove in self.open_moves:
            move = move_argmove[0]
            argmove = move_argmove[1:]
            return move(argmove) # return 1 if the player take the initiative
        else:
            raise Exception(f'move {move_argmove[0]} with {move_argmove[1]} not available')




class Discard(object):

    def __init__(self):
        self.discard = []

    def append(self, coin, masked):
        self.discard.append(
            {
                'coinId': coin,
                'masked': masked
            }
        )

    def empty(self):
        ret = [coin['coinId'] for coin in self.discard]
        self.discard = []
        return ret

