import time
import datetime
import threading
import logging

class Debug:
    def __init__(self, filename):
        self.filename = filename
        # Configuracao basica do logging
        logging.basicConfig(
        filename=self.filename,
        filemode='a+',
        level=logging.DEBUG,
        format='[%(asctime)s] [%(levelname)s] [%(threadName)-10s] %(message)s',
        datefmt='%Y-%b-%d %H:%M:%S'
        )
        
    def console(self, msg, level, destino):        
        hora_rede_local = time.strftime("%H:%M:%S", time.localtime())
        self.msg = msg
        self. level= level
        self.destino = destino
        if self.destino == 'monitor':
            print('[{} {}] [{}] {}'.format(datetime.date.today(), hora_rede_local, level, msg)) 
        elif self.destino == 'arquivo':
            if self.level == 'DEBUG':
                logging.debug(msg)
            elif self.level == 'INFO':
                logging.info(msg)
            elif self.level == 'WARNING':
                logging.warn(msg)
            elif self.level == 'ERROR':
                logging.error(msg)
            elif self.level == 'CRITICAL':
                logging.critical(msg)
        elif self.destino == 'ambos':    
            print('[{} {}] [{}] {}'.format(datetime.date.today(), hora_rede_local, level, msg)) 
            if self.level == 'DEBUG':
                logging.debug(msg)
            elif self.level == 'INFO':
                logging.info(msg)
            elif self.level == 'WARNING':
                logging.warn(msg)
            elif self.level == 'ERROR':
                logging.error(msg)
            elif self.level == 'CRITICAL':
                logging.critical(msg)