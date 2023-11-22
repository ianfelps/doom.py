from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path='resources/sprites/weapon/shotgun/0.png', scale=0.4, animation_time=90):
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale)) for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 60

        self.vertical_offset = 0
        self.vertical_speed = 2
        self.moving_up = True
        self.horizontal_offset = 0
        self.horizontal_speed = 2
        self.moving_right = True

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.frame_counter = 0
                    self.reloading = False

    def draw(self):
        weapon_y = self.weapon_pos[1] + self.vertical_offset
        weapon_x = self.weapon_pos[0] + self.horizontal_offset
        self.game.screen.blit(self.images[0], (weapon_x, weapon_y))

    def weapon_swing(self):
        if self.moving_up:
            self.vertical_offset -= self.vertical_speed
            if self.vertical_offset <= 0:
                self.moving_up = False
        else:
            self.vertical_offset += self.vertical_speed
            if self.vertical_offset >= 35:
                self.moving_up = True

        if self.moving_right:
            self.horizontal_offset += self.horizontal_speed
            if self.horizontal_offset >= 35:
                self.moving_right = False
        else:
            self.horizontal_offset -= self.horizontal_speed
            if self.horizontal_offset <= -35:
                self.moving_right = True

    def update(self):
        self.check_animation_time()
        self.animate_shot()
        if self.game.player.player_moving:
            self.weapon_swing()