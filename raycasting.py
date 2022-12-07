import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):   #take an instance of our game
        self.game = game    #game as an attribute
        self.ray_casting_result = []    #defines attributes for result of ray casting
        self.objects_to_render = []     #defines attributes for objects to be drawn
        self.textures = self.game.object_renderer.wall_textures #define a short name for the wall textures

    def get_objects_to_render(self):    #function for getting objects to draw
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values        #get the parameters calculated as a result of ray casting...

            if proj_height < height:    #normal scaling case
                wall_column = self.textures[texture].subsurface(    #and based on them, for each ray, select a sub surface...
                    offset * (texture_size - scale), 0, scale, texture_size #in the form of a rectangle from the initial texture
                )
                wall_column = pg.transform.scale(wall_column, (scale, proj_height)) #scale subsurface to projection height
                wall_pos = (ray * scale, half_height - proj_height // 2)
            else:   #if/else block is for the case when you get close to the wall, so that the texture height doesnt balloon up and tank performance
                texture_height = texture_size * height / proj_height    #calc height for texture column
                wall_column = self.textures[texture].subsurface(    #when scaling texture, height shouldnt exceed screen height
                    offset * (texture_size - scale), half_texture_size - texture_height // 2,
                    scale, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (scale, height))
                wall_pos = (ray * scale, 0) #calc the position of this column texture based on ray number...

            self.objects_to_render.append((depth, wall_column, wall_pos))   #...and add it to the list of objects for rendering

    def ray_cast(self): #entire function is using complicated trigonometry in order to determine angles, depth, and the ray casting on the map grid
        self.ray_casting_result = []    #clear list before beginning the ray casting
        texture_vert, texture_hor = 1, 1
        ox, oy = self.game.player.pos   #don't fully understand the math but in theory it should work for any game based on a grid that uses ray casting
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
                    texture_hor = self.game.map.world_map[tile_hor]  #determine the numbers of the textures of the walls to which the rays collided
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
                    texture_vert = self.game.map.world_map[tile_vert]   #determine the numbers of the textures of the walls to which the rays collided
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            #depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert   #based on calculated depths of the rays,
                y_vert %= 1                                 #we find the actual texture number
                offset = y_vert if cos_a > 0 else (1 - y_vert)  #calculate the correct texture offset
            else:
                depth, texture = depth_hor, texture_hor #based on calculated depths of the rays,
                x_hor %= 1                              #we find the actual texture number
                offset = (1 - x_hor) if sin_a > 0 else x_hor    #calculate the correct texture offset

            #remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            #draw for 2d debug
            #pg.draw.line(self.game.screen, "yellow", (100 * ox, 100 * oy),
             #            (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)

            #pseudo 3d projection
            proj_height = screen_dist / (depth + 0.0001)

            #draw walls (no longer necessary once textures were added)
            #color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            #pg.draw.rect(self.game.screen, color,
                         #(ray * scale, half_height - proj_height // 2, scale, proj_height))

            #ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))   #in list of results for each ray, add this tuple
            ray_angle += delta_angle

    def update(self):
        self.ray_cast() #call the function
        self.get_objects_to_render()    #call the function
