# -*- coding: utf-8 -*-
import math
import random
import cocos

class Block(cocos.sprite.Sprite):
    def __init__(self, pos):
        super(Block, self).__init__('black.png')
        self.image_anchor = 0, 0#图像坐标原点
        x, y = pos
        if x == 0:
            self.scale_x = 5
            self.scale_y = 1
        else:
            self.scale_x = 0.5 + random.random() * 1.5
            self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100.0#决定大小
            self.position = x + 50 + random.random() * 100, 0#决定位置
