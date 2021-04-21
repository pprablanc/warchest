'''
Board class
'''
import logging as log
import json

class Board(object):

    def __init__(self):
        self.board = {}
        self.hexagons = []
        self.bases = []
        self._load_board()


    def _load_board(self):
        filename_board = 'resources/board.json'
        filename_bases = 'resources/bases.json'
        try:
            with open(filename_board, 'r') as f:
                hexagons = json.load(f)
                self.hexagons = [tuple(hexagon) for hexagon in hexagons]
        except FileNotFoundError:
            print("board.json file was not found.")
        try:
            with open(filename_bases, 'r') as f:
                bases = json.load(f)
                self.bases= [tuple(base) for base in bases]
        except FileNotFoundError:
            print("bases.json file was not found.")

        for hexagon in self.hexagons:
            self.board[hexagon] = {'unitId': None, 'number': 0, 'base': None}
        for hexagon in self.bases:
            self.board[hexagon]['base'] = -1

    def available_bases(self):
        raise NotImplementedError

    def available_friendly_bases(self, player):
        '''
        Return list of available bases regarding a given player
        '''
        return [base for base in self.bases
                if (self.board[base]['base'] == player) and (self.board[base]['unitId'] is None)]


    def check_unit_deployed(self, unitId):
        '''
        Return 1 if unit is already deployed on the board
        '''
        for hexagon in self.hexagons:
            if self.board[hexagon]['unitId'] == unitId:
                return 1
            else:
                return 0
