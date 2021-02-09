"""Contains the playerstate. Call Playerstate Update Once every cycle, then interact with the class properties to retreive info
"""
import pyrect
import pyautogui
import os
from PIL import Image, ImageEnhance
from utils import read_warp_status
from fuzzywuzzy import fuzz
from gameui import GameUI
import cProfile

class PlayerState(object):

    def __init__(self, game_ui, gamerect=(0,0,1920,1080), liveuidir='liveui', uielementsdir='uielements'):
        self._region = gamerect
        self._state = 'unknown'
        self._previousstate = 'unknown'
        self._liveuidir = liveuidir
        self._uielementsdir = uielementsdir
        self._gameui = game_ui

        pass

    def _update_state(self, newstate:str):

        if newstate == self._previousstate:
            return
        else:
            self._previousstate = self._state
            self._state = newstate
            return
    
    def _read_game_state(self):
        # * let's first check if the player is docked, if not, let's find out if he's in space
        # cProfile.run('read_warp_status()')
        warp_message = read_warp_status()
        if fuzz.ratio(warp_message, 'WARP DRIVE ACTIVE') > 90:
            self._update_state('warp')
            return
        
        if fuzz.ratio(warp_message, 'ESTABLISHING WARP VECTOR') > 90:
            self._update_state('pre-warp')
            return

        if fuzz.ratio(warp_message, 'JUMPING') > 90:
            self._update_state('jump')
            return

        if fuzz.ratio(warp_message, 'APPROACHING') > 90:
            self._update_state('approach')
            return

        undock_rect = self._gameui.get_undock_rect()
        if undock_rect:
            self._update_state('docked')
            return

        if self.state == 'warp':
            self._update_state('post-warp')
            return

        if self._previousstate in ['unknown', 'jump']:
            self._update_state('idle')

    def _capture_game_area(self):
        target_file = os.path.join(self._liveuidir, 'game.png')
        pyautogui.screenshot(target_file, region=self._region)
        pass

    def update(self):
        self._capture_game_area()
        self._read_game_state()
        pass
    
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, x):
        self._update_state(x)

    @property
    def previoous_state(self):
        return self._previousstate

    @property
    def docked(self):
        return self._state == 'docked'
        

    @property
    def idle(self):
        return self._state == 'idle'
        

    @property
    def warping(self):
        return self._state == 'warp'
        

    @property
    def establishing_warp_vector(self):
        return self._state == 'pre-warp'
        

    @property
    def jumping(self):
        return self._state == 'jump'
        