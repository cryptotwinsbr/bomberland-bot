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
from debug import Debug

VERSAO_SCRIPT = "1.02"

# Tempo entre ações
pyautogui.PAUSE = 0.2

# Definicao de quatidade de naves
empty_qtd_spaceships = 60
qtd_send_spaceships = 15
qtd_refresh_ships = 0 
cont_boss = 1

global x_scroll
global y_scroll
global h_scroll
global w_scroll

dbg = Debug('debug.log')

str_in = """
            ░░░░░░░█▐▓▓░████▄▄▄█▀▄▓▓▓▌█
            ░░░░░▄█▌▀▄▓▓▄▄▄▄▀▀▀▄▓▓▓▓▓▌█
            ░░░▄█▀▀▄▓█▓▓▓▓▓▓▓▓▓▓▓▓▀░▓▌█
            ░░█▀▄▓▓▓███▓▓▓███▓▓▓▄░░▄▓▐█▌
            ░█▌▓▓▓▀▀▓▓▓▓███▓▓▓▓▓▓▓▄▀▓▓▐█
            ▐█▐██▐░▄▓▓▓▓▓▀▄░▀▓▓▓▓▓▓▓▓▓▌█▌
            █▌███▓▓▓▓▓▓▓▓▐░░▄▓▓███▓▓▓▄▀▐█
            █▐█▓▀░░▀▓▓▓▓▓▓▓▓▓██████▓▓▓▓▐█
            ▌▓▄▌▀░▀░▐▀█▄▓▓██████████▓▓▓▌█▌
            ▌▓▓▓▄▄▀▀▓▓▓▀▓▓▓▓▓▓▓▓█▓█▓█▓▓▌█▌
            █▐▓▓▓▓▓▓▄▄▄▓▓▓▓▓▓█▓█▓█▓█▓▓▓▐█ 
    +++++++++++++++++++++++++++++++++++++++++++++++
    +++ 🌙 Melhorando nossas noites de sono 🌙 +++
    +++ Se te ajudamos, por favor contribua 😊🚀++
    ++++++++++++ SPG SPE BCOIN BUSD BNB +++++++++++
    + 0x73933b679F940ea7352c3895852501e3044FE855 ++
    ++++++++++++++++ Pix key ++++++++++++++++++++++
    ++++ 5f3d220c-a2a3-4db2-bfb2-30ae0533e240 +++++

    >> Ctrl + c finaliza o bot.
    
    
    """

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

def clickBtn(img,name=None, timeout=3, threshold = 0.7):
    if not name is None:
        pass
    start = time.time()
    while(True):
        matches = positions(img, threshold=threshold)
        if(len(matches)==0):
            hast_timed_out = time.time()-start > timeout
            if(hast_timed_out):
                if not name is None:
                    pass

                return False
            continue
        x,y,w,h = matches[0]
        pos_click_x = x+w/2
        pos_click_y = y+h/2
        moveToWithRandomness(pos_click_x,pos_click_y,1)
        pyautogui.click()
        return True

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def positions(target, threshold=0.7,img = None):
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

def processLogin():
    dbg.console('Starting Login', 'INFO', 'ambos')
    sys.stdout.flush()
    loginSPG()
    time.sleep(3)
    playSPG()

def scroll(clickAndDragAmount):
    flagScroll = positions(images['spg-flag-scrool'], 0.8)    
    if (len(flagScroll) == 0):
        return
    x,y,w,h = flagScroll[len(flagScroll)-1]
    moveToWithRandomness(x,y,1)
    pyautogui.dragRel(0,clickAndDragAmount,duration=1, button='left')


