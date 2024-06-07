import cocos
from cocos.layer import *
from cocos.sprite import Sprite
from cocos.text import Label
from cocos.menu import Menu, MenuItem, shake, shake_back
from cocos.scene import *
from game import VoiceGame
import requests
import os
from io import BytesIO
from PIL import Image


class CustomizeSkinLayer(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(CustomizeSkinLayer, self).__init__()
        self.text = ""
        self.result = None

        self.label = Label('描述皮肤:', font_size=28, anchor_x='center', anchor_y='center')
        self.label.position = 400, 500
        self.add(self.label)

        self.description_box = Label('', font_size=18, color=(255, 255, 255, 255), anchor_x='center', anchor_y='center')
        self.description_box.position = 400, 450
        self.add(self.description_box)

        # 创建菜单项
        items = [
            MenuItem('提交', self.on_submit),
            MenuItem('返回菜单', self.on_back)
        ]

        # 创建菜单
        self.menu = Menu()
        self.menu.create_menu(items, shake(), shake_back())
        self.menu.position = 200, 284
        self.add(self.menu)

    def on_key_press(self, symbol, modifiers):
        if symbol == ord('\r'):
            self.on_submit()
        elif symbol == ord('\b'):
            self.text = self.text[:-1]
        else:
            self.text += chr(symbol)
        self.description_box.element.text = self.text

    def on_submit(self):
        self.generate_skin(self.text)

    def on_back(self):
        cocos.director.director.run(Scene(MainMenu()))  # 返回主菜单

    def generate_skin(self, description):
        try:
            response = requests.post('https://api.holdai.top/v1/images/generations', json={
                'prompt': description+",Make this image appear to be a 3D image",
                'size': '256x256',
                'model': 'dall-e-2'
            }, headers={
                'Authorization': 'Bearer sk-nK4cuB3SIyI2SMRMD5Ba69DcCb184dEaBf9926E367719187'  # 确保替换为你的API Key
            })

            if response.status_code == 200:
                response_data = response.json()

                # 打印完整的返回数据以调试
                print(response_data)

                if 'data' in response_data and len(response_data['data']) > 0 and 'url' in response_data['data'][0]:
                    image_url = response_data['data'][0]['url']
                    image_response = requests.get(image_url)

                    if image_response.status_code == 200:
                        image_data = image_response.content
                        image = Image.open(BytesIO(image_data))

                        # 调整图像大小为80x56
                        resized_image = image.resize((80, 56))

                        # 保存生成的图像
                        resized_image.save('player.png')
                        print('Image generated, resized to 80x56, and saved as player.png')

                        if self.result:
                            self.remove(self.result)
                        self.result = Sprite('player.png')
                        self.result.position = 400, 200
                        self.add(self.result)
                    else:
                        print('Failed to download image from URL')
                else:
                    print('Generated data is not a valid image')
            else:
                print('Error generating skin:', response.text)
        except Exception as e:
            print('Error during skin generation:', e)


class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__()

        items = [
            MenuItem('开始游戏', on_start),
            MenuItem('退出', on_quit),
            MenuItem('自定义皮肤', on_customize_skin)
        ]

        self.create_menu(items, shake(), shake_back())


def on_start():
    cocos.director.director.run(Scene(VoiceGame()))


def on_quit():
    cocos.director.director.window.close()


def on_customize_skin():
    cocos.director.director.run(Scene(CustomizeSkinLayer()))
