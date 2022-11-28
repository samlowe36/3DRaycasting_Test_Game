#creating the game map
import pygame as pg

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, 1, 1, 1, _, _, _, 1, 1, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],
    [1, _, _, _, _, _, 1, _, _, _, _, _, 1, _, _, 1],   #this will be the map
    [1, _, _, 1, 1, 1, 1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 1, _, _, _, 1, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:  #Map class with instance of Game class as input to the constructor.
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}     #mini_map and world_map are now attributes
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):     #iterate over array
            for i, value in enumerate(row):     #write only the coordinates with numeric values to the dictionary
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, "darkgray", (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]     #draws rectangles for each position in the world map
        #rectangles draw to the game screen, are dark grey, begin at the very first positions, are 100x100 and have a width/thickness of 2