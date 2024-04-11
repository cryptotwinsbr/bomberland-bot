# -*- coding: utf-8 -*-    
import pyautogui
import sys
import time
from debug import Debug
import yaml
from modules.config import Config
from modules.bombScreen import BombScreen
from modules.managerBomb import create_bombcrypto_managers
from modules.imageBomb import ImageBomb

VERSAO_SCRIPT = "2.00"
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
    +++++++++++ BCOIN BOMB SEN BUSD BNB +++++++++++
    + 0x73933b679F940ea7352c3895852501e3044FE855 ++
    ++++++++++++++++ Pix key ++++++++++++++++++++++
    ++++ 5f3d220c-a2a3-4db2-bfb2-30ae0533e240 +++++

    * Algumas configurações podem ser alteradas em 
    bomb_settings.yaml

    >> Ctrl + c finaliza o bot.
    
    
    """

def main():
    try:
        print(str_in)        
        time.sleep(5)
        dbg.console('Bot Iniciado. Versao: ' + str(VERSAO_SCRIPT), 'INFO', 'ambos', 'ALL')

        config_file = "bomb_settings.yaml"
        Config.load_config(config_file)
        ImageBomb.load_targets()
        bomb_crypto_managers = create_bombcrypto_managers()
        dbg.console("Contas BombCryto encontradas: " + str(len(bomb_crypto_managers)), 'INFO', 'ambos', 'BOMB')
        bomb_browser_count = 1
        show_initial = True

        while True:
            try:
                for manager in bomb_crypto_managers:
                    current_screen = BombScreen.get_current_screen()
                    
                    if show_initial:
                        dbg.console("Tela BombCrypto: " + str(bomb_browser_count), "INFO", "ambos", "BOMB:" + str(bomb_browser_count))
                    
                    with manager:
                        manager.do_what_needs_to_be_done(current_screen, bomb_browser_count)
                    
                    if bomb_browser_count == len(bomb_crypto_managers):
                        bomb_browser_count = 1
                        show_initial = False
                    else:
                        bomb_browser_count += 1
            except Exception as e:
                dbg.console("Except bombcrypto: " + str(e), "WARNING", "ambos", 'BOMB')      
        time.sleep(5)
    except Exception as e:
        dbg.console("Erro ao iniciar o bot. Erro: " + str(e), "ERROR", "ambos", 'ALL')

if __name__ == '__main__':
    main()