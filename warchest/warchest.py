#!/usr/bin/env python3

import logging as log

from classes import Game, Player

def main():
    log.basicConfig(level=log.INFO,
                    filename='warchest.log',
                    filemode='w')

    p1 = Player('White')
    p2 = Player('Black')
    game = Game(p1, p2, draft=[0, 1, 2, 3, 4, 5, 6, 7])
    # print(f'bag: \n{p1.bag}')
    # print(f'supply: \n{p1.supply}')


    # debug tools
    import pandas as pd
    df = pd.DataFrame
    game.proceed_game()

    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
