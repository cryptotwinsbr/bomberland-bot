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
import yaml

VERSAO_SCRIPT = "1.06"

# Tempo entre ações
pyautogui.PAUSE = 0.2

# Load config file.
stream = open("settings.yaml", 'r')
c = yaml.safe_load(stream)
st = c['ship_settings']
th = c['threshold']

ships_clicks = 0
cont_boss = 1
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

    * Algumas configurações podem ser alteradas em 
    settings.yaml

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

def clickBtn(img,name=None, timeout=3, threshold = th['default']):
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

def positions(target, threshold=th['default'],img = None):
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
    time.sleep(2)
    playSPG()

def scroll(clickAndDragAmount):
    flagScroll = positions(images['spg-flag-scrool'], th['commom'])    
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
        if clickBtn(images['select-wallet-1-hover'], name='selectMetamaskHoverBtn', threshold  = th['commom'] ):
            pass
    else:
        pass
    if clickBtn(images['sign'], name='signBtn', timeout = 20):
        login_attempts = login_attempts + 1

def playSPG():
    if clickBtn(images['play'], name='okPlay', timeout=8):
        dbg.console('played SPG','INFO', 'ambos')

def login():
    if len(positions(images['connect-wallet'], th['commom'])) > 0:
        processLogin() 
        return True
    else:
        return False

def confirm():
    global cont_boss
    confirm_action = False
    if len(positions(images['lose'], th['commom'])) > 0 and cont_boss > 1:
        if clickBtn(images['confirm'], name='okBtn', timeout=1, threshold  = th['commom']):
            dbg.console('Confirm encontrado','INFO', 'ambos')
            time.sleep(2) 
            endFight()  
            confirm_action = True
    if len(positions(images['victory'], th['commom'])) > 0:
        if clickBtn(images['confirm-victory'], name='okVicBtn', timeout=2) or clickBtn(images['confirm-bf'], name='okVicBtn', timeout=2):
            dbg.console('Confirm victory encontrado','INFO', 'ambos')
            dbg.console('Boss ' + str(cont_boss) + " derrotado",'INFO', 'ambos')
            cont_boss = cont_boss + 1
            confirm_action = True
            if st['boss_surrender'] != 0:
                if cont_boss == st['boss_surrender']:
                    dbg.console("Surrender boss: " + str(st['boss_surrender']), 'INFO', 'ambos')
                    time.sleep(3)
                    clickBtn(images['spg-surrender'])
                    time.sleep(1)
                    clickBtn(images['confirm-victory'], name='okVicBtn', timeout=2)
                    cont_boss = 1
            if st['key_waves'] == True:                   
                if cont_boss == st['numwavez1']:
                    time.sleep(5) 
                    dbg.console("Boss "+ str(st['numwavez1'])+", refresh ships", 'DEBUG', 'ambos')
                    clickBtn(images['ship'])
                if cont_boss == st['numwavez2']:
                    time.sleep(5) 
                    dbg.console("Boss "+ str(st['numwavez2'])+", refresh ships", 'DEBUG', 'ambos')
                    clickBtn(images['ship'])
                if cont_boss == st['numwavez3']:
                    time.sleep(5) 
                    dbg.console("Boss "+ str(st['numwavez3'])+", refresh ships", 'DEBUG', 'ambos')
                    clickBtn(images['ship'])
    return confirm_action

def removeSpaceships():
    time.sleep(2)   
    while True: 
        buttons = positions(images['spg-x'], threshold=th['hard'])
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
    global ships_clicks
    offset_x = 50
    offset_y = 30
    
    if st['send_ships_full'] == True:
        green_bars = positions(images['ship-full'], th['green_bar'])
        not_working_green_bars = []
        for bar in green_bars:
            not_working_green_bars.append(bar)
        for (x, y, w, h) in not_working_green_bars:
            moveToWithRandomness(x+offset_x+(w/2),y+offset_y+(h/2),1)
            pyautogui.click()
            ships_clicks = ships_clicks + 1        
            if ships_clicks >= st['qtd_send_spaceships']:
                dbg.console('Finish Click ships', 'INFO', 'ambos')
                return -1
        return len(green_bars)
    elif st['send_ships_full'] == False:
        buttons = positions(images['spg-go-fight'], th['go-fight'])
        for (x, y, w, h) in buttons:
            moveToWithRandomness(x+(w/2),y+(h/2),1)
            pyautogui.click()
            ships_clicks = ships_clicks + 1        
            if ships_clicks >= st['qtd_send_spaceships']:
                dbg.console('Finish Click ships', 'INFO', 'ambos')
                return -1
        return len(buttons)

