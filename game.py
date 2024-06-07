import cocos
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
import struct
import os
from player import player
from block import Block
import pyglet

class VoiceGame(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(VoiceGame, self).__init__(255, 255, 255, 0
                                        , 800, 600)

        # 加载您选择的背景图片
        background_texture = pyglet.image.load('Designer.png')

        # 创建一个精灵并设置纹理
        background_sprite = Sprite(background_texture)
        background_sprite.position = 0, 0  # 设置精灵的位置为屏幕中心
        background_sprite.image_anchor = 0, 0  # 设置锚点为左下角
        self.add(background_sprite, z=0)  # 将精灵添加到图层中，并设置z顺序为0

        # init voice
        self.NUM_SAMPLES = 1000  # pyAudio内部缓存的块的大小
        self.LEVEL = 1500  # 声音保存的阈值

        self.voicebar = Sprite('black.png', color=(0, 0, 255))
        self.voicebar.position = 20, 450
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0, 0
        self.add(self.voicebar)

        self.player = player()
        self.add(self.player)

        self.shadow = player()
        self.shadow.isShadow = True
        self.add(self.shadow)

        # 加载新生成的图像
        if os.path.exists('player.png'):
            self.player.image = pyglet.image.load('player.png')
            self.shadow.image = pyglet.image.load('sd.jpeg')

        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        pos = 0, 100
        for i in range(100):
            b = Block(pos)
            self.floor.add(b)
            pos = b.x + b.width, b.height

        # 开启声音输入
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)

        self.schedule(self.update)

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def collide(self):
        px = self.player.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.player.width * 0.8 and px + self.player.width * 0.2 <= b.x + b.width:
                if self.player.y < b.height:
                    self.player.land(b.height)
                    break

        px = self.shadow.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.shadow.width * 0.8 and px + self.shadow.width * 0.2 <= b.x + b.width:
                if self.shadow.y < b.height:
                    self.shadow.land(b.height)
                    break

    def update(self, dt):
        # 读入NUM_SAMPLES个取样
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('1000h', string_audio_data))
        # print k
        self.voicebar.scale_x = k / 10000.0
        if k > 3000:
            self.floor.x -= min((k / 20.0), 150) * dt
        if k > 8000:
            self.player.jump((k - 8000) / 1000.0)
            self.shadow.jump((k - 8000) / 1000.0)
        self.collide()

    def reset(self):
        self.floor.x = 0
