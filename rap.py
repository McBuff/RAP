import pyautogui
import pyrect


def get_eve_window_rect():
    oper_os = 'linux'
    if oper_os == 'windows':
        import pygetwindow
        raise NotImplementedError('MS Windows not supported.. sorry')

    elif oper_os == 'linux':
        # pyautogui.moveTo(1920,0,1)
        # print(pyautogui.getInfo())
        # print(pyautogui.position())
        
        rect = pyrect.Rect(1920,0,3840, 2160)
        rect = pyrect.Rect(1920,0,2560, 1440)

        return rect

    return None

def get_undock_button_center():
    # dock_button_rect = pyrect.Rect(4139, 200, 300, 200)
    # pyautogui.screenshot('dockbutton.png',(4139, 200, 150, 50))
    try:
        res = pyautogui.locateOnScreen('dockbutton.png', confidence=0.8)
    except pyautogui.ImageNotFoundException as ex:
        print('Cannot find docking button. Are you in space?')
        return

    if not res:
        return
    
    print('Location of dock button: {}'.format(res))
    return pyautogui.center(res)
    # clickme = pyautogui.center(res)

    # pyautogui.moveTo(clickme[0], clickme[1], 1)
    # pyautogui.click()
    return 

def eve_undock():
    pass

def screenshot_routelist():
    try:
        pyautogui.screenshot('route.png', (1990, 230, 70, 20))
        return True
    except:
        return False
def get_route_list():
    pass

def main():
    print('Initializing R.A.P.')
    pyautogui.FAILSAFE = True
    
    print('Searching for Host window')
    global EVE_WINDOW_RECT
    EVE_WINDOW_RECT = get_eve_window_rect()

    mouse_pos = pyautogui.position()
    print('Mouse at pos {0}'.format(mouse_pos))

    screenshot_routelist()
    # get_undock_button_center()

    print('Finishing running R.A.P.')


if __name__ == '__main__':
    main()