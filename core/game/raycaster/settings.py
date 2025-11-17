import math
#pygame constants. This is gross, but a tutorial is a tutorial

TILE_SIZE = 64

ROWS,COLS = 10,15

FPS = 60

WINDOW_WIDTH = COLS * TILE_SIZE
WINDOW_HEIGHT = ROWS * TILE_SIZE
FOV = 60 * (math.pi / 180) #in radians
RES = 4 # width of rects
NUM_RAYS = WINDOW_WIDTH // RES

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (128,128,127)
RED = (227,20,10)
GREEN = (0,248,10)
PURPLE = (255,0,255)