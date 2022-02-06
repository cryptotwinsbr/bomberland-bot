# -*- coding: utf-8 -*-    
from cv2 import cv2
from os import listdir
from random import randint
from random import random
import numpy as np
import mss
import pyautogui
import time
import sys

# Tempo entre ações
pyautogui.PAUSE = 1
global x_scroll
global y_scroll
global h_scroll
global w_scroll

def addRandomness(n, randomn_factor_size=None):
    if randomn_factor_size is None:
        randomness_percentage = 0.1
        randomn_factor_size = randomness_percentage * n

    random_factor = 2 * random() * randomn_factor_size
    if random_factor > 5:
        random_factor = 5
    without_average_random_factor = n - randomn_factor_size
    randomized_n = int(without_average_random_factor + random_factor)
    return int(randomized_n)

def moveToWithRandomness(x,y,t):
    pyautogui.moveTo(addRandomness(x,10),addRandomness(y,10),t+random()/2)

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images(dir_path='./img_compare/'):
    file_names = listdir(dir_path)
    targets = {}
    for file in file_names:
        path = 'img_compare/' + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)
    return targets

def show(rectangles, img = None):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def clickBtn(img, timeout=3, threshold = 0.8):
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            has_timed_out = time.time()-start > timeout
            continue
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,0.5)
        pyautogui.click()
        return True

    return False

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def positions(target, threshold=0.8,img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]
    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def click_fight_ship():
    global x_scroll
    global y_scroll
    global h_scroll
    global w_scroll

    offset_x = 220
    offset_y = 50
    y_ship_final = 0

    green_bars = positions(images['blue-bar-short'], threshold=0.9)
    print('Blue bars detected', len(green_bars))
    buttons = positions(images['fight'], threshold=0.9)
    print('Buttons fight detected', len(buttons))

    for key,(x, y, w, h) in enumerate(buttons):
        print('key: ', key)
        if key == 0:
            x_scroll = x
            y_scroll = y
            h_scroll = h
            w_scroll = w
        elif key == 2:
            y_ship_final = y
            print("Y ship final: ", y_ship_final)        

    yellow_bars = positions(images['yellow-bar-short'], threshold=0.9)
    print('Yellow bars detected', len(yellow_bars))

    not_working_green_bars = []
    for bar in green_bars:
        not_working_green_bars.append(bar)
    for bar in yellow_bars:
        not_working_green_bars.append(bar)
    if len(not_working_green_bars) > 0:
        print('buttons with green bar detected', len(not_working_green_bars))
        print('Clicking in heroes', len(not_working_green_bars))
    hero_clicks_cnt = 0
    for (x, y, w, h) in not_working_green_bars:
        print("Entrou for x y w h. Y:", y)
        if ( y < y_ship_final+50):
            moveToWithRandomness(x+offset_x+(w/2),y+offset_y+(h/2),1)
            pyautogui.click()
            global hero_clicks
            hero_clicks = hero_clicks + 1
            hero_clicks_cnt = hero_clicks_cnt + 1
            if hero_clicks_cnt > 20:
                print('Too many hero clicks, try to increase the go_to_work_btn threshold')
                return
        else:
            print("Botao abaixo")
    return len(not_working_green_bars)

def scroll_ships():
    global x_scroll
    global y_scroll
    global h_scroll
    global w_scroll
    use_click_and_drag_instead_of_scroll = True
    click_and_drag_amount = 200
    scroll_size = 60

    moveToWithRandomness(x_scroll+(w_scroll/2),y_scroll+300+(h_scroll/2),1)
    if not use_click_and_drag_instead_of_scroll:
        pyautogui.scroll(-scroll_size)
    else:
        pyautogui.dragRel(0,-click_and_drag_amount,duration=1, button='left')

def go_to_continue():
    if clickBtn(images['confirm']):
        print('confirm clicked')
        return True
    else:
        return False

def go_to_ship():
    if clickBtn(images['ship']):
        print('ship clicked')
        return True
    else:
        return False

def go_to_fight():
    if clickBtn(images['fight-boss-new']):
        print('fight-boss clicked')

def ships_15_15():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(images['15-15'], 0.9)

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        print('Encontrou 15-15')
        return True
    return False

def ships_15_15_boss():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(images['15-15-boss'], 0.9)

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        print('Encontrou 15-15 boss')
        return True
    return False

def time_is_zero():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(images['time-zero'], 0.8)

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        print('Encontrou time-zero')
        return True
    print('Time diferente de zero')
    return False
       
def ship_to_fight():
    #if time_is_zero():
    if go_to_ship():
        buttonsClicked = 1
        empty_scrolls_attempts = 3
        while(empty_scrolls_attempts >0):
            buttonsClicked = click_fight_ship()
            if buttonsClicked == 0:
                empty_scrolls_attempts = empty_scrolls_attempts - 1
            if ships_15_15():
                break
            scroll_ships()
            time.sleep(1)
        go_to_fight()
    else:
        return
    #else:
    #    return

def go_to_ship_tela_boss():
    if clickBtn(images['ship-boss']):
        print('ship tela boss clicked')
        return True
    else:   
        return False

def ship_tela_boss():
    if ships_15_15_boss():
        return
    elif ships_15_15_boss() == False:        
        if go_to_ship_tela_boss():
            time.sleep(5)
            buttonsClicked = 1
            empty_scrolls_attempts = 3

            while(empty_scrolls_attempts >0):
                buttonsClicked = click_fight_ship()
                if buttonsClicked == 0:
                    empty_scrolls_attempts = empty_scrolls_attempts - 1
                if ships_15_15():
                    break
                scroll_ships()
                time.sleep(2)
            go_to_fight()

def main():
    global images    
    global hero_clicks
    hero_clicks = 0
    images = load_images()
    
    #print("""Opa beleza?""")
    '''print('Quantas naves(minimo) você deseja para iniciar a batalha?')
    qtd_ships = input()
    print('Quantidade de naves selecionadas: ' + qtd_ships)'''

    time.sleep(1)

    time_start = {
    "ship_to_fight" : 0,
    "ship" : 0,
    "fight" : 0,
    "fight_boss" : 0,
    "ship_tela_boss": 0,
    "continue": 0,
    }

    time_to_check = {
    "ship_to_fight" : 5,
    "ship" : 10,
    "fight" : 5,
    "fight_boss" : 20,
    "ship_tela_boss": 3,
    "continue": 5,
    }
    while True:
        actual_time = time.time()

        if actual_time - time_start["ship_to_fight"] > time_to_check['ship_to_fight']:
                time_start["ship_to_fight"] = actual_time
                print("Ship to fight")
                ship_to_fight()
        
        if actual_time - time_start["ship_tela_boss"] > time_to_check['ship_tela_boss']:
                time_start["ship_tela_boss"] = actual_time
                print("Ship tela boss")
                ship_tela_boss()

        if actual_time - time_start["continue"] > time_to_check['continue']:
                time_start["continue"] = actual_time
                print("Ship continue")
                go_to_continue()

        time.sleep(1)

if __name__ == '__main__':
    main()