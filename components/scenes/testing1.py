import pygame
from typing import *
from constants import *
import components.events as events
import components.scenes as scenes
import components.element as element
from components.controller import controller

testing1 = scenes.Scene()

def init():
    # 一個製作 element 的函式
    def make_color_block(color: (255, 255, 255)):
        ele = element.Element((50, 50))
        ele.background_color = color
        return ele

    # 根據給定數據（rgb 值）製作一個 list 的 element
    children = [make_color_block(c) for c in [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
    ]]

    # 設置 parent_ele 的樣式
    parent_ele = element.Element()
    parent_ele.min_width = 150
    parent_ele.max_height = 400
    parent_ele.x = 50
    parent_ele.y = 50
    parent_ele.spacing = 25
    # 將 children 添加到 parent_ele
    parent_ele.append_child(*children)

    # 設置鼠標在元素上的樣式
    children[0].cursor = 'crosshair'
    children[1].cursor = 'sizeall'
    children[2].cursor = 'ibeam'
    children[3].cursor = 'hand'

    # 添加 click 事件監聽器
    def blue_clicked():
        print('blue clicked')
    children[2].add_event_listener(events.CLICK, blue_clicked)

    # 創建 image_ele1
    image_ele1 = element.Element(element.load_image('icon.png', (50, 50)))
    image_ele1.cursor = 'hand'

    # 添加 click 事件監聽器
    def image_ele_clicked():
        image_ele1.image = pygame.transform.flip(image_ele1.image, True, False)
    image_ele1.add_event_listener(events.CLICK, image_ele_clicked)

    # 創建 image_ele2
    image_ele2 = element.Element(element.load_image('entities/sun.png', (60, 60)))

    # 創建 image_ele3
    image_ele3 = element.Element(element.load_image('plants/demo.png', (128, 128)))
    image_ele3.image = pygame.transform.flip(image_ele3.image, True, False)
    image_ele3.rect.right = controller.screen_rect.right - 10
    image_ele3.rect.centery = controller.screen_rect.centery
    image_ele3.cursor = 'hand'
    def plant_demo_shoot():
        bullet = element.Element((10, 10))
        bullet.allow_flyout = False
        bullet.background_color = (255, 255, 255)
        def bullet_update():
            bullet.x -= 5
        bullet.update = bullet_update
        bullet.rect.centerx = image_ele3.rect.centerx - 32
        bullet.rect.centery = image_ele3.rect.centery - 18
        bullet.z_index = 99
        testing1.add_element(bullet)
    image_ele3.add_event_listener(events.CLICK, plant_demo_shoot)

    # 將 image_ele1, image_ele2 添加到 parent_ele
    parent_ele.append_child(image_ele1, image_ele2)
    def parent_update():
        print(tuple(testing1.elements_generator).__len__())
    parent_ele.update = parent_update
    # 重新添加 children[3] 到 parent_ele
    # - 這會導致 children[3] 從 parent_ele 中移除
    # - 然後 children[3] 會重新被添加到 parent_ele.childern 的尾部
    parent_ele.append_child(children[3])

    # 添加 click 事件監聽器（頁面轉跳）
    def goto_testing2():
        controller.goto_scene(controller.scenes.testing2)
    children[3].add_event_listener(events.CLICK, goto_testing2)

    # 將 parent_ele 添加到 testing1 場景
    testing1.add_element(parent_ele)

    # 將 image_ele3 添加到 testing1 場景
    testing1.add_element(image_ele3)

testing1.init = init
