import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

testing1 = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    
    # 創建 Level（關卡的數據, eg. 太陽）
    level = levels.Level()
    testing1.add_element(level)

    # 一個製作 element 的函式
    def make_color_block(color: (255, 255, 255)):
        ele = Element((50, 50))
        ele.background_color = color
        return ele

    # 根據給定數據（rgb 值）製作一個 list 的 element
    children = [make_color_block(c) for c in ((255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0))]

    # 添加 click 事件監聽器，當按下紅色方塊是會重新加載場景。
    children[0].add_event_listener(events.CLICK, lambda: testing1.reload())

    # 添加 click 事件監聽器，當按下綠色方塊時會掉下太陽。
    children[1].add_event_listener(events.CLICK, lambda: levels.SunSpawner().spawn(level))

    # 添加 click 事件監聽器（頁面轉跳）
    children[3].add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.testing2))

    # 設置鼠標在元素上的樣式
    children[0].cursor = 'crosshair'
    children[1].cursor = 'hand'
    children[2].cursor = 'hand'
    children[3].cursor = 'hand'

    # 創建 parent_ele 並設置樣式
    parent_ele = Element()
    parent_ele.min_width = 150
    parent_ele.min_height = 520
    parent_ele.rect.x = 50
    parent_ele.rect.y = 50
    parent_ele.spacing = 25

    # 將 children 添加到 parent_ele
    parent_ele.append_child(*children)

    # 創建 troll_face
    troll_face = Entity(media.load_image('troll.png', (50, 50)))
    troll_face.cursor = 'hand'

    # 添加 click 事件監聽器，當 troll face 被按下時它會左右反轉
    def image_ele_clicked():
        troll_face.image = pygame.transform.flip(troll_face.image, True, False)
    troll_face.add_event_listener(events.CLICK, image_ele_clicked)

    # 創建 demo_plant 並設置其屬性
    demo_plant = plants.Shooter(
        pygame.transform.flip(media.load_image('plants/demo.png', (128, 128)), True, False),
        plants.BulletTemplate(
            pygame.Surface((10, 10)),
            (0.26, 0.36),
            -10,
            (255, 0, 255),
            10,
            [Entity],
            [],
            media.load_sound('entities/bullet-demo.mp3'),
        )
    )
    demo_plant.rect.center = (controller.screen_rect.right - 10 - demo_plant.rect.width / 2, controller.screen_rect.centery)
    demo_plant.cursor_r = 'hand'
    demo_plant.radius_scale = 0.75
    demo_plant.add_event_listener(events.CLICK_R, lambda: demo_plant.shoot())

    # 將元素添加到 parent_ele
    parent_ele.append_child(troll_face)

    # 重新添加 children[3] 到 parent_ele
    parent_ele.append_child(children[3])

    # 創建一個 TextBox 綁定關卡的太陽數量
    parent_ele.append_child(TextBox(level.suns))

    # 將 Element 添加到場景
    testing1.add_element(parent_ele)
    testing1.add_element(demo_plant)

    # 創建導航
    navigator = Element()
    navigator.spacing = 16

    # 創建轉跳按鈕
    def create_link(scene_name: str, scene: scenes.Scene):
        element = TextBox(scene_name, 24)
        element.add_event_listener(events.CLICK, lambda: controller.goto_scene(scene))
        def mouseenter():
            element.font_color = (0, 0, 255)
        def mouseleave():
            element.font_color = None
        element.add_event_listener(events.MOUSEENTER, mouseenter)
        element.add_event_listener(events.MOUSELEAVE, mouseleave)
        element.cursor = 'hand'
        navigator.append_child(element)
    
    # 創建每個轉跳按鈕
    for scene_name, scene in (
        ('main_menu', scenes.main_menu),
        ('main_game', scenes.main_game),
        ('pause_menu', scenes.pause_menu),
        ('the_end', scenes.the_end),
    ): create_link(scene_name, scene)

    # 注意！透過 .rect 設置坐標的前，須先將 Element 添加到場景和排版。
    # 這是為了使子元素預先加載，以免坐標設置失敗。
    testing1.add_element(navigator)
    testing1.compose()
    navigator.rect.center = controller.screen_rect.center

    # 設置背景音樂
    # testing1.background_music = 'assets/soundtracks/Brainiac Maniac.mp3'

testing1.init = init