def loginSPG():
    global login_attempts    
    if login_attempts > 3:
        dbg.console('Too many login attempts, refreshing', 'ERROR', 'ambos')
        login_attempts = 0
        processLogin()
        return
    if clickBtn(images['connect-wallet'], name='connectWalletBtn', timeout = 10):
        dbg.console('Connect wallet button detected, logging in!', 'INFO', 'ambos')
        login_attempts = login_attempts + 1
    if clickBtn(images['sign'], name='sign button', timeout=8):
        login_attempts = login_attempts + 1
        return
    if not clickBtn(images['select-wallet-1-no-hover'], name='selectMetamaskBtn'):
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = 0.8 ):
            pass
    else:
        pass
    if clickBtn(images['sign'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1

def playSPG():
    if clickBtn(images['play'], name='okPlay', timeout=5):
        dbg.console('played SPG','INFO', 'ambos')

def login():
    if clickBtn(images['connect-wallet'], name='conectBtn', timeout=5):
        processLogin() 
        return True
    else:
        return False

def confirm():
    global cont_boss
    confirm_action = False
    if clickBtn(images['confirm'], name='okBtn', timeout=1):
        dbg.console('Confirm encontrado','INFO', 'ambos')
        time.sleep(2) 
        endFight()  
        confirm_action = True
    if clickBtn(images['confirm-victory'], name='okVicBtn', timeout=1):
        dbg.console('Confirm victory encontrado','INFO', 'ambos')
        dbg.console('Boss ' + str(cont_boss) + " derrotado",'INFO', 'ambos')
        cont_boss = cont_boss + 1
        confirm_action = True
        if cont_boss == 9:
            time.sleep(30) 
            dbg.console("Boss 8, refresh ships", 'DEBUG', 'ambos')
            clickBtn(images['ship'])
        if cont_boss == 14:
            time.sleep(30) 
            dbg.console("Boss 14, refresh ships", 'DEBUG', 'ambos')
            clickBtn(images['ship'])
        if cont_boss == 19:
            time.sleep(30) 
            dbg.console("Boss 19, refresh ships", 'DEBUG', 'ambos')
            clickBtn(images['ship'])
    return confirm_action

def removeSpaceships():
    time.sleep(2)   
    while True: 
        buttons = positions(images['spg-x'], threshold=0.9)
        buttonsNewOrder = []
        if len(buttons) > 0:
            index = len(buttons)
            while index > 0:
                index -= 1
                buttonsNewOrder.append(buttons[index])
            for (x, y, w, h) in buttonsNewOrder:
                moveToWithRandomness(x+(w/2),y+(h/2),1)
                pyautogui.click()
        if len(buttons) == 0:
            break

def clickButtonsFight():
    global qtd_send_spaceships
    buttons = positions(images['spg-go-fight'], 0.9)
    for (x, y, w, h) in buttons:
        moveToWithRandomness(x+(w/2),y+(h/2),1)
        pyautogui.click()
        global ships_clicks
        ships_clicks = ships_clicks + 1        
        if ships_clicks >= qtd_send_spaceships:
            dbg.console('Finish Click ships', 'INFO', 'ambos')
            return -1
    return len(buttons)

def refreshPage():
    pass


def screen_close():
    global cont_boss
    if clickBtn(images['close']):
        dbg.console('Encontrou close', 'ERROR', 'ambos')        
        cont_boss = 1
        return True
    else:
        return False

def reloadSpacheship():
    global cont_boss
    if len(positions(images['spg-base'], 0.8)) > 0 and len(positions(images['fight-boss'], 0.9))  > 0:
        clickBtn(images['spg-base'], name='closeBtn', timeout=1)
        time.sleep(3)
        clickBtn(images['ship'], name='closeBtn', timeout=1)
        time.sleep(3)        
        cont_boss = 1

def refreshSpaceships(qtd):
    global empty_qtd_spaceships
    global qtd_send_spaceships
    dbg.console('Refresh Spaceship to Fight', 'INFO', 'ambos')
    buttonsClicked = 1
    cda =  100
    
    global ships_clicks
    ships_clicks = 0
    empty_scrolls_attempts = qtd_send_spaceships   

    if qtd > 0:
        ships_clicks = qtd
        dbg.console('Quantidade ja selecionada:' + str(ships_clicks), 'DEBUG', 'ambos')
        if ships_clicks == qtd_send_spaceships:
            empty_scrolls_attempts = 0
            goToFight()
    while(empty_scrolls_attempts >0):
        buttonsClicked = clickButtonsFight()        
        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
            scroll(-cda)
        else:
            if buttonsClicked == -1:
                empty_scrolls_attempts = 0   
            else:
                if buttonsClicked > 0:
                    empty_scrolls_attempts = empty_scrolls_attempts + 1

        time.sleep(2)
        dbg.console('Spaceships sent to Fight: ' + str(ships_clicks), 'INFO', 'ambos')

    if ships_clicks == qtd_send_spaceships:
        empty_scrolls_attempts = 0
        goToFight()
    else:
        reloadSpacheship()
        refreshSpaceships(ships_clicks)
        
def goToFight():
    clickBtn(images['fight-boss'])
    time.sleep(1)
    clickBtn(images['confirm'])

def endFight():
    global cont_boss    
    cont_boss = 1
    dbg.console("End fight", 'INFO', 'ambos')
    time.sleep(3) 
    returnBase()
    time.sleep(15) 
    if len(positions(images['spg-processing'], 0.9)) > 0:
        time.sleep(40) 
    if len(positions(images['fight-boss'], 0.9))  > 0:
        removeSpaceships()
        time.sleep(1) 
        refreshSpaceships(0)
    else:
        refreshPage()

def goToSpaceShips():
    if clickBtn(images['ship']):
        global login_attempts
        login_attempts = 0

def returnBase():
    goToSpaceShips()

def lifeBoss():
    lessPosition = positions(images['spg-life-boss-1'], 0.9)
    if len(lessPosition) == 0:
        lessPosition = positions(images['spg-life-boss-2'], 0.9)                    
    if len(lessPosition) == 0:
        lessPosition = positions(images['spg-life-boss-3'], 0.9)
    return lessPosition

def zero_ships():
    if len(positions(images['spg-surrender'], 0.8)  ) > 0:
        start = time.time()
        has_timed_out = False
        while(not has_timed_out):
            matches = positions(images['0-15'], 0.9)
            #dbg.console("Result boss 9: " + str(len(matches)), 'DEBUG', 'ambos')
            if(len(matches)==0):
                has_timed_out = time.time()-start > 3
                continue
            elif(len(matches)>0):
                clickBtn(images['ship'])
                return True
    return False
                  

def main():
    global images    
    global ship_clicks
    global login_attempts
    ship_clicks = 0
    login_attempts = 0
    images = load_images()

    print(str_in)        
    time.sleep(5)
    dbg.console('Bot Iniciado. Versao: ' + str(VERSAO_SCRIPT), 'INFO', 'ambos')

    time_start = {
    "close" : 0,
    "login" : 0,
    }
    time_to_check = {
    "close" : 5,  
    "login" : 1,
    }

    while True:
        actual_time = time.time()

        action_found = False

        if actual_time - time_start["login"] > addRandomness(time_to_check['login'] * 1):
            sys.stdout.flush()
            time_start["login"] = actual_time
            if not login():
                if len(positions(images['fight-boss'], 0.9))  > 0:
                    removeSpaceships()
                    refreshSpaceships(0)
                    action_found = True
            else:
                action_found = True     

        if confirm():
            action_found = True 

        if zero_ships():
            action_found = True       
        
        if actual_time - time_start["close"] > time_to_check['close']:
            time_start["close"] = actual_time
            if screen_close():
                action_found = True

        if action_found == False:
            dbg.console('Nenhuma acao encontrada', 'WARNING', 'ambos')

if __name__ == '__main__':
    main()