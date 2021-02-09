import pyrect
import pyautogui
import os
from PIL import Image, ImageEnhance
from utils import get_box_center

class GameUI(object):
    def __init__(self):
        pass

    def do_undock(self):
        undock_rect = self.get_undock_rect()
        target_mousepos = get_box_center(undock_rect)
        pyautogui.moveTo(target_mousepos[0], target_mousepos[1], 0.5)
        # logger.info('Undocking player')
        pyautogui.click()
        
        pass

    def do_jump(self):
        # * rmb on route
        pyautogui.moveTo(236, 378, 1)
        pyautogui.rightClick()
        # * click on jump

        pyautogui.moveTo(350, 400, 1)
        pyautogui.click()


        pass

    def get_undock_rect(self):
        rect = pyautogui.locateOnScreen("uielements/undock.png", confidence=0.9)
        return rect