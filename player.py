import pygame as pg
from settings import *
import math


class Player:
    def __init__(self, game):
        self.game = game        #create instance of game class
        self.x, self.y = player_pos
        self.angle = player_angle   #x/y coordinates of player and angle of direction taken from settings

    def movement(self): #this whole function is math for player move speed and camera turn speed
        sin_a = math.sin(self.angle)    #uses sin and cos from math to determine angles related to movement
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = player_speed * self.game.delta_time     #speed takes into account the delta time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:    #configures WASD for moving forwards, backwards, left, and right
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += - speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)    #apply received increments to corresponding coordinates of the player (as long as no wall is in the way)

        if keys[pg.K_LEFT]:     #uses left and right keys for control of the player's direction
            self.angle -= player_rot_speed * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += player_rot_speed * self.game.delta_time
        self.angle %= math.tau

    def check_wall(self, x, y):     #check if coordinates hit a wall
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy): #using computed dx and dy coordinates and check_wall function, only allow movement if there is no wall
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):     #draws player on a plane
        #pg.draw.line(self.game.screen, "yellow", (self.x * 100, self.y * 100),  #draws direction of movement/where player is looking as a yellow line
         #            (self.x * 100 + width * math.cos(self.angle),
           #           self.y * 100 + width * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)     #player drawn as a green circle

    def update(self):   #updates with the latest movement
        self.movement()

    @property   #this property returns the player coordinates
    def pos(self):
        return self.x, self.y

    @property   #returns int coordinates so that we know which tile of the map we are on
    def map_pos(self):
        return int(self.x), int(self.y)
