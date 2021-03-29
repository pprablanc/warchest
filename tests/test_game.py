#!/usr/bin/env python3

import pytest
from warchest.classes import Game, Player
import numpy as np

def test_player_draft():
    p1 = Player()
    p2 = Player()
    draft = [0, 1, 2, 3, 4, 5, 6, 7]
    game = Game(p1, p2, draft=draft)
    assert (p1.unit_draft == [0, 1, 2, 3] and p2.unit_draft == [4, 5, 6, 7])

def test_player_first_hand():
    np.random.seed(123)
    p1 = Player()
    p2 = Player()
    draft = [0, 1, 2, 3, 4, 5, 6, 7]
    game = Game(p1, p2, draft=draft)
    game.proceed_game()
    assert (p1.hand == [3, 0, 2] and p2.hand == [5, 6, 6])
