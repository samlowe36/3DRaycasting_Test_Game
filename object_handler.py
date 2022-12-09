from sprite_object import *
from npc import *
from random import choices, randrange


class ObjectHandler:
    def __init__(self, game):
        self.game = game    #attribute for the game instance
        self.sprite_list = []   #attribute for list of sprites
        self.npc_list = []  #attribute for empty starting list of npc sprites
        self.npc_sprite_path = "resources/sprites/npc/" #path to npc folders
        self.static_sprite_path = "resources/sprites/static_sprites/"   #paths to sprite folders
        self.anim_sprite_path = "resources/sprites/animated_sprites/"   #paths to sprite folders
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        #spawn NPCs
        self.enemies = 20   #npc count
        self.npc_types = [SoldierNPC, CacoDemonNPC, CyberDemonNPC]
        self.weights = [70, 20, 10]
        self.restricted_area = {(i, j) for i in range(10) for j in range(10)}
        self.spawn_npc()

        #sprite map
        add_sprite(SpriteObject(game))  #adds static sprite to game
        add_sprite(AnimatedSprite(game))    #adds animated sprite to game
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))    #adds animated sprite in different position
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 4.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(14.5, 5.5)))   #adds the other sprite file
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(14.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(12.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(9.5, 7.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(14.5, 12.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(9.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(10.5, 20.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(3.5, 14.5)))
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/4.png', pos=(3.5, 18.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 24.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 30.5)))
        add_sprite(AnimatedSprite(game, pos=(1.5, 24.5)))

        #npc map (no longer needed after spawn function made)
        #add_npc(NPC(game))  #create instance of npc class and add it to game
        #add_npc(NPC(game, pos=(11.5, 4.5)))

    def spawn_npc(self):
        for i in range(self.enemies):
            npc = choices(self.npc_types, self.weights)[0]
            pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            while (pos in self.game.map.world_map) or (pos in self.restricted_area):
                pos = x, y = randrange(self.game.map.cols), randrange(self.game.map.rows)
            self.add_npc(npc(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(2000)
            self.game.new_game()

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}    #for making sure npc's dont occupy the same tile
        [sprite.update() for sprite in self.sprite_list]    #call update for all sprites in this list
        [npc.update() for npc in self.npc_list] #call update for all npc's in list
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append((npc))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite) #adds a sprite to the sprite_list