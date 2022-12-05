from sprite_object import *


class Weapon(AnimatedSprite):
    def __init__(self, game, path="resources/sprites/weapon/shotgun/0.png", scale=0.4, animation_time=90):  #parameters for weapon sprites
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)  #scale all sprites to specified values
        self.images = deque(    #deque of scaled weapon sprites so they are in order
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (half_width - self.images[0].get_width() // 2, height - self.images[0].get_height())
#find position of weapon and make sure its centered on the screen
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)  #rotate through weapon sprites
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:   #stop cycling through weapon sprites once all have appeared and reload is complete
                    self.reloading = False
                    self.frame_counter = 0

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()