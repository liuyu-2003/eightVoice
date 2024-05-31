import cocos
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from game import VoiceGame
from skin import CustomizeSkinLayer  # 引入自定义皮肤层

# 创建一个菜单项的回调函数
def on_start():
    cocos.director.director.run(Scene(VoiceGame()))

def on_quit():
    cocos.director.director.window.close()

def on_customize_skin():
    cocos.director.director.run(Scene(CustomizeSkinLayer()))

# 创建一个自定义的菜单层
class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__()

        # 创建菜单项
        items = [
            MenuItem('开始游戏', on_start),
            MenuItem('退出', on_quit),
            MenuItem('自定义皮肤', on_customize_skin)
        ]

        self.create_menu(items, zoom_in(), zoom_out())

# 主函数
if __name__ == '__main__':
    # 初始化导演
    cocos.director.director.init(caption="Let's Go!", width=800, height=600)

    # 创建一个菜单场景并运行
    main_menu_scene = Scene(MainMenu())
    cocos.director.director.run(main_menu_scene)
