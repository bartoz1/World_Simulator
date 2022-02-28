from worldsimulator.engine import Engine
from worldsimulator.utilities import Options
from worldsimulator.world import World

engine = Engine()

mars = World(2, 3)
# engine.start_new_game()
#input("hh?")
opt = 1
while opt != Options.EXIT:
    opt = engine.main_menu()
    if opt == Options.NEW_GAME:     # creating new world
        engine.start_new_game()
        engine.run_game_loop()
    if opt == Options.LOAD_GAME:    # loading game from file
        engine.load_from_file()
        engine.run_game_loop()
    if opt == Options.OPTIONS:
        engine.options_menu()
