#!/usr/bin/python3


from game import Game
from settings import Settings
import time

def bench(name, f):
    before = time.perf_counter()
    f()
    after = time.perf_counter()
    elapsed = (after - before) * 1000
    print(f'{name}: {elapsed}ms')

if __name__ == '__main__':
    # mock settings
    settings = {}
    Settings._add_setting(settings, 'settings timebank 10000')
    Settings._add_setting(settings, 'settings time_per_move 100')
    Settings._add_setting(settings, 'settings player_names player0,player1')
    Settings._add_setting(settings, 'settings your_bot player0')
    Settings._add_setting(settings, 'settings your_botid 0')
    Settings._add_setting(settings, 'settings field_width 18')
    Settings._add_setting(settings, 'settings field_height 16')
    Settings._add_setting(settings, 'settings max_rounds 100')
    Settings._load_settings(settings)

    # create engine
    game = Game()

    # mock an update to setup state
    game._handle_update("update game round 0")
    game._handle_update("update game field .,.,.,1,.,0,.,.,.,.,.,0,.,1,.,.,1,.,.,.,.,.,.,.,0,.,.,1,1,.,.,.,1,1,.,.,0,.,.,.,0,.,.,0,1,0,1,.,.,.,1,.,.,.,1,.,.,.,.,1,.,0,.,.,1,.,0,.,1,.,1,1,.,1,.,1,.,.,0,1,.,0,.,0,.,0,.,.,.,1,1,.,.,.,.,0,.,.,1,.,.,.,.,.,0,.,0,1,0,.,.,.,.,.,.,1,.,1,0,.,1,0,.,.,.,.,.,0,.,.,.,.,.,.,1,.,.,.,.,.,1,.,0,1,0,1,.,0,.,.,.,.,.,0,.,.,.,.,.,.,1,.,.,.,.,.,1,0,.,1,0,.,0,.,.,.,.,.,.,1,0,1,.,1,.,.,.,.,.,0,.,.,1,.,.,.,.,0,0,.,.,.,1,.,1,.,1,.,0,1,.,.,0,.,0,.,0,0,.,0,.,1,.,0,.,.,1,.,0,.,.,.,.,0,.,.,.,0,.,.,.,0,1,0,1,.,.,1,.,.,.,1,.,.,0,0,.,.,.,0,0,.,.,1,.,.,.,.,.,.,.,0,.,.,0,.,1,.,.,.,.,.,1,.,0,.,.,.")
    game._handle_update("update player0 living_cells 50")
    game._handle_update("update player1 living_cells 50")

    # run one move
    bench('build_children', game.current_node.build_children)
    bench('move', game.move)

