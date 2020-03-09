# coding: utf8

##Copyright (c) 2019 Лобов Евгений
## <ewhenel@gmail.com>
## <evgenel@yandex.ru>

## This file is part of LRScript_Detail.
##
##    JMScript_Detail is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    JMScript_Detail is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with LRScript_Detail.  If not, see <http://www.gnu.org/licenses/>.
##
##  (Этот файл — часть JMScript_Detail.)
##
##   JMScript_Detail - свободная программа: вы можете перераспространять ее и/или
##   изменять ее на условиях Стандартной общественной лицензии GNU в том виде,
##   в каком она была опубликована Фондом свободного программного обеспечения;
##   либо версии 3 лицензии, либо (по вашему выбору) любой более поздней
##   версии.
##
##   JMScript_Detail распространяется в надежде, что она будет полезной,
##   но БЕЗО ВСЯКИХ ГАРАНТИЙ; даже без неявной гарантии ТОВАРНОГО ВИДА
##   или ПРИГОДНОСТИ ДЛЯ ОПРЕДЕЛЕННЫХ ЦЕЛЕЙ. Подробнее см. в Стандартной
##   общественной лицензии GNU.
##
##   Вы должны были получить копию Стандартной общественной лицензии GNU
##   вместе с этой программой. Если это не так, см.
##   <http://www.gnu.org/licenses/>.)


import os
import sys
import functools
import logging
import traceback
from tkinter import tix as tk
import JMScript_Detail as jmscd
import exceptionHandler as excpt


def catch_except(func):
    @functools.wraps(func)
    def decorat_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except excpt.TkinterRuntimeExcept as tkexcpt:
            sys.excepthook(tkexcpt.__class__, tkexcpt, tkexcpt.__traceback__)
            return func(*args, **kwargs)
        except Exception as e:
            raise e
    return decorat_func

def class_meth_decor(cls):
    for attrName in dir(cls):
        attrValue = getattr(cls, attrName)
        if hasattr(attrValue, '__call__') and type(attrValue).__name__ == 'function':
            setattr(cls, attrName, catch_except(attrValue))
    return cls

@class_meth_decor
class JMScriptUsrApi(tk.Frame):

    def __init__(self, master=None):
        self.root = master
        self.root.title('JMProj_Detail')
        self.mFrame = tk.Frame
        self.mFrame = tk.Frame.__init__(self, self.root)
        self.currWidget = None
        self.jmscdObj = jmscd.JMScriptItems()
        self._currCyclIter_ = 0
        self._chkBtVar_ = tk.BooleanVar()
        self._chkBtVar_.set(False)
        self._incrOnGenVar_ = tk.BooleanVar()
        self._incrOnGenVar_.set(False)
        self._selctdItemsLst_ = []
        self._selctdKey_ = None
        self._txtBegin_ = 0.0
        self._txtEnd_ = tk.END
        #self.mFrame = tk.Frame
        #self.pack()
        #self.createWidgets()
        ###############
        self.xmlMsgLst = []

        self._varIfCutUrlInSmpl_ = tk.BooleanVar()
        self._varIfCutUrlInSmpl_.set(False)
        self._varRbSmplThruNum_ = tk.StringVar()
        self._varRbSmplThruNum_.set("Controller")
        self._varCbIfNotRstrUnqInSmpl_ = tk.BooleanVar()
        self._varCbIfNotRstrUnqInSmpl_.set(False)

        self._initText_ = """Перед работой с прилож.\n
		ознакомтесь с инструкцией.\n
		Еще какой-нибудь текст добавиться,\n
		далее будет видно."""
        self.excptHandl = excpt.ExceptHandler()
        tk.Tk.report_callback_exception = self.excptHandl.tkinter_callback_except
        self.logger = None
        self._loggerInit_()
        self._consHandlerInit_()
        self.excptHandl.logger = self.logger
        self._logOffset_ = 0

## Определение логгера
    def _loggerInit_(self):
        self.logger = logging.getLogger('jmscript.api')
        self.logger.setLevel(logging.INFO)

