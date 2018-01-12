#!/usr/bin/python3

import time
from game import Game
from settings import Settings
from rules import Rules
from thomas_rules import ThomasRules

def bench(name, f):
    before = time.perf_counter()
    f()
    after = time.perf_counter()
    elapsed = int((after - before) * 1000)
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

    # mock an update to setup state
    game = Game()
    game._handle_update("update game round 0")
    game._handle_update("update game field .,.,.,1,.,0,.,.,.,.,.,0,.,1,.,.,1,.,.,.,.,.,.,.,0,.,.,1,1,.,.,.,1,1,.,.,0,.,.,.,0,.,.,0,1,0,1,.,.,.,1,.,.,.,1,.,.,.,.,1,.,0,.,.,1,.,0,.,1,.,1,1,.,1,.,1,.,.,0,1,.,0,.,0,.,0,.,.,.,1,1,.,.,.,.,0,.,.,1,.,.,.,.,.,0,.,0,1,0,.,.,.,.,.,.,1,.,1,0,.,1,0,.,.,.,.,.,0,.,.,.,.,.,.,1,.,.,.,.,.,1,.,0,1,0,1,.,0,.,.,.,.,.,0,.,.,.,.,.,.,1,.,.,.,.,.,1,0,.,1,0,.,0,.,.,.,.,.,.,1,0,1,.,1,.,.,.,.,.,0,.,.,1,.,.,.,.,0,0,.,.,.,1,.,1,.,1,.,0,1,.,.,0,.,0,.,0,0,.,0,.,1,.,0,.,.,1,.,0,.,.,.,.,0,.,.,.,0,.,.,.,0,1,0,1,.,.,1,.,.,.,1,.,.,0,0,.,.,.,0,0,.,.,1,.,.,.,.,.,.,.,0,.,.,0,.,1,.,.,.,.,.,1,.,0,.,.,.")
    game._handle_update("update player0 living_cells 50")
    game._handle_update("update player1 living_cells 50")    
    
    # repeatedly calculate immutable states from the original one
    first_state = game.current_node.state

    def calc100():
        for i in range(1, 100):
            Rules.calculate_next_state(first_state)
    bench('calc100', calc100)

    def calc1000():
        for i in range(1, 1000):
            Rules.calculate_next_state(first_state)
    bench('calc1000', calc1000)

    def thomas100():
        for i in range(1, 100):
            ThomasRules.calculate_next_state(first_state)
    bench('thomas100', thomas100)

    def thomas1000():
        for i in range(1, 1000):
            ThomasRules.calculate_next_state(first_state)
    bench('thomas1000', thomas1000)