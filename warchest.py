'''
main module
'''
import logging as log

from warchest.game import Game

def main():
    log.basicConfig(level=log.INFO,
                    filename='warchest.log',
                    filemode='w')

    game = Game('P1', 'P2', draft=[0, 1, 2, 3, 4, 5, 6, 7])
    # print(f'bag: \n{p[PLAYER_1]bag}')
    # print(f'supply: \n{p[PLAYER_1]supply}')



    count = 0
    while count < 40:
        game.render(game.player[game.player_turn])
        game.player[game.player_turn].get_open_moves()
        game.player[game.player_turn].make_move() #random move
        if len(game.player[game.player_turn].bases) > 5:
            log.info('Player {game.player_turn} win the game.')
            break
        game.proceed_game()

        count += 1
    import pdb; pdb.set_trace()

if __name__ == '__main__':
    main()