## Добавление хэндлера для вывода ошибок в консоль
    def _consHandlerInit_(self):
        self.logHandler = logging.StreamHandler()
        self.logHandler.setLevel(logging.ERROR)
        self.logFormat = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        self.logHandler.setFormatter(self.logFormat)
        self.logger.addHandler(self.logHandler)

    def activForm(self):
        #self.mFrame = tk.Frame(self, self)
        self._createWidgets_()
        self.logger.info("Widgets created")
        self.jmscdObj._logOffset_ = self._logOffset_
        #self.mFrame.pack()
        #self.createWidgets()

    def _createWidgets_(self):
        self.fsFrame = tk.Frame(self.mFrame)
        self.tk_setPalette(background = '#F2D7D5') ##F2D7D5
        self.btQuit = tk.Button(self.mFrame)
        self.btQuit.config(text = 'Завершить', command = self.root.destroy)
        self.btQuit.pack(side =tk.BOTTOM)
        ##self.loadFrame = tk.LabelFrame(self.fsFrame)
        ##self.listBMsg = tk.Listbox(self.loadFrame, relief='flat')

        self.topElemsFrame = tk.Frame(self.fsFrame)
        self.btnLstFrame = tk.LabelFrame(self.topElemsFrame)
        self.smplUnqOptFrame = tk.Frame(self.topElemsFrame)
        
        self.smplUnqOptLabelF = tk.LabelFrame(self.smplUnqOptFrame)
        
        self._lbSmplUnqOptLabelF_ = self.getSubWgts(self.smplUnqOptLabelF, tk._dummyLabel)
        self._lbSmplUnqOptLabelF_.config(text = "Уник. сэмпл.")
        self._frSmplUnqOptLabelF_ = self.getSubWgts(self.smplUnqOptLabelF, tk._dummyFrame)
        
        self.cbIfCutUrl = tk.Checkbutton(self._frSmplUnqOptLabelF_, text = "Сократ. Url в назв. сэмпл.", variable = self._varIfCutUrlInSmpl_)
        
        self.smplThruNum = tk.LabelFrame(self._frSmplUnqOptLabelF_)
        self._lbSmplThruNum_ = self.getSubWgts(self.smplThruNum, tk._dummyLabel)
        self._lbSmplThruNum_.config(text = "Скозн. нумер.")
        self._frSmplThruNum_ = self.getSubWgts(self.smplThruNum, tk._dummyFrame)
        self.smplThruNumCntrl = tk.Radiobutton(self._frSmplThruNum_, text = "Контроллер", variable = self._varRbSmplThruNum_, value = "Controller")
        self.smplThruNumThGr = tk.Radiobutton(self._frSmplThruNum_, text = "ТредГрупп", variable = self._varRbSmplThruNum_, value = "ThreadGroup")
        self.smplThruNumTstPl = tk.Radiobutton(self._frSmplThruNum_, text = "ТестПлан", variable = self._varRbSmplThruNum_, value = "TestPlan")
        self.smplThruNumCntrl.pack(side = tk.TOP, anchor = tk.W)
        self.smplThruNumThGr.pack(side = tk.TOP, anchor = tk.W)
        self.smplThruNumTstPl.pack(side = tk.TOP, anchor = tk.W)
        
        self.cbIfNotRstrUnqInSmpl = tk.Checkbutton(self._frSmplUnqOptLabelF_, text = "Не восст. ориг. назв. сэмпл.", variable = self._varCbIfNotRstrUnqInSmpl_)
        
        self.cbIfCutUrl.pack(side = tk.TOP, anchor = tk.W)
        self.smplThruNum.pack(side = tk.TOP, anchor = tk.W)
        self.cbIfNotRstrUnqInSmpl.pack(side = tk.TOP, anchor = tk.W)
        
        self.smplUnqOptLabelF.pack(anchor = tk.E)
        self.smplUnqOptFrame.config(width = self.smplThruNum.winfo_reqwidth(), padx = 100)
        
        self.emptyFrameTemp = tk.Frame(self.topElemsFrame)
        self.update_idletasks()
        leftCornerWidth = self._frSmplUnqOptLabelF_.winfo_reqwidth() + int(self.smplUnqOptLabelF.cget("borderwidth")) * 2
        leftCornerHeight = self.smplUnqOptLabelF.winfo_reqheight() + 2
        self.emptyFrameTemp.config(width = leftCornerWidth + 202, height = leftCornerHeight)
        self.emptyFrameTemp.pack_propagate(0)
        
        self.leftUpperFuncElemFrame = tk.LabelFrame(self.emptyFrameTemp)
        self._lbLeftUpperFuncElemFrame_ = self.getSubWgts(self.leftUpperFuncElemFrame, tk._dummyLabel)
        self._lbLeftUpperFuncElemFrame_.config(text = "Ифно")
        self._frLeftUpperFuncElemFrame_ = self.getSubWgts(self.leftUpperFuncElemFrame, tk._dummyFrame)
        tempText = """Некоторые замечания
по работе с приложением: 
1 - рекомендуется открыть 
в jmeter файл, сгенерированный 
после загрузки jmx-файла; 
2 - корректно выставлять 
настройки уникальн. сэмпл.; 
3 - внимательно прочитать 
файл README перед началом 
работы с приложением."""
        self.lbLeftUpperTextTemp = tk.Label(self._frLeftUpperFuncElemFrame_, text = tempText)
        self.lbLeftUpperTextTemp.pack(anchor = tk.W)
        self.leftUpperFuncElemFrame.pack(anchor = tk.W)		

        ##self.msgsToAscFrame = tk.Listbox(self.loadFrame, relief='flat', selectmode='multiple')
        ##self.vScroll = tk.Scrollbar(self.loadFrame, orient=tk.VERTICAL)
        ##self.msgsToAscFrame.config( yscrollcommand=self.vScroll.set)
        self.consFrame = tk.LabelFrame(self.mFrame)
        #self.varsFrame = tk.LabelFrame(self.fsFrame)

        ##self.btnCollctnFrame = tk.LabelFrame(self.fsFrame)
        
        self.mCllctnFrame = tk.Frame(self.mFrame)
        
        self._lbBtnLstFrame_ = self.getSubWgts(self.btnLstFrame, tk._dummyLabel)
        self._lbBtnLstFrame_.config(text = 'Раб. с исх. Xml-дер.')
        self._frBtnLstFrame_ = self.getSubWgts(self.btnLstFrame, tk._dummyFrame)
        
        self.varsFrame = tk.Frame(self._frBtnLstFrame_, borderwidth=2, bg = 'blue')
        self.vrSPathFrame = tk.Label(self.varsFrame)
        self.vrFnameFrame = tk.Label(self.varsFrame)
        self.vrUnqFNmFrame = tk.Label(self.varsFrame)
        #self.vrPileCllctnFrame = tk.Label(self.varsFrame)
        self.vrRestreFNmFrame = tk.Label(self.varsFrame)
        
        self._btnLstFrame_ = tk.Frame(self._frBtnLstFrame_, borderwidth = 2)
        
        self.btCatchJMXFiles = tk.Button(self._btnLstFrame_, text="Собрать все \n.jmx файлы", fg="green")
        
	#self.btCatchJMXFiles.config(command = self.testFrame)
        self.btCatchJMXFiles.config(command = self.prcdCatchJMXFiles)
        self.btCatchJMXFiles.config(relief='raised')
        self.btCatchJMXFiles.pack(fill = 'x')
        #self.jmscdObj.setFName = 'toParce.jmx'

        self.btGetJMXMkTree = tk.Button(self._btnLstFrame_, text="Получить дерево из \n.jmx файла", fg="green")
        self.btGetJMXMkTree.config(command = self.prcdGetJMXMkTree)
        self.btGetJMXMkTree.config(relief='raised')
        self.btGetJMXMkTree.pack(fill = 'x')
        
        self.btTreeUnqNms = tk.Button(self._btnLstFrame_, text="Сген. колл. \nс уник. именами")
        self.btTreeUnqNms.config(command = self.prcdTreeUnqNms)
        self.btTreeUnqNms.config(relief='raised', state = tk.DISABLED)
        self.btTreeUnqNms.pack(fill = 'x')
        
        self.btRstrOrigNms = tk.Button(self._btnLstFrame_, text="Восст. ориг. имена\nдля получен. колл.")
        self.btRstrOrigNms.config(command = self.prcdRstrOrigNms)
        self.btRstrOrigNms.config(relief='raised')
        self.btRstrOrigNms.pack(fill = 'x')
        
        self.vrSPathLabel = tk.Label(self.vrSPathFrame)
        self.vrSPathValue = tk.Entry(self.vrSPathFrame, bg='white')
        self.vrSPathLabel.config(text='Каталог с (*.jmx)  файл.:', justify = tk.LEFT)
        self.vrSPathValue.config(justify = tk.LEFT)
        self.vrSPathValue.insert(0, self.jmscdObj.setPATH)
        self.vrSPathLabel.pack(side = tk.LEFT)
        self.vrSPathValue.pack(side = tk.LEFT)
        self.vrSPathFrame.pack(side = tk.TOP)
        
        self.vrFnameLabel = tk.Label(self.vrFnameFrame)
        self.vrFnameValue = tk.Entry(self.vrFnameFrame, bg='white')
        self.vrFnameLabel.config(text='Файл (*.jmx) для парам.:', justify = tk.LEFT)
        self.vrFnameValue.config(justify = tk.LEFT)
        self.vrFnameValue.insert(0, self.jmscdObj.setFName)
        self.vrFnameLabel.pack(side = tk.LEFT)
        self.vrFnameValue.pack(side = tk.LEFT)
        self.vrFnameFrame.pack(side=tk.TOP)
        
        self.vrUnqFNmLabel = tk.Label(self.vrUnqFNmFrame)
        self.vrUnqFNmValue = tk.Entry(self.vrUnqFNmFrame, bg = 'white')
        self.vrUnqFNmLabel.config(text='Файл(*.jmx), униф. элм.:', justify = tk.LEFT)
        self.vrUnqFNmValue.config(justify = tk.LEFT)
        self.vrUnqFNmValue.insert(0, self.jmscdObj.outFileUniqueNames)
        self.vrUnqFNmLabel.pack(side = tk.LEFT)
        self.vrUnqFNmValue.pack(side = tk.LEFT)
        self.vrUnqFNmFrame.pack(side=tk.TOP)
        
        self.vrRestreFNmLabel = tk.Label(self.vrRestreFNmFrame)
        self.vrRestreFNmValue = tk.Entry(self.vrRestreFNmFrame, bg = 'white')
        self.vrRestreFNmLabel.config(text='Файл(*.jmx), восcт. элм.:', justify = tk.LEFT)
        self.vrRestreFNmValue.config(justify = tk.LEFT)
        self.vrRestreFNmValue.insert(0, self.jmscdObj.outFileRestrdOrig)
        self.vrRestreFNmLabel.pack(side = tk.LEFT)
        self.vrRestreFNmValue.pack(side = tk.LEFT)
        self.vrRestreFNmFrame.pack(side=tk.TOP)
        
        self._btnLstFrame_.pack(side = tk.TOP)
        self.varsFrame.pack(side=tk.TOP)
        ##
        
        
        self.frPileOptns = tk.LabelFrame(self.mCllctnFrame)
        self._lbFrPileOptns_ = self.getSubWgts(self.frPileOptns, tk._dummyLabel)
        self._lbFrPileOptns_.config(text = 'Получ. осн. колл.')
        self._frPileOptns_ = self.getSubWgts(self.frPileOptns, tk._dummyFrame)
        self.lsbxPileMCllct = tk.Listbox(self._frPileOptns_, height = 4, width = 34)
        for itm in range(4):
            self.lsbxPileMCllct.insert(tk.END, '--')
            
        self.btPileMCllct = tk.Button(self._frPileOptns_, text="Аккумул. раб. коллекц.")
        self.btPileMCllct.config(command = self.prcdPileMCllct, relief='raised')
        self.lsbxPileMCllct.pack(side = tk.TOP)
        self.btPileMCllct.pack(side = tk.TOP)
        self.frPileOptns.pack(side = tk.LEFT)
        
        self.frOutRslts = tk.LabelFrame(self.mCllctnFrame)
        self._lbFrOutRslts_ = self.getSubWgts(self.frOutRslts, tk._dummyLabel)
        self._lbFrOutRslts_.config(text = 'Текущ. знач.')
        self._frOutRslts_ = self.getSubWgts(self.frOutRslts, tk._dummyFrame)
        self.entStrVar = tk.StringVar(self._frOutRslts_)
        #self.entStrVar.set(self.jmscdObj.entityNames[2]) # default value
        self.lstWrkEnts = tk.OptionMenu(self._frOutRslts_, variable = self.entStrVar)
        for ent in self.jmscdObj.entityNames:
            self.lstWrkEnts.add_command(ent)
        self.entStrVar.set(self.jmscdObj.entityNames[2])
        #self.lstWrkEnts = tk.Listbox(self.mCllctnFrame)
        
        ##Опция выбора сущности на данный момент выключена
        ####self.lstWrkEnts.pack(side = tk.TOP)
        self.tstOutText = tk.Text(self._frOutRslts_, state = tk.DISABLED, bg='#FFEFD5')#, width=64)
        self.tstOutText.pack(side = tk.TOP)
        self.txtWdgtDelete(False)
        self.txtWdgtInsert(self._initText_)
        #
        self.frWrInfExtCntrlElm = tk.Frame(self._frOutRslts_)
        self.btWriteChngsToF = tk.Button(self.frWrInfExtCntrlElm, text='Запис. изм.\nв файл')
        self.btWriteChngsToF.config(command = self.prcdWrtXmlTree)
        self.btUpdateXMLTree = tk.Button(self.frWrInfExtCntrlElm, text='Обнов. \nxml-дерево')
        self.btUpdateXMLTree.config(command = self.prcdUpdtXMLTree, state = tk.DISABLED)
        self.btUpdateXMLTree.pack(side = tk.LEFT)
        self.btWriteChngsToF.pack(side = tk.LEFT)
        self.frWrInfExtCntrlElm.pack(side = tk.BOTTOM)
        #
        self.frOutRslts.pack(side = tk.LEFT)

        ###
        
        self.frGetCollctnData = tk.Frame(self.mCllctnFrame)
        #
        self.frGetListKeys = tk.LabelFrame(self.frGetCollctnData)
        self._frGetListKeys_ = self.getSubWgts(self.frGetListKeys, tk._dummyFrame)
        self.frBtGetLstKeys = tk.Frame(self._frGetListKeys_)
        self.btGetListKeys = tk.Button(self.frBtGetLstKeys, text="Список получ. ключей:")
        self.varRBtLstKeys = tk.IntVar()
        self.varRBtLstKeys.set(1)
        self.rBtLstKeysPrms = tk.Radiobutton(self.frBtGetLstKeys, text = 'Парам. ', variable = self.varRBtLstKeys, value = 1)
        self.rBtLstKeysLnks = tk.Radiobutton(self.frBtGetLstKeys, text = 'Ссылки', variable = self.varRBtLstKeys, value = 2)
        self.btGetListKeys.config(relief='groove')
        self.btGetListKeys.config(command = self.prcdfGetListKeys)
        self._lbGetListKeys_ = self.getSubWgts(self.frGetListKeys, tk._dummyLabel)
        self._lbGetListKeys_.config(text = 'Раб. с осн. коллекц.')
        self.frBtGetLstKeys.pack(side = tk.TOP, anchor = tk.W)
        self.btGetListKeys.pack(side = tk.LEFT)
        self.rBtLstKeysPrms.pack(side = tk.TOP, anchor = tk.E)
        self.rBtLstKeysLnks.pack(side = tk.TOP, anchor = tk.E)
        self.frGetListKeys.pack(side = tk.TOP, fill = 'x')
        #
        self.frGetDictData = tk.Frame(self._frGetListKeys_)
        self.frGetDictData.config(borderwidth = 2, bg = 'green')
        ##
        self.frGetDataDictItem = tk.Frame(self.frGetDictData)
        self.vlGetDataDictItem = tk.Entry(self.frGetDataDictItem, bg='white')
        self.vlGetDataDictItem.insert(0, '<знач.ключа>')
        self.btGetDataDictItem = tk.Button(self.frGetDataDictItem, text="Все знач.\nпо задан. ключу:")
        self.btGetDataDictItem.config(command = self.prcdGetDataDictItem)
        self.btGetDataDictItem.config(relief='groove')
        self.btGetDataDictItem.pack(side= tk.LEFT)
        self.vlGetDataDictItem.pack(side = tk.RIGHT, fill = 'y')
        self.frGetDataDictItem.pack(side = tk.TOP)
        ##
        self.frGetScrLstByNm = tk.Frame(self.frGetDictData)
        self.btGetScrLstByNm = tk.Button(self.frGetScrLstByNm, text="Все контрлр.\nпо задан. ключу:")
        self.btGetScrLstByNm.config(command = self.prcdGetScrLstByNm)
        self.btGetScrLstByNm.config(relief='groove')
        self.vlGetScrLstByNm = tk.Entry(self.frGetScrLstByNm, bg='white')
        self.vlGetScrLstByNm.insert(0, '<знач.ключа>')
        self.chkBtVar = tk.BooleanVar(self.frGetScrLstByNm)
        self.chkBtVar.set(False)
        self.chkGetScrLstByNm = tk.Checkbutton(self.frGetScrLstByNm, text='Вывод сэмплр.', variable=self.chkBtVar)
        self.btGetScrLstByNm.pack(side= tk.LEFT)
        self.vlGetScrLstByNm.pack(side = tk.TOP)
        self.chkGetScrLstByNm.pack(side = tk.LEFT)
        self.frGetScrLstByNm.pack(side = tk.TOP)
        ##
        self.frGetScrFncByKeyVal = tk.Frame(self.frGetDictData)
        self.btGetScrFncByKeyVal = tk.Button(self.frGetScrFncByKeyVal, text="Все контрлр.\nпо  паре  кл.-зн.:")
        self.btGetScrFncByKeyVal.config(command = self.prcdGetScrFncByKeyVal)
        self.btGetScrFncByKeyVal.config(relief='groove')
        self.vlGetScrFncByKeyVal = tk.Entry(self.frGetScrFncByKeyVal, bg='white')
        self.vlGetScrFncByKeyVal.insert(0, '<знач.ключа>')
        self.vrGetScrFncByKeyVal = tk.Entry(self.frGetScrFncByKeyVal, bg='white')
        self.vrGetScrFncByKeyVal.insert(0, '<знач.парам.>')
        self.chkKeyVlVar = tk.BooleanVar(self.frGetScrFncByKeyVal)
        self.chkKeyVlVar.set(False)
        self.chkGetScrFncByKeyVal = tk.Checkbutton(self.frGetScrFncByKeyVal, text='Вывод сэмплр.', variable=self.chkKeyVlVar)
        self.btGetScrFncByKeyVal.pack(side= tk.LEFT, fill='y')
        self.vlGetScrFncByKeyVal.pack(side = tk.TOP)
        self.vrGetScrFncByKeyVal.pack(side = tk.TOP)
        self.chkGetScrFncByKeyVal.pack(side = tk.LEFT)
        self.frGetScrFncByKeyVal.pack(side = tk.TOP, fill='x')
        ##
        self.frGetValByKSF = tk.Frame(self.frGetDictData)
        self.frGetValByKSF.config(borderwidth = 1, bg = 'red')
        self.blnMsg = tk.Balloon(self.frGetValByKSF, initwait = 350, bg='yellow')
        self.blnMsgText = 'Внимание!\nНазвания контроллеров и сэмплеров (возможно) были изменены,\nследует сверять в jmeter по файлу "(*.jmx) униф. эл"'
        self.blnMsg.bind_widget(self.frGetValByKSF, msg = self.blnMsgText)
        self.btGetValByKSF = tk.Button(self.frGetValByKSF, text="Значен. для\n кл.-кнтр.-смпл.:")
        self.btGetValByKSF.config(command = self.prcdGetValByKSF)
        self.btGetValByKSF.config(relief='groove')
        self.vlGetValByKSF = tk.Entry(self.frGetValByKSF, bg='white')
        self.vlGetValByKSF.insert(0, '<знач.ключа>')
        self.ctGetValByKSF = tk.Entry(self.frGetValByKSF, bg='white')
        self.ctGetValByKSF.insert(0, '<назв. контрлр.>')
        self.smGetValByKSF = tk.Entry(self.frGetValByKSF, bg='white')
        self.smGetValByKSF.insert(0, '<назв. сэмплр.>')
        self.btGetValByKSF.pack(side= tk.LEFT, fill='y')
        self.vlGetValByKSF.pack(side = tk.TOP)
        self.ctGetValByKSF.pack(side = tk.TOP)
        self.smGetValByKSF.pack(side = tk.TOP)
        self.frGetValByKSF.pack(side = tk.TOP, fill='x')
        ##
        self.frSetValsToSlctn = tk.Frame(self._frGetListKeys_, pady = 2)
        self.btSetValsToSlctn = tk.Button(self.frSetValsToSlctn, text = 'Установ.\n для дан.\n элемен.\n словар.')
        self.btSetValsToSlctn.config(command = self.prcdSetValsToSlctn, state = tk.DISABLED)
        self.lblSetValsToSlctn = tk.Label(self.frSetValsToSlctn, text = ' <==> ')
        self.entSetValsToSlctn = tk.Entry(self.frSetValsToSlctn, bg='white')
        self.entSetValsToSlctn.insert(0, '*новое знач.*')
        self.btSetValsToSlctn.pack(side = tk.LEFT, anchor=tk.W)
        self.lblSetValsToSlctn.pack(side = tk.LEFT)
        self.entSetValsToSlctn.pack(side = tk.RIGHT, anchor=tk.E)
        ###
        self.frGetDictData.pack(side = tk.TOP)
        self.frSetValsToSlctn.pack(side = tk.TOP, anchor = tk.W)
        #
        self.frGetCollctnData.pack(side = tk.LEFT)

        #for lstEntr in self.jmscdObj.entityNames:
        #    self.lstWrkEnts.insert(tk.END, lstEntr)
        
        self.fsFrame.pack(side="top", fill='x')
        self.mCllctnFrame.pack(side=tk.LEFT, fill='x')
        ##self.loadFrame.pack(side="top", fill='x')
        self.smplUnqOptFrame.pack(side = tk.RIGHT, anchor = tk.E)
        self.btnLstFrame.pack(side = tk.RIGHT)
        self.emptyFrameTemp.pack(side = tk.RIGHT)
        self.topElemsFrame.pack(side="top", fill='y')
        ##self.varsFrame.pack(side=tk.TOP)
        ##self.btnCollctnFrame.pack(side=tk.TOP)
        #self.inputFrame.pack(side="top")
        #self.actBtnFrame.pack(side="top")
        #self.consFrame.pack(side="top")
        #self.contrBtPane.pack(side="top")
        
    ##def testFrame(self):
        ##self.jmscdObj.catchJMXFilesInPath()
        ##print(self.jmscdObj.scrFlsLst)
        
    def getEntryText(self, entryNm):
        return entryNm.get()
        
    def prcdCatchJMXFiles(self):
        self.jmscdObj.setPATH = self.vrSPathValue.get()
        self.txtWdgtDelete(False)
        resJmxFls = self.jmscdObj.catchJMXFilesInPath()
        if resJmxFls == -1:
            self.txtWdgtInsert(self.jmscdObj._infoMsg_)
        else:
            for fl in range(len(self.jmscdObj.scrFlsLst)):
                self.tstOutText.tag_config("jmx_file_name"+str(fl))
                self.tstOutText.tag_bind("jmx_file_name"+str(fl), sequence="<Double-Button-1>", func=lambda evt, arg=self.jmscdObj.scrFlsLst[fl-1]: self.prcdFillvrFname(evt, arg))
                self.txtWdgtInsert(self.jmscdObj.scrFlsLst[fl-1] + '\n', "jmx_file_name"+str(fl))
	    
    def prcdFillvrFname(self, event, chTag):
        self.vrFnameValue.delete(0, tk.END)
        self.vrFnameValue.insert(0, chTag)
        
    def prcdGetJMXMkTree(self):
        self.jmscdObj.setFName = self.getEntryText(self.vrFnameValue)
        self.txtWdgtDelete(False)
        self.jmscdObj.getJMXFileAndMakeTree()
        self.btTreeUnqNms.config(state = tk.NORMAL)
        self.btUpdateXMLTree.config(state = tk.NORMAL)
        self.txtWdgtInsert(self.jmscdObj._infoMsg_)
        
    def prcdTreeUnqNms(self):
        self.jmscdObj.outFileUniqueNames = self.getEntryText(self.vrUnqFNmValue)
        self.txtWdgtDelete(False)
        self.jmscdObj._smplThruVar_ = self._varRbSmplThruNum_.get()
        self.jmscdObj.xmlTreeStructToUnqNams()
        ##
        self.lsbxPileMCllct.delete(0, tk.END)
        for itm in self.jmscdObj._thrGrpLst_:
            self.lsbxPileMCllct.insert(tk.END, itm[4])
        self.lsbxPileMCllct.selection_set(0,0)
        self.lsbxPileMCllct.activate(0)
        self.logger.info("List of ThreadGroup entries widget created")
        self.btTreeUnqNms.config(state = tk.DISABLED)
        self.txtWdgtInsert(self.jmscdObj._msgInfo_)
        
    def prcdRstrOrigNms(self):
        self.jmscdObj.outFileRestrdOrig = self.getEntryText(self.vrRestreFNmValue)
        self.jmscdObj.setFName = self.getEntryText(self.vrFnameValue)
        self.jmscdObj.restorOrigCntrlNm()
        self.txtWdgtDelete(True)
        self.txtWdgtInsert(self.jmscdObj._msgInfo_)
        
    def prcdPileMCllct(self):
        self.jmscdObj.setEntity(self.entStrVar.get())
        ##self.jmscdObj._currThrGrNam_ = self.lsbxPileMCllct.curselection()[0] + 1
        self.jmscdObj._currThrGrNam_ = self.jmscdObj._thrGrpLst_[self.lsbxPileMCllct.curselection()[0]][4]
        self.logger.info("ThreadGroup %s chosen", self.jmscdObj._currThrGrNam_)
        self.jmscdObj.extrHTTPDataNamesAndLinks()
        self.txtWdgtDelete(False)
        self.txtWdgtInsert(self.jmscdObj._msgInfo_)
        
    def prcdGetDataDictItem(self):
        self.jmscdObj.setEntity(self.entStrVar.get())
        if (self.ifChkLstRadio()):
            self.vlGetDataDictItem.delete(0, tk.END)
            entryDict = self.entryFillVal() 
            self.vlGetDataDictItem.insert(0, entryDict["key"])
        try:
            tmpVal = self.jmscdObj.getDataDictItem(self.vlGetDataDictItem.get())
            self.jmscdObj._selctdKey_ = self.vlGetDataDictItem.get()
            self.crtChkLstItms(tmpVal)
            self.btSetValsToSlctn.config(state = tk.NORMAL)
            del tmpVal
        except IndexError:
            self.crtChkLstItms(['Некорректное значение сущности'])
            self.btSetValsToSlctn.config(state = tk.DISABLED)
        
    def prcdGetScrLstByNm(self):
        self.jmscdObj.setEntity(self.entStrVar.get())
        if (self.ifChkLstRadio()):
            self.vlGetScrLstByNm.delete(0, tk.END)
            entryDict = self.entryFillVal()
            self.vlGetScrLstByNm.insert(0, entryDict["key"])
        try:
            tmpVal = self.jmscdObj.getScrListByKey(self.vlGetScrLstByNm.get(), funcFlag = self.chkBtVar.get())
            self.jmscdObj._selctdKey_ = self.vlGetScrLstByNm.get()
            self.crtChkLstItms(tmpVal, ifRadio = True)
            del tmpVal
        except IndexError:
            self.crtChkLstItms(['Некорректное значение сущности'])
        finally:
            self.btSetValsToSlctn.config(state = tk.DISABLED)
        
    def prcdGetScrFncByKeyVal(self):
        self.jmscdObj.setEntity(self.entStrVar.get())
        if (self.ifChkLstRadio()):
            self.vlGetScrFncByKeyVal.delete(0, tk.END)
            entryDict = self.entryFillVal()
            self.vlGetScrFncByKeyVal.insert(0, entryDict["key"])
        try:
            tmpTpl = (self.vlGetScrFncByKeyVal.get(), self.vrGetScrFncByKeyVal.get())
            tmpVal = self.jmscdObj.getScrFuncByKeyValue(tmpTpl, funcFlag = self.chkKeyVlVar.get())
            if len(tmpVal) == 0:
                raise excpt.CollectKeyValError
            self.jmscdObj._selctdKey_ = self.vlGetScrFncByKeyVal.get()
            self.crtChkLstItms(tmpVal, ifRadio = True)
            del tmpVal
            del tmpTpl
        except IndexError:
            self.crtChkLstItms(['Некорректное значение сущности'])
        except excpt.CollectKeyValError:
            self.crtChkLstItms(['Ничего не найдено\nс таким знач. парам.'])
        finally:
            self.btSetValsToSlctn.config(state = tk.DISABLED)
        
    def prcdGetValByKSF(self):
        self.jmscdObj.setEntity(self.entStrVar.get())
        if (self.ifChkLstRadio()):
            self.vlGetValByKSF.delete(0, tk.END)
            self.ctGetValByKSF.delete(0, tk.END)
            self.smGetValByKSF.delete(0, tk.END)
            entryDict = self.entryFillVal()
            self.vlGetValByKSF.insert(0, entryDict["key"])
            self.ctGetValByKSF.insert(0, entryDict["cntrl"])
            self.smGetValByKSF.insert(0, entryDict["smplr"])
        try:
            tmpTpl = (self.vlGetValByKSF.get(), self.ctGetValByKSF.get(), self.smGetValByKSF.get())
            tmpVal = self.jmscdObj.getValueByKeyScrFunc(tmpTpl)
            self.jmscdObj._selctdKey_ = self.vlGetValByKSF.get()
            self.crtChkLstItms([(self.ctGetValByKSF.get(), ((self.smGetValByKSF.get(), tmpVal),))])
            self.btSetValsToSlctn.config(state = tk.NORMAL)
            del tmpVal
            del tmpTpl
        except IndexError:
            self.crtChkLstItms(['Некорректное значение сущности,\nлибо в коллекции не найдено совпадений\nкл.-кнтр.-смпл.'])
            self.btSetValsToSlctn.config(state = tk.DISABLED)
        
    def testCmd(self):
        tmpChkLst = self.getSubWgts(self.dctItmsChkLst, tk._dummyHList)
        tmpVar = 'on'
        self.dctItmsChkLst.setstatus(tmpChkLst.info_children()[0], mode = 'on')
        if self.dctItmsVar.get() == False:
            tmpVar = 'off'
        for i in tmpChkLst.info_children():
            self.dctItmsChkLst.setstatus(i, mode = tmpVar)
        if (int(self.dctItmsChkLst.cget("radio")) != 0) and (tmpVar == 'on'):
            self.dctItmsChkLst.setstatus(tmpChkLst.info_children()[1], mode = 'on')
        del tmpVar

    def prcdfGetListKeys(self):
        self.jmscdObj.setEntity(self.entStrVar.get())
        self.tstOutText.delete(0.0, tk.END)
        self.btSetValsToSlctn.config(state = tk.DISABLED)
        if self.varRBtLstKeys.get() == 1:
            self.jmscdObj._selctdKey_ = 'Все парам.'
            self.crtChkLstItms(self.jmscdObj._curList_, ifRadio = True)
        elif self.varRBtLstKeys.get() == 2:
            self.jmscdObj._selctdKey_ = 'Все ссылки'
            self.crtChkLstItms(self.jmscdObj._curLinkList_, ifRadio = True)
        else:
            raise Exception           
            
    def prcdSetValsToSlctn(self):
        #tmpChkLst = self.getSubWgts(self.dctItmsChkLst, tk._dummyHList)
        if self.entSetValsToSlctn.get() == '*новое знач.*':
            newVal = 'set_to_none'
        elif self.entSetValsToSlctn.get() == None:
            newVal = 'set_to_none'
        elif self.entSetValsToSlctn.get() == '':
            newVal = 'set_to_none'
        elif self.entSetValsToSlctn.get() == 'Пустое значен.':
             newVal = ''
        else:
            newVal = self.entSetValsToSlctn.get()
        tmpChkLst = self.getChckLstSel()
        [self.jmscdObj.setValueByKeyScrFunc(newVal,(self.jmscdObj._selctdKey_,cntrl[0],prm[0])) for cntrl in tmpChkLst for prm in cntrl[1]]
        self._selctdItemsLst_.clear()
        self.jmscdObj._msgInfo_ = "Измен. добавлены в дерево,\nпосле обнов. будут видны\nпри работе с парам."
        self.txtWdgtDelete(True)
        self.txtWdgtInsert(self.jmscdObj._msgInfo_)
        del tmpChkLst
        
    def getSubWgts(self, widget, wgtClass):
        tmpLst = widget.subwidgets_all()
        for wdgt in tmpLst:
            if isinstance(wdgt, wgtClass):
                return wdgt
        return None
        
    def crtChkLstItms(self, itmCllctn, ifRadio = False):
        self.txtWdgtDelete(False)
        self._selctdItemsLst_.clear()
        [wdg.destroy() for wdg in self.frOutRslts.subwidgets_all() if (isinstance(wdg, tk.CheckList))]
            #self.dctItmsChkLst.destroy()
        
        ## Список чекбоксов для вывода в текстовом окне
        self.dctItmsChkLst = tk.CheckList(self.frOutRslts, radio = ifRadio)
        ##
        self.jmscdObj.setEntity(self.entStrVar.get())
        indx = 1.0
        ##
        self.dctItmsVar = tk.BooleanVar()
        self.dctItmsVar.set(not ifRadio)
        tmpChkLst = self.getSubWgts(self.dctItmsChkLst, tk._dummyHList)
        if (self.jmscdObj.platf.startswith('linux')):
            widthFrInSymb = int(self.tstOutText.winfo_width() / 7 - 3)
        elif (self.jmscdObj.platf.startswith('win')):
            widthFrInSymb = int(self.tstOutText.winfo_width() / 6 - 4)
        else:
            widthFrInSymb = int(self.tstOutText.winfo_width() / 7 - 3)
        heightTstInSymb = int(round(self.tstOutText.cget("height") / 2, 0))
        tmpChkLst.config(header = True, width = widthFrInSymb, height = heightTstInSymb, borderwidth=1)
        tmpChkLst.header_create(col = 0, itemtype = tk.TEXT, text = self.jmscdObj._selctdKey_)
        self.chkBtnTst = tk.Checkbutton(tmpChkLst, command = self.testCmd, variable = self.dctItmsVar)
        self.chkBtnTst.config(text = "Авто выбор/Все знач.")
        tmpChkLst.add('dctItm_0', itemtype = tk.WINDOW, window = self.chkBtnTst)
        entrCnt = 0
        for lnNum in range(len(itmCllctn)):
            for entr in itmCllctn[lnNum][1]:
                entrCnt += 1
                indx = '%d.%d' % (entrCnt, 0)
                curEntr = '%s_%s' % ('dctItm', str(entrCnt))
                entrTxt = (itmCllctn[lnNum][0] + ': ' + str(entr)) if isinstance(itmCllctn[lnNum], tuple) else itmCllctn[lnNum]
                entrVal = (itmCllctn[lnNum][0], ((entr),)) if isinstance(itmCllctn[lnNum], tuple) else itmCllctn[lnNum]
                self._selctdItemsLst_.append((curEntr, entrVal))
                exec('tmpChkLst.add(eval("curEntr"), itemtype = tk.IMAGETEXT, data = curEntr, text = entrTxt)')
        self.tstOutText.window_create(tk.END, window = self.dctItmsChkLst, align = tk.TOP)
        tmpIfMode = 'off' if (ifRadio) else 'on'
        for i in tmpChkLst.info_children():
            self.dctItmsChkLst.setstatus(i, mode=tmpIfMode)
        self.tstOutText.config(state = tk.DISABLED)
        del tmpChkLst
        del tmpIfMode
        self.logger.info("Checklist of dictionary entries created in Text Widget")
        
    def prcdUpdtXMLTree(self):
        self.jmscdObj.updateXMLTree()
        #self.jmscdObj._linksToUpdate_ = ()
        #self.btUpdateXMLTree.config(state = tk.DISABLED)
        self.txtWdgtDelete(True)
        self.txtWdgtInsert(self.jmscdObj._msgInfo_)
        
    def prcdWrtXmlTree(self):
        self.jmscdObj.outFileUniqueNames = self.vrUnqFNmValue.get()
        self.jmscdObj.wrtTreeToFile()
        self.txtWdgtDelete(True)
        self.txtWdgtInsert(self.jmscdObj._msgInfo_)

    def txtWdgtInsert(self, text, *tags):
        self._txtBegin_ = 0.0
        self.tstOutText.config(state = tk.NORMAL)
        self.tstOutText.insert(self._txtEnd_, text, *tags)
        self.tstOutText.config(state = tk.DISABLED)

    def txtWdgtDelete(self, ifWndKeep = True):
        wndIsTxtLst = self.tstOutText.window_names()
        srchRes = self.tstOutText.search(pattern = r'[\w\s-]+', index = self._txtBegin_, stopindex = self._txtEnd_, regexp = True)
        if len(wndIsTxtLst) > 0 and ifWndKeep == True:
            self._txtBegin_ = srchRes
        self.tstOutText.config(state = tk.NORMAL)
        self.tstOutText.delete(self._txtBegin_, self._txtEnd_)
        self.tstOutText.config(state = tk.DISABLED)

    def ifChkLstRadio(self):
        tmpChkLst = self.getSubWgts(self.dctItmsChkLst, tk._dummyHList)
        if (int(self.dctItmsChkLst.cget("radio")) != 0) and (self.dctItmsVar.get()):
            return True
        else:
            return False

    def getChckLstSel(self):
        return [lstItm[1] for lstItm in self._selctdItemsLst_ if self.dctItmsChkLst.getselection().count(lstItm[0]) != 0]

    def entryFillVal(self):
        fillVals = {"key": None, "cntrl": "<назв. контрлр.>","smplr":"<назв. сэмплр.>"}
        slctdVal = [lstItm[1] for lstItm in self._selctdItemsLst_ if self.dctItmsChkLst.getselection().count(lstItm[0]) != 0].pop(0)
        if self.jmscdObj._selctdKey_ in ("Все парам.", "Все ссылки"):
            fillVals["key"] = slctdVal
        else:
            fillVals["key"] = self.jmscdObj._selctdKey_
            fillVals["cntrl"] = slctdVal
            if isinstance(slctdVal, tuple):
                fillVals["cntrl"] = slctdVal[0]
                fillVals["smplr"] = slctdVal[1][0]
        return fillVals