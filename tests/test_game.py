#!/usr/bin/env python3

import pytest
from warchest.game import Game
from warchest.player import Player
import numpy as np
import logging as log


class TestWarchest(object):
    @pytest.fixture(scope="function")
    def p1(self):
        return Player(name="White")

    @pytest.fixture(scope="function")
    def p2(self):
        return Player(name="Black")

    @pytest.fixture(scope="function")
    def game(self, p1, p2):
        draft = [0, 1, 2, 3, 4, 5, 6, 7]
        return Game(p1, p2, draft=draft)

    def test_player_draft(self, p1, p2):
        # Test a manual draft (different than human manual draft)
        draft = [0, 1, 2, 3, 4, 5, 6, 7]
        game = Game(p1, p2, draft=draft)
        assert p1.unit_draft == [0, 1, 2, 3] and p2.unit_draft == [4, 5, 6, 7]

    def test_board(self, game):
        # Test the length of board
        assert len(game.board) == 37

    def test_3turn_pass(self, game):
        """
        Assert that player_turn after 3 actions for each player without taking
        the initiative is still the same
        """
        first_player = game.player_turn

        count = 0
        while count < 6:
            game.p[game.player_turn].get_open_moves()
            pass_move = (
                game.p[game.player_turn].pass_move,
                game.p[game.player_turn].hand[0],
            )
            game.p[game.player_turn].make_move(pass_move)  # random move
            game.proceed_game()
            count += 1

        assert first_player == game.player_turn

    def test_3turn_change_init(self, game):
        """
        Assert that player_turn after 3 actions for each player,
        with player 2 taking the initiative, has changed
        """
        first_player = game.player_turn
        game.p[game.player_turn].get_open_moves()
        game.p[game.player_turn].make_move()  # random move
        game.proceed_game()

        game.p[game.player_turn].get_open_moves()
        init_move = (
            game.p[game.player_turn].take_initiative,
            game.p[game.player_turn].hand[0],
        )
        game.p[game.player_turn].make_move(init_move)  # random move
        game.proceed_game()

        count = 0
        while count < 4:
            game.p[game.player_turn].get_open_moves()
            game.p[game.player_turn].make_move()  # random move
            game.proceed_game()
            count += 1

        assert first_player != game.player_turn
