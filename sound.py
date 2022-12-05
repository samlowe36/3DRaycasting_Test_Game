import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init() #initialize sound mixer
        self.path = "resources/sound/"  #location of sound files
        self.shotgun = pg.mixer.Sound(self.path + "shotgun.wav")    #assign the shotgun sound to the shotgun
