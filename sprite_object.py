import pygame as pg
import math
from settings import *


class SpriteObject:
    #input of constructor is path to sprite file, its location on the map, and the game
    def __init__(self, game, path="resources/sprites/static_sprites/candelabra.png", pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game    #take instance of game
        self.player = game.player   #take instance of player
        self.x, self.y = pos    #take coordinates of sprite
        self.image = pg.image.load(path).convert_alpha()    #load the image of the sprite
        self.image_width = self.image.get_width()   #create attribute for width of sprite
        self.image_half_width = self.image.get_width() // 2 #create attribute for half width of sprite
        self.image_ratio = self.image_width / self.image.get_height()   #attribute for getting initial sprite aspect ratio
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1   #defining more attributes we introduced
        self.sprite_half_width = 0
        self.sprite_scale = scale   #assigning the scale parameter above to an attribute
        self.sprite_height_shift = shift    #assigning the shift parameter above to an attribute

    def get_sprite_projection(self):
        proj = screen_dist / self.norm_dist * self.sprite_scale #get projection of sprite
        proj_width, proj_height = proj * self.image_ratio, proj #adjust correct projection size

        image = pg.transform.scale(self.image, (proj_width, proj_height))   #scale the image to the calculated projection size

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.sprite_height_shift
        pos = self.screen_x - self.sprite_half_width, half_height - proj_height // 2 + height_shift   #find position of sprite

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos)) #add sprite to array with walls

    def get_sprite(self):
        #math to calculate theta angle (angle player is looking at sprite from)
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        #find delta angle to determine how many rays the sprite has shifted
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        #calculate how many rays in the delta angle
        delta_rays = delta / delta_angle
        self.screen_x = (half_num_rays + delta_rays) * scale

        #calculate distance to sprite
        self.dist = math.hypot(dx, dy)
        #remove fishbowl effect on sprite
        self.norm_dist = self.dist * math.cos(delta)
        #maintain performance so sprite size doesnt balloon up and tank frame-rate if we get too close
        if -self.image_half_width < self.screen_x < (width + self.image_half_width) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
        