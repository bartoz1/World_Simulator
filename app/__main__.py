from app.engine import Engine
from app.utilities import Options
from app.world import World

engine = Engine()

mars = World(2, 3)
# engine.start_new_game()
#input("hh?")
opt = 1
while opt != Options.EXIT:
    opt = engine.main_menu()
    if opt == Options.NEW_GAME:     # creating new world
        engine.start_new_game()
        input("hh?")
    if opt == Options.LOAD_GAME:    # loading game from file
        pass
