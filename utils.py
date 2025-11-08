import pygame

# some global constants
WIDTH = 1050
HEIGHT = 650
# colors.
# if you find it more suitable, change this dictionary to standalone constants like: RED = (255, 0, 0)
COLORS = {
    'RED': (255, 0, 0),           # closed nodes
    'GREEN': (0, 255, 0),         # open nodes
    'BLUE': (0, 0, 255),          # start node
    'YELLOW': (255, 255, 0),      # end node
    'WHITE': (255, 255, 255),     # unvisited nodes
    'BLACK': (0, 0, 0),           # barrier
    'PURPLE': (128, 0, 128),      # path
    'ORANGE': (255, 165 ,0),      # nodes being considered
    'GREY': (128, 128, 128),      # grid lines
    'TURQUOISE': (64, 224, 208),   # neighbor nodes
    'DARK PINK': (255, 20, 147),  
    'PINK': (255, 192, 203)        # background color      
}
