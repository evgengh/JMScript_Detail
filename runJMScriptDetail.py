from tkinter import tix as tk
import JMScript_Api as jmsca
import logging
import os
import sys

logger = None
offset = 0

def _checkLogFile_():
    fLog = open('jmscript.log', '+a')
    fLog.close()

def _getOffset_():
    return os.stat('jmscript.log').st_size

def _initLogger_():
    logger = logging.getLogger('jmscript')
    logger.setLevel(logging.INFO)
    logHandler = logging.FileHandler('jmscript.log')
    logHandler.setLevel(logging.INFO)
    logFormat = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
    logHandler.setFormatter(logFormat)
    logger.addHandler(logHandler)
    return logger

_checkLogFile_()
offset = _getOffset_()
logger = _initLogger_()
logger.info("JMSrcipt started")

root = tk.Tk()
app = jmsca.JMScriptUsrApi(master=root)
app._logOffset_ = offset
app.activForm()
app.mainloop()