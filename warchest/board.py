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
        self.bases = []
        self._load_bases()
        self._load_board()

    def _load_bases(self):
        filename_bases = 'resources/bases.json'
        try:
            with open(filename_bases, 'r') as f:
                bases = json.load(f)
                self.bases= [tuple(base) for base in bases]
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

    def available_hexagon(self, hexagon):
        if self.board[hexagon]['coinId']:
            return 0
        else:
            return hexagon

    def available_friendly_bases(self, player):
        '''
        Return list of available bases regarding a given player
        '''
        return [base for base in self.bases
                if (self.board[base]['base'] == player) and (self.board[base]['coinId'] is None)]

    def friendly_units_deployed(self, player):
        '''
        Return list of friendly units deployed on the board
        '''



    def check_unit_deployed(self, coinId):
        '''
        Return 1 if unit is already deployed on the board
        '''
        for u_deployed in self.units_deployed:
            if u_deployed == coinId:
                return 1
            else:
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
