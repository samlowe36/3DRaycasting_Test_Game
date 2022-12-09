import pygame as pg


class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init() #initialize sound mixer
        self.path = "resources/sound/"  #location of sound files
        self.shotgun = pg.mixer.Sound(self.path + "shotgun.wav")    #assign the shotgun sound to the shotgun
        self.npc_pain = pg.mixer.Sound(self.path + "npc_pain.wav")
        self.npc_death = pg.mixer.Sound(self.path + "npc_death.wav")
        self.npc_shot = pg.mixer.Sound(self.path + "npc_attack.wav")
        self.npc_shot.set_volume(0.2)
        self.player_pain = pg.mixer.Sound(self.path + "player_pain.wav")
        self.theme = pg.mixer.music.load(self.path + "theme.mp3")
        pg.mixer.music.set_volume(0.4)
