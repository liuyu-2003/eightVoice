# -*- coding: utf-8 -*-
import math
import random
import cocos

class player(cocos.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__('player.png')
        self.can_jump = False
        self.speed = 0
        self.image_anchor = 0, 0
        self.position = 100, 300
        self.schedule(self.update)

    def jump(self, h):
        if self.can_jump:
            self.y += 1
            self.speed -= max(min(h, 10), 7)
            self.can_jump = False#精灵正在空中，不能再次跳跃

    def land(self, y):
        if self.y > y - 30:
            self.can_jump = True
            self.speed = 0
            self.y = y

    def update(self, dt):
        self.speed += 10 * dt
        self.y -= self.speed
        if self.y < -80:
            self.reset()

    def reset(self):
        self.parent.reset()
        self.can_jump = False
        self.speed = 0
        self.position = 100, 300
