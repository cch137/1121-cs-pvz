import pygame
from typing import *
from utils.constants import *
import components.scenes as scenes

testing2 = scenes.Scene()

def init():
    from components import Element, TextBox, media, \
        events, Entity, plants, zombies, controller, levels

    # 創建 outer_element
    outer_element = Element()
    outer_element.min_width = WINDOW_WIDTH
    outer_element.min_height = WINDOW_HEIGHT

    # 創建 inner_element
    inner_element = Element((600, 400))
    inner_element.background_color = (255, 0, 0)
    inner_element.spacing = 10
    inner_element.padding = 10
    inner_element.align_items = END
    inner_element.justify_content = START

    # 創建 btn1, btn2, btn3
    btn1 = Element((300, 80))
    btn1.background_color = (0, 255, 255)
    btn2 = Element((300, 80))
    btn2.background_color = (0, 255, 0)
    btn3 = Element((300, 80), ROW)
    btn3.background_color = (0, 255, 0)
    btn3.spacing = 15

    # 創建 btn3_1, btn3_2, btn3_3
    btn3_1 = Element((75, 50))
    btn3_1.background_color = (0, 0, 255)
    btn3_2 = Element((75, 50))
    btn3_2.background_color = (0, 0, 255)
    btn3_3 = Element((75, 50))
    btn3_3.background_color = (0, 0, 255)

    # 添加 click 事件監聽器（頁面轉跳）
    def goto_testing1():
        controller.goto_scene(controller.scenes.testing1)
    btn1.add_event_listener(events.CLICK, goto_testing1)
    btn1.cursor = 'hand'

    # 把 elements 添加到父級元素
    outer_element.append_child(inner_element)
    inner_element.append_child(btn1, btn2, btn3)
    btn3.append_child(btn3_1, btn3_2, btn3_3)

    # 創建 textbox
    text_element = TextBox('Hello World', 32)
    text_element.rect.x = 20
    text_element.rect.y = 20
    testing2.add_element(text_element)

    # 把 outer_element 添加到 testing2 場景
    testing2.add_element(outer_element)

    # 設置背景音樂
    testing2.background_music = 'assets/soundtracks/Rigor Mormist.mp3'

testing2.init = init
