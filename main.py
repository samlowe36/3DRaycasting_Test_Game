import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *

class Game:
    def __init__(self):
        pg.init()   #initializes pygame modules
        pg.mouse.set_visible(False) #make mouse cursor invisible
        self.screen = pg.display.set_mode(res)  #creates a screen for rendering the set resolution
        self.clock = pg.time.Clock()    #instance of the clock class for frame-rate
        self.delta_time = 1     #delta time is so that movement speed can be independent of frame-rate
        self.new_game()

    def new_game(self):
        self.map = Map(self)    #instance of Map class
        self.player = Player(self)      #instance of player class
        self.object_renderer = ObjectRenderer(self) #instance of object renderer class
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self)

    def update(self):       #function for updating the screen
        self.player.update()
        self.raycasting.update()
        self.static_sprite.update()
        pg.display.flip()       #flip updates the screen
        self.delta_time = self.clock.tick(fps)    #tick is a measure of time. so this says for every second, 60 frames should pass
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")  #display fps in the window caption with 1 decimal place (the .1f does this)

    def draw(self):
        #self.screen.fill("black")   #at each iteration, paint the screen black (not needed now that we have background and wall textures
        self.object_renderer.draw()
        #self.map.draw()     #draw the map (this was for 2d testing and isnt needed now that it is 3d)
        #self.player.draw()      #draw the player (this was for 2d testing and isnt needed now that it is 3d)

    def check_events(self): #function checks for the events of closing the working window or pressing the escape key, and exits app if this happens
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def run(self):  #main loop of the game runs from here
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":  #create an instance of the game and call the run method
    game = Game()
    game.run()
