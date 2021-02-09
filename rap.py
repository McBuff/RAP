import pyautogui
import pyrect
import time
import keyboard
import logging
import os
import pytesseract
from fuzzywuzzy import fuzz
from playerstate import PlayerState
from gameui import GameUI

from utils import do_mousepoll, get_dock_uielement, get_route_root_uielement, get_route_blocks, read_num_jumps, DEFAULT_DOCKED_ROUTE_BLOCKS_REGION, get_box_center, read_warp_status


SCRIPT_START = time.time()

draw_buffer = []

GAMEUI = GameUI()
PLAYERSTATE = PlayerState(game_ui=GAMEUI)
LAST_FRAME_TIME  = time.time()
def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    consolechannel = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s]: %(message)s')
    consolechannel.setFormatter(formatter)
    logger.addHandler(consolechannel)
    # logger.info('THIS IS AN INFO LOG')
    return logger


logger = get_logger()
logger.info('Starting script')

update_events = []
player_state = 'docked'
script_state = 'waiting'



def get_eve_window_rect():
    oper_os = 'linux'
    oper_os = 'windows'
    if oper_os == 'windows':
        import pygetwindow
        win_hdn = pygetwindow.getWindowsWithTitle('EVE - Jayon Luthric')
        print('Did I find the rect??')
        print(win_hdn)

    elif oper_os == 'linux':
        # pyautogui.moveTo(1920,0,1)
        # print(pyautogui.getInfo())
        # print(pyautogui.position())
        
        rect = pyrect.Rect(1920,0,3840, 2160)
        rect = pyrect.Rect(1920,0,2560, 1440)

        return rect

    return None


def find_player_undock_button():
    undock_rect = pyautogui.locateOnScreen("uielements/undock.png", confidence=0.9)
    return undock_rect

def is_player_docked():
    logger.info('Finding undock button...')
    undock_rect = find_player_undock_button()

    # print(undock_rect)
    if undock_rect:
        return True

    logger.info("Didn't find undock button")
    logger.info('Finding velocimeter...')
    velocimeter_rect = pyautogui.locateOnScreen("uielements/velocity_random.png", confidence = 0.8)
    if velocimeter_rect:
        logger.info('Found velocimeter')

    return False

def is_player_warping():
    fuzzy_text = read_warp_status()
    target_text = 'WARP DRIVE ACTIVE'
    ratio = fuzz.ratio(fuzzy_text, target_text)
    logger.debug(f'Fuzzy Search: {fuzzy_text} - {target_text} : RATIO: {ratio}')
    if ratio > 90:
        return True
    return False
    # pass

def is_player_establishing_warp_vector():
    target_text = 'ESTABLISHING WARP VECTOR'
    fuzzy_text = read_warp_status()
    ratio = fuzz.ratio(fuzzy_text, target_text)
    logger.debug(f'Fuzzy Search: {fuzzy_text} - {target_text} : RATIO: {ratio}')
    if ratio > 90:
        return True
    return False
    # pass

def trigger_update_events():
    for update_event in update_events:
        update_event()

def draw():
    clear_console()
    global draw_buffer
    for drawing in draw_buffer:
        print(drawing)
    
    draw_buffer = []
    



def update_loop(updates_per_second = 2):
    do_loop = True
    print('Entered main loop')
    while do_loop:

        if keyboard.is_pressed('escape'):
            break

        global LAST_FRAME_TIME
        current_time = time.time()
        delta = current_time - LAST_FRAME_TIME
        if delta > (1/updates_per_second):
            sleeptime = (1/updates_per_second) - delta
            sleeptime = sleeptime if sleeptime > 0 else 0
            time.sleep(sleeptime)
            LAST_FRAME_TIME = current_time


        # time.sleep(1 /updates_per_second)

        trigger_update_events()
        global PLAYERSTATE
        global GAMEUI

        PLAYERSTATE.update()


        draw_buffer.append('Script time: {}s'.format( (time.time() - SCRIPT_START) / 1 ))
        draw_buffer.append('Player State: {}'.format(PLAYERSTATE.state))

        if PLAYERSTATE.state in ['idle', 'post-warp', 'jump']:
            GAMEUI.do_jump()
            # PLAYERSTATE.state = 'approach'
        
        if PLAYERSTATE.state =='docked':
            # global GAMEUI
            GAMEUI.do_undock()
            time.sleep(5)
        # draw_buffer.append('Script State: {}'.format(script_state))

def clear_console():
    import os
    clear = lambda: os.system('cls')
    clear()

def undock_player():
    undock_rect= find_player_undock_button()
    target_mousepos = get_box_center(undock_rect)
    pyautogui.moveTo(target_mousepos[0], target_mousepos[1], 0.5)
    pyautogui.click()
    global player_state, script_state
    player_state = 'undocking'
    script_state = 'waiting for undock'

def main():

    print('Initializing R.A.P.')
    pyautogui.FAILSAFE = True
    
    print('Searching for Host window')
    global EVE_WINDOW_RECT
    EVE_WINDOW_RECT = get_eve_window_rect()
    global player_state
    # if is_player_docked():
    #     print('Player is docked!')
    #     player_state = 'docked'
    # else:
    #     player_state = 'unknown'

    
    update_events.append(draw)
    update_events.append(do_mousepoll)
    # update_events.append(clear_console)



    update_loop()
    # screenshot_routelist()
    # get_undock_button_center()

    print('Finishing running R.A.P.')


def capture_screenshot_loop(interval=5000):
    filename = 0
    while True:
        pyautogui.screenshot(f"screenshot_{filename}.png")
        filename += 1
        time.sleep(interval/1000)



def read_docked_ui():
    get_dock_uielement()
    get_route_root_uielement()
    get_route_blocks()
    pass

if __name__ == '__main__':
    # # pyautogui.moveTo(200,200)
    # # capture_screenshot_loop()
    # # read_docked_ui()
    # read_num_jumps()
    # exit()
    main()
    # capture_screenshot_loop()