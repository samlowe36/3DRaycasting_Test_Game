import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game    #take an instance of our game

    def ray_cast(self): #entire function is using complicated trigonometry in order to determine angles, depth, and the ray casting on the map grid
        ox, oy = self.game.player.pos   #dont fully understand the math but in theory it should work for any game based on a grid that uses raycasting
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - half_fov + 0.0001
        for ray in range(num_rays):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            #horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(max_depth):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            #verticals
            x_vert, dx = (x_map +1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(max_depth):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            #depth
            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            #remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            #draw for 2d debug
            #pg.draw.line(self.game.screen, "yellow", (100 * ox, 100 * oy),
             #            (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            #pseudo 3d projection
            proj_height = screen_dist / (depth + 0.0001)

            #draw walls
            color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            pg.draw.rect(self.game.screen, color,
                         (ray * scale, half_height - proj_height // 2, scale, proj_height))

            ray_angle += delta_angle

    def update(self):
        self.ray_cast()

