import pygame as pg
import sys
from settings import *


class Game:
    def __init__(self):
        pg.init()   #initializes pygame modules
        self.screen = pg.display.set_mode(res)  #creates a screen for rendering the set resolution
        self.clock = pg.time.Clock()    #instance of the clock class for frame-rate

    def new_game(self):
        pass

    def update(self):       #function for updating the screen
        pg.display.flip()       #flip updates the screen
        self.clock.tick(fps)    #tick is a measure of time. so this says for every second, 60 frames should pass
        pg.display.set_caption(f"{self.clock.get_fps() :.1f}")  #display fps in the window caption with 1 decimal place (the .1f does this)

    def draw(self):
        self.screen.fill("black")   #at each iteration, paint the screen black

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
