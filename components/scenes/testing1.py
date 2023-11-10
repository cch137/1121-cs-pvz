import pygame
from typing import *
from constants import *
import components.scenes as scenes

testing1 = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, Plant, Zombie, controller, levels
    
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
    parent_ele.x = 50
    parent_ele.y = 50
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
    demo_plant = Plant(media.load_image('plants/demo.png', (128, 128)))
    demo_plant.image = pygame.transform.flip(demo_plant.image, True, False)
    demo_plant.rect.right = controller.screen_rect.right - 10
    demo_plant.rect.centery = controller.screen_rect.centery
    demo_plant.cursor = 'hand'

    # 發射子彈子彈
    def plant_demo_shoot():
        bullet = Entity((10, 10)) # 創建子彈
        bullet.allow_flyout = False # 讓元素在超出屏幕時自動消失
        bullet.background_color = (255, 0, 255) # 設置背景顏色
        bullet.velocity_x = -10 # 設置速度
        bullet.rect.center = (demo_plant.rect.centerx - 32, demo_plant.rect.centery - 18) # 設置初始坐標
        bullet.collision_damage = 10 # 設置碰撞傷害
        # 將 Entity 設為碰撞目標，也就是當它與 Entity 發生碰撞時，會對那個 Entity 造成傷害
        bullet.collision_targets.add(Entity)
        bullet.z_index = 99 # 提高元素所在的層次，以確保它在繪製時能覆蓋其他元素
        testing1.add_element(bullet) # 把子彈添加到場景
        bullet_sound.play()
    bullet_sound = pygame.mixer.Sound('assets/entities/bullet-demo.mp3')
    demo_plant.add_event_listener(events.CLICK, plant_demo_shoot)

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

    # 設置背景音樂
    testing1.background_music = 'assets/soundtracks/Brainiac Maniac.mp3'

testing1.init = init
