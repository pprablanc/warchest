#!/usr/bin/env python3

import logging as log

from game import Game
from player import Player
# from classes import Game, Player

def main():
    log.basicConfig(level=log.INFO,
                    filename='warchest.log',
                    filemode='w')

    p1 = Player('P1')
    p2 = Player('P2')
    game = Game(p1, p2, draft=[0, 1, 2, 3, 4, 5, 6, 7])
    # print(f'bag: \n{p[PLAYER_1]bag}')
    # print(f'supply: \n{p[PLAYER_1]supply}')



    count = 0
    while count < 40:
        game.render(game.p[game.player_turn])
        game.p[game.player_turn].get_open_moves()
        game.p[game.player_turn].make_move() #random move
        if len(game.p[game.player_turn].bases) > 5:
            log.info('Player {game.player_turn} win the game.')
            break
        game.proceed_game()

        count += 1






    # import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
