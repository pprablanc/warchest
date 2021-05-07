'''
Game class
'''
import json
import numpy as np
from warchest.player import Player
from warchest.board import Board


class Game(object):
    # Class variable
    PLAYER_1 = 0
    PLAYER_2 = 1

    def __init__(self, player_name_1, player_name_2, draft="random", first_player="random"):
        self.player_turn = None
        self.units = None
        self.available_units = None
        self.board = Board()

        # Instantiate players
        player1 = Player(player_name_1, self.board, playerId=Game.PLAYER_1)
        player2 = Player(player_name_2, self.board, playerId=Game.PLAYER_2)
        self.player = [player1, player2]

        # Initialize starting bases
        self.board.add_base((-3,-1,-2), Game.PLAYER_1)
        self.board.add_base((-2,-3,1), Game.PLAYER_1)
        self.board.inc_base_count(Game.PLAYER_1, 2)
        self.board.add_base((3,1,2), Game.PLAYER_2)
        self.board.add_base((2,3,-1), Game.PLAYER_2)
        self.board.inc_base_count(Game.PLAYER_2, 2)

        self._load_units()
        self._make_draft(draft=draft)
        self._set_initiative(first_player=first_player)
        self.player[Game.PLAYER_1].draw_bag_end_turn()
        self.player[Game.PLAYER_2].draw_bag_end_turn()

    def reset(self, draft="random", first_player="random"):
        self.__init__(draft, first_player)

    def get_state_vector(self, playerId):
        # TODO: Need optimisation
        # Update state after each action instead of updating the whole
        # state_vector

        state_vector = []
        # board vector: encode position + unitId + #units
        for elt in self.board.board.values():
            vec = 16*[0]
            if elt['coinId'] is not None:
                vec[elt['coinId']] = elt['coinId']
            state_vector = state_vector + vec

        # bases vector
        # discards vector
        # supplies vector
        # player_1 bag vector
        # player_1 hand vector
        # player_2 hand+bag vector

        # for developpement
        # print(self.state_vector)
        return state_vector

    def get_action_vector(self, playerId):

        self.player[playerId].get_action_vector()
        return self.player[playerId].action_vector

    def get_state_action_vector(self, playerId):
        state_action_vector = self.get_state_vector(playerId) + self.get_action_vector(playerId)
        return state_action_vector


    def proceed_game(self):
        """
        Start or remain game after selecting actions for a player
        """
        if self.player[self.player_turn].hand == []:
            self.player[self.player_turn].draw_bag_end_turn()
            change_init = (
                not self.player[self.player_turn].init_available
                and not self.player[not self.player_turn].init_available
            )
            if change_init and len(self.player[not self.player_turn].hand) == 3:
                self.player[not self.player_turn].init_available = 1
                self.player_turn = not self.player_turn

        self.player_turn = not self.player_turn

    def who_win(self, playerId):
        if self.board.get_base_count(playerId) > 5:
            return playerId
        else:
            return -1

    def _load_units(self):
        """
        Load units file and initialize available units
        """
        filename = "resources/units.json"
        try:
            with open(filename, "r") as f:
                self.units = json.load(f)
                self.available_units = np.arange(len(self.units))
        except FileNotFoundError:
            print("units.json file was not found.")

    def _make_draft(self, draft="random"):
        """
        Make draft
        """

        if draft == "random":
            self.player[Game.PLAYER_1].initialize_player(
                self._draw_units_draft(), self.units
            )
            self.player[Game.PLAYER_2].initialize_player(
                self._draw_units_draft(), self.units
            )
        elif draft == "manual":
            assert draft == "random", "Manual draft not yet implemented"
        elif isinstance(draft, list):
            try:
                draft_p1 = draft[:4]
                draft_p2 = draft[4:]
            except IndexError as e:
                print(f"draft variable should be list of 8 integers: {e}")

            self.player[Game.PLAYER_1].initialize_player(draft_p1, self.units)
            self.player[Game.PLAYER_2].initialize_player(draft_p2, self.units)

    def _draw_units_draft(self, n_units=4):
        units_draft = np.random.choice(self.available_units, n_units, replace=False)
        for i in units_draft:
            self.available_units = np.delete(
                self.available_units, np.where(self.available_units == i)
            )
        return units_draft

    def _set_initiative(self, first_player="random"):
        """
        Set initiative and prepare game to start.
        """

        if first_player == "random":
            self.player_turn = np.random.choice([Game.PLAYER_1, Game.PLAYER_2])
        elif isinstance(first_player, int):
            if first_player not in [Game.PLAYER_1, Game.PLAYER_2]:
                raise Exception(
                    f"first_player value not in [{Game.PLAYER_1}, {Game.PLAYER_2}]"
                )
            else:
                self.player_turn = first_player

        self.player[self.player_turn].init_available = 0
        self.player[not self.player_turn].init_available = 1

    def render(self, player):
        """
        Game rendering
        """
        info_p = f"""Player {player.name}:
        supply: {player.supply}
        bag: {player.bag}
        hand: {player.hand}
        discard: {player.discard.discard}
        board: {self.board.board}
        """
        print(info_p)


