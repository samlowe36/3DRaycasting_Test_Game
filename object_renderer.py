import pygame as pg
from settings import *


class ObjectRenderer:   #this class renders all objects in the game
    def __init__(self, game):
        self.game = game    #take game instance as attribute
        self.screen = game.screen   #take rendering screen as attribute
        self.wall_textures = self.load_wall_textures()  #access textures for walls through wall_textures attribute by calling our texture loading function
        self.sky_image = self.get_texture("resources/textures/sky.png", (width, half_height))
        self.sky_offset = 0 #image of sky depends on mouse movement, so initial offset will be zero
        self.blood_screen = self.get_texture("resources/textures/blood_screen.png", res)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f"resources/textures/digits/{i}.png", [self.digit_size] * 2)
                            for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture("resources/textures/game_over.png", res)
        self.win_image = self.get_texture('resources/textures/win.png', res)

    def draw(self):
        self.draw_background()
        self.render_game_objects()  #call the function
        self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits["10"], ((i + 1) * self.digit_size, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % width    #calc offset depending on relative mouse movement from player
        self.screen.blit(self.sky_image, (-self.sky_offset, 0)) #sky texture 1 based off calculated sky_offset value
        self.screen.blit(self.sky_image, (-self.sky_offset + width, 0)) #sky texture 2 based off calculated sky_offset value
        #floor
        pg.draw.rect(self.screen, floor_color, (0, half_height, width, height)) #make floor based off color in settings

    def render_game_objects(self):
        #this is sorted as a tuple so that things are loaded in the correct order and sprites dont appear through walls
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:  #iterate over list of objects for rendering
            self.screen.blit(image, pos)    #draw resulting texture columns on the screen
            #blit stands for block transfer and it copies the contents of one surface onto another surface

    @staticmethod
    def get_texture(path, res=(texture_size, texture_size)):    #static method where path to texture and resolution are specified
        texture = pg.image.load(path).convert_alpha()   #loads texture from specified path
        return pg.transform.scale(texture, res)     #returns a scaled image

    def load_wall_textures(self):
        return {
            1: self.get_texture("resources/textures/1.png"),
            2: self.get_texture("resources/textures/2.png"),
            3: self.get_texture("resources/textures/3.png"),
            4: self.get_texture("resources/textures/4.png"),
            5: self.get_texture("resources/textures/5.png"),
        }