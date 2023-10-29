import pygame
from typing import *
from constants import *
import components.scenes as scenes

testing1 = scenes.Scene()

def init():
    from components import Element, load_image, load_animation, create_textbox, \
        events, Entity, Plant, Zombie, controller

    # 一個製作 element 的函式
    def make_color_block(color: (255, 255, 255)):
        ele = Element((50, 50))
        ele.background_color = color
        return ele

    # 根據給定數據（rgb 值）製作一個 list 的 element
    children = [make_color_block(c) for c in [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
    ]]

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
    parent_ele.min_height = 480
    parent_ele.x = 50
    parent_ele.y = 50
    parent_ele.spacing = 25

    # 將 children 添加到 parent_ele
    parent_ele.append_child(*children)

    # 創建 troll_face
    troll_face = Entity(load_image('icon.png', (50, 50)))
    troll_face.cursor = 'hand'

    # 添加 click 事件監聽器
    def image_ele_clicked():
        troll_face.image = pygame.transform.flip(troll_face.image, True, False)
    troll_face.add_event_listener(events.CLICK, image_ele_clicked)

    # 創建 demo_plant 並設置其屬性
    demo_plant = Plant(load_image('plants/demo.png', (128, 128)))
    demo_plant.image = pygame.transform.flip(demo_plant.image, True, False)
    demo_plant.rect.right = controller.screen_rect.right - 10
    demo_plant.rect.centery = controller.screen_rect.centery
    demo_plant.cursor = 'hand'
    # 哈咯！!

    # 創建子彈
    def plant_demo_shoot():
        bullet = Entity((10, 10))
        # 這樣設置是為了讓元素在超出屏幕時自動消失
        bullet.allow_flyout = False
        bullet.background_color = (255, 0, 255)
        bullet.velocity_x = -10
        bullet.rect.centerx = demo_plant.rect.centerx - 32
        bullet.rect.centery = demo_plant.rect.centery - 18
        bullet.collision_damage = 10
        bullet.collision_target_types.add(Entity)
        bullet.z_index = 99
        testing1.add_element(bullet)
    demo_plant.add_event_listener(events.CLICK, plant_demo_shoot)

    # 列印當前場景元素總數
    parent_ele.update = lambda: print(tuple(testing1.elements_generator).__len__())

    # 將元素添加到 parent_ele
    parent_ele.append_child(troll_face)

    # 重新添加 children[3] 到 parent_ele
    # - 這會導致 children[3] 從 parent_ele 中移除
    # - 然後 children[3] 會重新被添加到 parent_ele.childern 的尾部
    parent_ele.append_child(children[3])

    # 將 Element 添加到場景
    testing1.add_element(parent_ele)
    testing1.add_element(demo_plant)

    # 創建導航
    navigator = Element()
    navigator.spacing = 16

    # 創建轉跳按鈕
    def create_link(scene_name: str, scene: scenes.Scene):
        element = Element(create_textbox(scene_name, 24))
        element.add_event_listener(events.CLICK, lambda: controller.goto_scene(scene))
        def mouseenter():
            element.image = create_textbox(scene_name, 24, (0, 0, 255))
        def mouseleave():
            element.image = create_textbox(scene_name, 24)
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

testing1.init = init
