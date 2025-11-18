import math
#pygame constants. This is gross, but a tutorial is a tutorial

TILE_SIZE = 64

ROWS,COLS = 10,15

FPS = 60

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE
FOV = 60 * (math.pi / 180) #in radians
RES = 6 # width of rects
NUM_RAYS = WINDOW_WIDTH // RES

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,127)
RED = (227,20,10)
GREEN = (0,248,10)
PURPLE = (255,0,255)
DARK_GREY = (40,40,40)
LIGHT_GREY = (200,200,200)
LIGHT_BLUE = (128,128,255)
LIGHT_GREEN = (128,255,128)
DARK_BLUE = (40,40,255)

TILE_KEY = {
    'W1': {'type': 'wall', 'color': GREY, 'action': None},         # Wall type 1
    'W2': {'type': 'wall', 'color': DARK_GREY, 'action': None},    # Wall type 2
    'W3': {'type': 'wall', 'color': PURPLE, 'action': None},  # Wall type 33 (example of another wall)
    'F1': {'type': 'floor', 'color': WHITE, 'action': None},       # Floor type 1 (standard floor)
    'F2': {'type': 'floor', 'color': LIGHT_BLUE, 'action': None},  # Floor type 2 void tile
    'F3': {'type': 'floor', 'color': LIGHT_GREEN, 'action': 'next_map'}, # Floor type 3 (another variant)
    # You can continue to expand this dictionary for additional types
}