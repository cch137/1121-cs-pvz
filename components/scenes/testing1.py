import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

testing1 = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels
    from components.element import ElementV2, Style
    
    level = levels.Level()
    testing1.add_element(level)
    # 一個製作 element 的函式
    def make_color_block(color: (255, 255, 255)):
        ele = Element((50, 50))
        ele.background_color = color
        return ele

    # 根據給定數據（rgb 值）製作一個 list 的 element
    children = [make_color_block(c) for c in [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
    ]]

    # 添加 click 事件監聽器 (reload)
    children[0].add_event_listener(events.CLICK, lambda: testing1.reload())
    # 添加 click 事件監聽器 (sun)
    children[1].add_event_listener(events.CLICK, lambda: levels.SunSpawner().spawn(level))
    # 添加 click 事件監聽器
    children[2].add_event_listener(events.CLICK, lambda: print('blue clicked'))
    # 添加 click 事件監聽器（頁面轉跳）
    children[3].add_event_listener(events.CLICK, lambda: controller.goto_scene(controller.scenes.testing2))

    # 設置鼠標在元素上的樣式
    children[0].cursor = 'crosshair'
    children[1].cursor = 'sizeall'
    children[2].cursor = 'ibeam'
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
    troll_face = Entity(media.load_image('icon.png', (50, 50)))
    troll_face.cursor = 'hand'

    # 添加 click 事件監聽器
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

    # 列印當前場景元素總數
    # parent_ele.update = lambda: print(tuple(testing1.elements_generator).__len__())

    # 將元素添加到 parent_ele
    parent_ele.append_child(troll_face)

    # 重新添加 children[3] 到 parent_ele
    # - 這會導致 children[3] 從 parent_ele 中移除
    # - 然後 children[3] 會重新被添加到 parent_ele.childern 的尾部
    parent_ele.append_child(children[3])

    # 添加太陽數量
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
    for scene_name, scene in (
        ('main_menu', scenes.main_menu),
        ('main_game', scenes.main_game),
        ('pause_menu', scenes.pause_menu),
        ('the_end', scenes.the_end),
    ): create_link(scene_name, scene)

    # 注意！透過 .rect 設置坐標的時候，先將 Element 添加到場景
    # 然後使用 Scene.compose() 進行排版，最後才設置坐標
    # 這是為了防止坐標設置失敗（子元素尚未加載所導致的）
    testing1.add_element(navigator)
    testing1.compose()
    navigator.rect.center = controller.screen_rect.center

    # ElementV2 測試
    # import utils.asynclib as asynclib
    # from utils.refs import Ref
    # e2_bg = Ref((255, 255, 255))
    # e2 = ElementV2().apply(Style(width=100, height=100, background_color=e2_bg))
    # def e2_l1(): e2_bg.value = (88, 88, 88)
    # asynclib.set_timeout(e2_l1, 2000)
    # testing1.add_element(e2)

    # 設置背景音樂
    testing1.background_music = 'assets/soundtracks/Brainiac Maniac.mp3'

testing1.init = init
