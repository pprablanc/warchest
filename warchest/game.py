import logging as log
import json
import numpy as np

class Game(object):

    def __init__(self, player1, player2, draft='random', first_player='random'):


        # instantiate players
        self.p = [player1, player2]

        self._board_initialization()
        self._load_game_data()

        self._make_draft(draft=draft)

        # Set initiative
        self._set_initiative(first_player=first_player)


    def _board_initialization(self):
        '''
        Initialize the game board
        '''
        self.board = [(x-3, y-3, x-y) for x in range(7) for y in range(7) if abs(x-y) <=3]
        self.PLAYER_1 = 0
        self.PLAYER_2 = 1

    def _load_game_data(self):
        '''
        Initialize game data: possibles units and initialize player bases
        '''
        self._load_units()
        self._load_bases()

    def proceed_game(self):
        '''
        Start or remain game after selecting actions for a player
        '''
        if self.action_todo:
            self.action_todo = 0
            return
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

        self.player_turn = not self.player_turn
        return

    def _load_units(self):
        '''
        Load units file and initialize available units
        '''
        filename = 'resources/units.json'
        try:
            with open(filename, 'r') as f:
                self.units = json.load(f)
                self.available_units = np.arange(len(self.units))
        except:
            print("units.json file was not found.")


    def _load_bases(self):
        '''
        Load bases json file and initialize player bases
        '''
        filename = 'resources/bases.json'
        try:
            with open(filename, 'r') as f:
                self.bases_map = json.load(f)
                self.p[self.PLAYER_1].add_base(self.bases_map[:2])
                self.p[self.PLAYER_2].add_base(self.bases_map[-2:])
        except:
            print("bases.json file was not found.")

    def _make_draft(self, draft='random'):
        '''
        Make draft
        '''

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

    def _draw_units_draft(self, n_units=4):
        units_draft = np.random.choice(self.available_units, n_units, replace=False)
        for i in units_draft:
            self.available_units = np.delete(self.available_units,
                                             np.where(self.available_units == i)
                                             )
        return units_draft

    def _set_initiative(self, first_player='random'):
        '''
        Set initiative and prepare game to start.
        '''

        if first_player=='random':
            self.player_turn = np.random.choice([self.PLAYER_1, self.PLAYER_2])
        elif type(first_player) == int:
            if first_player not in [self.PLAYER_1, self.PLAYER_2]:
                raise Exception(f"first_player value not in [{self.PLAYER_1}, {self.PLAYER_2}]")
            else:
                self.player_turn = first_player

        self.p[self.player_turn].init_available = 0
        self.p[not self.player_turn].init_available = 1
        self.p[self.PLAYER_1].draw_bag_end_turn()
        self.p[self.PLAYER_2].draw_bag_end_turn()
        self.action_todo = 1


    def render(self, p):
        info_p = f'''Player {p.name}:
        supply: {p.supply}
        bag: {p.bag}
        hand: {p.hand}
        discard: {p.discard}
        bases: {p.bases}
        '''
        print(info_p)

