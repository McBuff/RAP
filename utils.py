import time
import pyautogui
from PIL import Image, ImageEnhance
from imagelevels import level_image
import pytesseract
import cProfile
DEFAULT_DOCKED_ROUTE_BLOCKS_REGION = (140, 448, 378, 60)
DEFAULT_UNDOCK_REGION = (1636, 227, 240, 60)
DEFAULT_ROUTE_ROOT = (110, 345, 95, 25)

DEFAULT_WARPSTATE_REGION = (720, 630, 1180-720, 40)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# from pytessy import PyTessy

# print(pytesseract.image_to_string(Image.open('uielements/route_root.png')))
# exit()

def read_warp_status(region=(720, 630, 1180-720, 40)):
    warpstatus = ''
    # global DEFAULT_WARPSTATE_REGION
    # cProfile.run('pyautogui.screenshot(region=(720, 630, 1180-720, 40))')
    status_image = pyautogui.screenshot(region=DEFAULT_WARPSTATE_REGION)

    new_size = status_image.width * 0.5, status_image.height * 0.5
    status_image.thumbnail(new_size)
    status_image.save('scaled_warp_image.png')
    # cProfile.run('pytesseract.image_to_string(status_image)')
    warpstatus = pytesseract.image_to_string(status_image)
    # print(pytesseract.image_to_string(Image.open('test.png')))
    return warpstatus


def do_mousepoll():    
    print('Current Mouse Position: {}'.format(pyautogui.position()))

def get_dock_uielement():
    # pyautogui.screenshot()
    pyautogui.screenshot('uielements/undock.png', region=DEFAULT_UNDOCK_REGION)    
    

def get_route_root_uielement():
    pyautogui.screenshot('uielements/route_root.png', region=DEFAULT_ROUTE_ROOT)    
    pass



def get_route_blocks():
    pyautogui.screenshot('uielements/route_blocks.png', region=DEFAULT_DOCKED_ROUTE_BLOCKS_REGION)    


def get_box_center(box):
    x = box.left + box.width / 2
    y = box.top + box.height / 2

    return (x, y)
    pass

def read_num_jumps():
    jumps_image = pyautogui.screenshot(region=DEFAULT_DOCKED_ROUTE_BLOCKS_REGION)
    # jumps_image = Image.open('uielements/route_blocks.png')


    jumps_image = level_image(jumps_image, 140, 255, 1)
    # ImageEnhance.Contrast.
    jumps_image = ImageEnhance.Color(jumps_image).enhance(0)
    jumps_image = ImageEnhance.Brightness(jumps_image).enhance(1)
    jumps_image = ImageEnhance.Contrast(jumps_image).enhance(4)

    # ImageEnhance.
    jumps_image.save('test_img.png')
    
    jump_squares = pyautogui.locateAll(needleImage='uielements/route_block.png', haystackImage=jumps_image, grayscale=True, confidence=0.70)
    
    jump_squares = list(jump_squares)

    print(f'Found {len(list(jump_squares))} jumps')
    # return
    print('Iterating over squares')
    
    for square in jump_squares:
        center = get_box_center(square)
        pyautogui.moveTo(center[0] + DEFAULT_DOCKED_ROUTE_BLOCKS_REGION[0], center[1] + DEFAULT_DOCKED_ROUTE_BLOCKS_REGION[1], 0)
        time.sleep(0.25)

    pyautogui.moveTo(100,100)
    # time.sleep(3)
    
    # print(dir(jump_squares))

    pass


class GameScreen(object):
    
    def __init__(self, gamerect=(0, 0, 1920, 1080)):
        self._x = gamerect[0]
        self._y = gamerect[1]
        self._width = gamerect[2]
        self._height = gamerect[3]

    def convert_xy(self, x, y):
        
        newx = x * self._width
        newy = y * self._height

        return (newx + self._x, newy + self._y)
        
    
        # pass
