'''
Board class
'''
import logging as log
import json

class Board(object):

    def __init__(self):
        self.board = {}
        self.units_deployed = {}
        self.hexagons = {}
        self.bases = {}
        self.base_count = [0, 0]
        self._load_bases()
        self._load_board()

    def _load_bases(self):
        filename_bases = 'resources/bases.json'
        try:
            with open(filename_bases, 'r') as f:
                bases = json.load(f)
                self.bases= {tuple(base): -1 for base in bases}
        except FileNotFoundError:
            print("bases.json file was not found.")

    def _load_board(self):
        filename_board = 'resources/board.json'
        try:
            with open(filename_board, 'r') as f:
                hexagons = json.load(f)
                self.hexagons = [tuple(hexagon) for hexagon in hexagons]
        except FileNotFoundError:
            print("board.json file was not found.")

        for hexagon in self.hexagons:
            self.board[hexagon] = {'coinId': None, 'number': 0, 'base': None}
        for hexagon in self.bases:
            self.board[hexagon]['base'] = -1


    def inc_base_count(self, playerId, amount=1):
        self.base_count[playerId] = self.base_count[playerId] + amount

    def dec_base_count(self, playerId):
        self.base_count[playerId] = self.base_count[playerId] - 1

    def get_base_count(self, playerId):
        return self.base_count[playerId]

    def add_base(self, base, playerId):

        self.bases[base] = playerId
        if (self.board[base]['base'] != -1) and (self.board[base]['base'] != playerId):
            self.dec_base_count(not playerId)
        self.board[base]['base'] = playerId

    def available_hexagon(self, hexagon):
        if self.board[hexagon]['coinId']:
            return 0
        else:
            return hexagon

    def available_friendly_bases(self, playerId):
        '''
        Return list of available bases regarding a given player
        '''
        res = [base for base, basePlayerId in self.bases.items()
                if (basePlayerId == playerId)
                and (self.board[base]['coinId'] is None)]
        # print(res)
        return res




    def check_unit_deployed(self, coinId):
        '''
        Return 1 if unit is already deployed on the board
        '''

        for unit in self.units_deployed.keys():
            if unit == coinId:
                return 1
        return 0

    def neighbors_1(self, hexagon):
        x, y, z = hexagon
        neighbors = set()
        for i in [-1, 1]:
            neighbors.update({(x, y-i, z+i), (x+i, y+i, z), (x+i, y, z+i)})
        return {hexag for hexag in neighbors if hexag in self.hexagons}

    def neighbors_2(self, hexagon):
        x, y ,z = hexagon
        neighbors = set()
        for a, b, c in self.neighbors_1((x, y, z)):
            neighbors.update(self.neighbors_1((a, b, c)))
        neighbors.discard((x, y, z))
        return {hexag for hexag in neighbors if hexag in self.hexagons}