def refreshPage():
    pass

def screen_close():
    global cont_boss
    confirm_click = False
    if clickBtn(images['close'],timeout=1):
        dbg.console('Encontrou close', 'ERROR', 'ambos')        
        cont_boss = 1
        confirm_click = True
    if clickBtn(images['bt-ok'], timeout=1):
        dbg.console('Encontrou ok', 'ERROR', 'ambos')        
        cont_boss = 1
        confirm_click = True
    return confirm_click

def reloadSpacheship():
    global cont_boss
    if len(positions(images['spg-base'], th['commom'])) > 0 and len(positions(images['fight-boss'], th['hard']))  > 0:
        clickBtn(images['spg-base'], name='closeBtn', timeout=1)
        time.sleep(3)
        clickBtn(images['ship'], name='closeBtn', timeout=1)
        time.sleep(3)        
        cont_boss = 1

def ships_15_15():
    start = time.time()
    has_timed_out = False
    while(not has_timed_out):
        matches = positions(images['15-15-ships'], th['15-15-ships'])

        if(len(matches)==0):
            has_timed_out = time.time()-start > 3
            continue
        dbg.console('Encontrou 15-15 tela naves', 'DEBUG', 'ambos')
        return True
    return False

def refreshSpaceships(qtd):
    global cont_boss
    global ships_clicks
    dbg.console('Refresh Spaceship to Fight', 'INFO', 'ambos')
    buttonsClicked = 1
    go_to_boss = False
    cda =  100
    aux_ships = 0
    
    empty_scrolls_attempts = st['qtd_send_spaceships']
    if ships_clicks > 0:
        dbg.console('Quantidade ja selecionada:' + str(ships_clicks), 'DEBUG', 'ambos')
        if ships_clicks == st['qtd_send_spaceships']:
            empty_scrolls_attempts = 0
            goToFight()
    while(empty_scrolls_attempts >0):        
        aux_ships = ships_clicks
        if ships_15_15():
            go_to_boss = True
            break
        buttonsClicked = clickButtonsFight()        
        if buttonsClicked == 0:
            empty_scrolls_attempts = empty_scrolls_attempts - 1
            scroll(-cda)
        elif buttonsClicked == -1:
            empty_scrolls_attempts = 0   
        else:
            if buttonsClicked > 0:
                empty_scrolls_attempts = empty_scrolls_attempts + 1
        
        time.sleep(2.1)
        if aux_ships != ships_clicks:
            dbg.console('Spaceships sent to Fight: ' + str(ships_clicks), 'INFO', 'ambos')

    if ships_clicks == st['qtd_send_spaceships'] or cont_boss > 1 or go_to_boss == True:
        empty_scrolls_attempts = 0
        goToFight()
    else:
        reloadSpacheship()

        
def goToFight():
    global ships_clicks
    global cont_boss
    ships_clicks = 0 
    clickBtn(images['fight-boss'])
    time.sleep(4)
    if clickBtn(images['confirm'], timeout = 4, threshold = th['commom']):
        cont_boss = 1

def endFight():
    global cont_boss    
    cont_boss = 1
    dbg.console("End fight", 'INFO', 'ambos')
    time.sleep(3) 
    returnBase()
    time.sleep(15) 
    if len(positions(images['spg-processing'], th['hard'])) > 0:
        time.sleep(40) 
    if len(positions(images['fight-boss'], th['hard']))  > 0:
        if st['remove_ships'] == True:
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

def zero_ships():
    if len(positions(images['spg-surrender'], th['commom'])  ) > 0:
        start = time.time()
        has_timed_out = False
        while(not has_timed_out):
            matches = positions(images['0-15'], th['0-15'])
            if(len(matches)==0):
                has_timed_out = time.time()-start > 3
                continue
            elif(len(matches)>0):
                clickBtn(images['ship'])
                return True
    return False                  

def main():
    global images    
    global login_attempts
    login_attempts = 0
    images = load_images()

    print(str_in)        
    time.sleep(5)
    dbg.console('Bot Iniciado. Versao: ' + str(VERSAO_SCRIPT), 'INFO', 'ambos')
    dbg.console('Qtd naves total: ' + str(st['empty_qtd_spaceships']), 'INFO', 'ambos')
    dbg.console('Qtd naves enviar: ' + str(st['qtd_send_spaceships']), 'INFO', 'ambos')

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
                if len(positions(images['fight-boss'], th['hard']))  > 0:
                    if st['remove_ships'] == True:
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