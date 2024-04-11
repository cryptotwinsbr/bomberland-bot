import time
import pyautogui
from .imageBomb import ImageBomb
from .utils import *


def click_on_multiple_targets(target: str, not_click:str= None, filter_func = None):
    targets_positions = ImageBomb.get_target_positions(target, not_target=not_click)
    n_before = (len(targets_positions))
    if filter_func is not None:
        targets_positions = filter(filter_func, targets_positions)
    click_count = 0
    for x, y, w, h in targets_positions:
        x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
        pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
        time.sleep(time_between)
        pyautogui.click(duration=click_duration)
        click_count += 1
    
    return click_count    

def click_one_target(target: str):
    result = None
    try:
        x_left, y_top, w, h = ImageBomb.get_one_target_position(target)
        x, y, move_duration, click_duration, time_between  = randomize_values(x_left, w, y_top, h)
        pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
        time.sleep(time_between)
        pyautogui.click(duration=click_duration)
        result = True
    except Exception as e:
        return None
    
    return result

def click_randomly_in_position(x, y, w, h):
    x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
    pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
    time.sleep(time_between)
    pyautogui.click(duration=click_duration)


def click_when_target_appears(target: str, time_beteween: float = 0.5, timeout: float = 10):
    return do_with_timeout(click_one_target, args = [target])


def randomize_values(x, w, y, h):
    x_rand = randomize_int(x, w, 0.20)
    y_rand = randomize_int(y, h, 0.20)
    move_duration = randomize(0.1, 0.5)
    click_duration = randomize(0.05, 0.2)
    time_between = randomize(0.05, 0.3)
    return x_rand, y_rand, move_duration, click_duration, time_between

def move_to(target:str):
    def move_to_logical():
        try:
            x, y, w, h = ImageBomb.get_one_target_position(target)
            x, y, move_duration, click_duration, time_between  = randomize_values(x, w, y, h)
            pyautogui.moveTo(x, y, duration=move_duration, tween=pyautogui.easeOutQuad)
            return True
        except Exception as e:
            return None

    return do_with_timeout(move_to_logical)

def scroll_and_click_on_targets(safe_scroll_target: str, repeat: int, distance:float, duration: float, wait:float, function_between, execute_before=True):
    res = []
    if execute_before:
        res.append(function_between())
    for i in range(repeat):
        move_to(safe_scroll_target)
        pyautogui.mouseDown(duration=0.1)
        pyautogui.moveRel(0, distance, duration)
        time.sleep(0.3)
        pyautogui.mouseUp(duration=0.1)
        time.sleep(wait)
        click_when_target_appears(safe_scroll_target)
        res.append(function_between())        
    return res