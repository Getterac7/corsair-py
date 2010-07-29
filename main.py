from os.path import join
import sys

sys.path = [join(sys.path[0],"data")] + sys.path

import game

game.main()
