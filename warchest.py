'''
main module
'''
import logging as log
import time

from warchest.game import Game

def main():
    log.basicConfig(level=log.INFO,
                    filename='warchest.log',
                    filemode='w')

    tic = time.perf_counter()
    game = Game('P1', 'P2', draft=[0, 1, 2, 3, 4, 5, 6, 7])


    count = 0
    game_count = 0
    while count < 100000:
        # game.render(game.player[game.player_turn])
        game.player[game.player_turn].get_open_moves()
        game.player[game.player_turn].make_move() #random move
        winner = game.who_win(game.player_turn)
        if winner in [game.PLAYER_1, game.PLAYER_2]:
            log.info('Player {game.player_turn} win the game.')
            game.reset()
            game_count += 1
        game.proceed_game()
        count += 1
    toc = time.perf_counter()
    print('elapsed time: '+ str(toc - tic))
    print('total count: '+str(count))
    print('number of games:'+ str(game_count))
    print('average game count: '+str(count/game_count))

if __name__ == '__main__':
    main()
