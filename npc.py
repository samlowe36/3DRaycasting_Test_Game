from sprite_object import *
from random import randint, random, choice


class NPC(AnimatedSprite):
    def __init__(self, game, path="resources/sprites/npc/soldier/0.png", pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time) #run constructor of parent class
        self.attack_images = self.get_images(self.path + "/attack") #provide path for all sprite images
        self.death_images = self.get_images(self.path + "/death")
        self.idle_images = self.get_images(self.path + "/idle")
        self.pain_images = self.get_images(self.path + "/pain")
        self.walk_images = self.get_images(self.path + "/walk")

        self.attack_dist = randint(3, 6)    #provide starting attributes of NPC
        self.speed = 0.03
        self.size = 10
        self.health = 100
        self.attack_damage = 10
        self.accuracy = 0.15
        self.alive = True
        self.pain = False
        self.ray_cast_value = False #raycasting will be required so that our bullets dont go through walls
        self.frame_counter = 0
        self.player_search_trigger = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        #self.draw_ray_cast()    #for 2d mode testing

    #check_wall and #check_wall_collision copied from player file
    def check_wall(self, x, y):     #check if coordinates hit a wall
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy): #using computed dx and dy coordinates and check_wall function, only allow movement if there is no wall
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos) #npc moves toward player
        next_x, next_y = next_pos
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)    #angle for npc moving toward the player tile
            dx = math.cos(angle) * self.speed   #calc increment for x axis
            dy = math.sin(angle) * self.speed   #calc increment for y axis
            self.check_wall_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.npc_shot.play()
            if random() < self.accuracy:    #determines if the npc will hit the player or not and give damage if it does
                self.game.player.get_damage(self.attack_damage)

    def animate_death(self):
        if not self.alive:  #if not alive
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:  #play death animation only once
                self.death_images.rotate(-1)    #rotate through death_images
                self.image = self.death_images[0]
                self.frame_counter += 1

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def check_hit_in_npc(self):
        if self.ray_cast_value and self.game.player.shot:   #if player shoots and there is actual line of sight
            if half_width - self.sprite_half_width < self.screen_x < half_width + self.sprite_half_width:
                self.game.sound.npc_pain.play() #play the npc pain sound we loaded in the sound file
                #if shot hit the npc sprite in the middle of the screen. shot ends, and npc is in pain
                self.game.player.shot = False
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.npc_death.play()

    def run_logic(self):
        if self.alive:  #if alive, check to see if the npc has been hit
            self.ray_cast_value = self.ray_cast_player_npc()
            self.check_hit_in_npc()

            if self.pain:   #if its been hit and is in pain, animate the pain sprite images
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)  #turn on idle images animation
        else:
            self.animate_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    #need to paste the majority of the ray_cast function in order to have ray casting here. changing name to ray_cast_player_npc and making updates
    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos   #don't fully understand the math but in theory it should work for any game based on a grid that uses ray casting
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta
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
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_dist_h = depth_hor
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
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h) #find max values of these distances
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:    #determine if there is a line of sight from player to npc or not
            return True
        return False

    def draw_ray_cast(self):    #draw in 2d to test
        pg.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)   #npc is red circle
        if self.ray_cast_player_npc():
            pg.draw.line(self.game.screen, "orange", (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)   #single ray is orange line for LOS between player and npc


class SoldierNPC(NPC):
    def __init__(self, game, path="resources/sprites/npc/soldier/0.png", pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CacoDemonNPC(NPC):
    def __init__(self, game, path="resources/sprites/npc/caco_demon/0.png", pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35


class CyberDemonNPC(NPC):
    def __init__(self, game, path="resources/sprites/npc/cyber_demon/0.png", pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 200
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25
