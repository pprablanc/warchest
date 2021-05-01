'''
Tests
'''
import pytest
# from warchest.game import Game

from warchest.game import Game
import numpy as np
import logging as log


class TestWarchest(object):
    @pytest.fixture(scope="function")
    def p1(self):
        return "White"

    @pytest.fixture(scope="function")
    def p2(self):
        return "Black"

    @pytest.fixture(scope="function")
    def game(self, p1, p2):
        draft = [0, 1, 2, 3, 4, 5, 6, 7]
        return Game(p1, p2, draft=draft)

    def test_player_draft(self, p1, p2):
        # Test a manual draft (different than human manual draft)
        draft = [0, 1, 2, 3, 4, 5, 6, 7]
        game = Game(p1, p2, draft=draft)
        assert game.player[Game.PLAYER_1].unit_draft == [0, 1, 2, 3] and game.player[Game.PLAYER_2].unit_draft == [4, 5, 6, 7]

    def test_board(self, game):
        # Test the length of board
        assert len(game.board.board) == 37

    def test_3turn_pass(self, game):
        """
        Assert that player_turn after 3 actions for each player without taking
        the initiative is still the same
        """
        first_player = game.player_turn

        count = 0
        while count < 6:
            game.player[game.player_turn].get_open_moves()
            pass_move = (
                game.player[game.player_turn].pass_move,
                game.player[game.player_turn].hand[0],
            )
            game.player[game.player_turn].make_move(pass_move)
            game.proceed_game()
            count += 1

        assert first_player == game.player_turn

    def test_3turn_change_init(self, game):
        """
        Assert that player_turn after 3 actions for each player,
        with player 2 taking the initiative, has changed
        """
        first_player = game.player_turn
        game.player[game.player_turn].get_open_moves()
        game.player[game.player_turn].make_move()
        game.proceed_game()

        game.player[game.player_turn].get_open_moves()
        init_move = (
            game.player[game.player_turn].take_initiative,
            game.player[game.player_turn].hand[0],
        )
        game.player[game.player_turn].make_move(init_move)
        game.proceed_game()

        count = 0
        while count < 4:
            game.player[game.player_turn].get_open_moves()
            game.player[game.player_turn].make_move()
            game.proceed_game()
            count += 1

        assert first_player != game.player_turn


    def recruit(self, game):
        """
        Assert that recruit move was handled properly:
            - transfer coin from hand to discard
            - add unit coin to discard
        """
        raise NotImplementedError

    def deploy(self, game):
        '''
        Assert that unit is deployed
        '''
        raise NotImplementedError

    def deploy_only_one(self, game):
        '''
        Assert that only one type of unit is deployed
        on the board.
        '''
        raise NotImplementedError
