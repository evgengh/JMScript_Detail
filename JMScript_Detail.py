<<<<<<< HEAD
# coding: utf8

##Copyright (c) 2020 Лобов Евгений
## <ewhenel@gmail.com>
## <evgenel@yandex.ru>

## This file is part of JMScript_Detail.
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
##    along with JMScript_Detail.  If not, see <http://www.gnu.org/licenses/>.
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
import re
import sys
import math
import urllib
import datetime
import pickle
import logging
import functools
import xml.etree.ElementTree as ET
import urllib.parse as urlpars
import exceptionHandler as excpt

class JMScriptItems:

    """Get details from scripts"""

## Инициализация при создании объекта

    def __init__(self):
        self.setPATH = "/home/pi/Документы/jmProj/wrk_dir"                   # Рабочая директория
        self.setDirMASK = '^uc[_0-9]+'                      # Маска для фильтра скриптов
        self.setPrefTrailInUniqNames = {"pref": '~', "trail": "#"} # Задаем символы префикса начала и разделителя перед номер для уник. имен
        
        self.setFName = 'example.jmx'                       # Название .jmx файла, должно присутствовать в каталоге self.scrFlsLst  
        
        self.setClassDir = os.getcwd()                      # Путь к директории с данным классом
        
        self._currDate_ = datetime.datetime.today()         # Текущая дата
        self._xmlTree_ = None                               # Полученное xml-дерево из файла скрипта JMeter
        self._xTreeRoot_ = {"elem": None, "hashTree": None} # Корневой элемент xml-дерева
        self._xTreeLocalRoot_ = {"elem": None, "hashTree": None} # Локальный корневой элемент xml-дерева, например для итериций внутри одной ThreadGroup
        self._thrGrpLst_ = []                               # Список ThreadGroup с названиями
        self._currThrGrNam_ = None                          # Имя выбранной ThreadGroup
        self._currBkpCntrLst_ = []                          # Список с указанием ориг. и изменных названий для дампа и восстановления названий нодов
        self._currDumpFName_ = None                         # Название файла для текущей коллекции
        self._currDumpDir_ = None                           # Название папки дампа сессии
        self.outFileUniqueNames = 'outputUnq.jmx'           # Файл для сохранения xml-дерева с уникальными названиями нодов (внутри ThreadGroup)
        self.outFileRestrdOrig = 'restoredOrig.jmx'         # Файл для восстановления xml-дерева с уникальными названиями нодов (внутри ThreadGroup)
        self._xPathUsrParam_ = []                           # ??Список пользовательских параметров для формирования xPath
        self._currNode_ = {"elem": None, "hashTree": None}  # Текущий нод
        self._ancstNode_ = {"elem": None, "hashTree": None} # Нод предка
        self._ancstNdClass_ = None                          # Класс нода предка
        
        self._curEntity_ = ''                               # Текущая заданная сущность (рабочая)
        self._curDict_ = {}                                 # Текущий заданый словарь (рабочий)
        self._curList_ = []                                 # Текущий заданый список ключей (рабочий)
        self._curLinkList_ = []                             # Текущий заданый список ссылок (рабочий)
        self._curLinkDict_ = {}                             # Текущий заданый словарь ссылок (рабочий
        self.entityNames = ('webUrl_URL', 'webUrl_Ref', 'webSubmit_Item', 'webSubmit_Ref')    # Список возможных сущностей (расширяется, при добавлении соответствующих методов обработки)
        os.chdir(self.setPATH)
        self.scrFlsLst = []                                 # Список файлов .jmx в рабочей директории
        self.scrFldLst = []                                 # Список каталогов в рабочей директории (папок со скриптами)
        self.sbmNamesLst = []                               # Список ключей для значений параметров (ItemData) функции web_submit_data
        self.sbmDataDict = {}                               # Словарь данных для сущности 'webSubmit_Item'
        self.sbmActLinkList = []                            # Список ссылок в строке Action функции web_submit_data
        self.sbmActLinkDict = {}                            # Словарь ссылок в строке Action функции web_submit_data
        self.refSbmLinkList = []                            # Список ссылок в строке Referer функции web_submit_data
        self.refSbmLinkDict = {}                            # Словарь ссылок в строке Referer функции web_submit_data
        self.refSbmNameList = []                            # Список ключей для ссылки в строке Referer функции web_submit_data
        self.refSbmDataDict = {}                            # Словарь данных для ссылки в строке Referer функции web_submit_data
        self.wbUrlParamLst = []                             # Список ключей для параметров в поле URL функции wer_url
        self.refWbNameLst = []                              # Список ключей для параметров в поле Referer функции web_url
        self.wbUrlDatalDict = {}                            # Словарь данных для сущности 'webUrl_URL'
        self.wbURLLinkList = []                             # Список ссылок без парам. в строке URL функции web_url
        self.wbURLLinkDict = {}                             # Словарь ссылок без парам. в строке URL функции web_url
        self.refWbDataDict = {}                             # Словарь данных для сущности 'webUrl_Ref'
        self.refWbLinkList = []                             # Список ссылок в строке Referer функции web_url
        self.refWbLinkDict = {}                             # Словарь ссылок в строке Referer функции web_url
        self._linksToUpdate_ = tuple()                      # Вспомогательный картеж для хранения изменений перед обновлением файлов
        self._selctdKey_ = None                             # Текущий выбраный ключ
        self._dctSmplThru_ = {}                             # Словарь оригинальных названий при режиме сквозной нумерации
        self._smplThruVar_ = "Controller"                   # Переменная сквозной нумерации
        self._ifNotRestoreSamplrs_ = False                  # Переменная восстановления оригинальных названий сэмплеров
        self._ifCutUrlInSmpl_ = False                       # Переменная, включающая признак усечения названий сэмплеров
        self.calcDictRes = {}                               # Словарь волатильности параметров
        self._ifVolatileParam_ = False                      # Переменная признака волатильности 

        #self._checkDmpDirExst_()                           # Проверка, что общий каталог для дампов существует
        self.excptHandl = excpt.ExceptHandler()             # Создание объекта класса ExceptHandler
        self.logger = None                                  # Логгер 
        self._logOffset_ = 0                                # Текущая позиция в файле лога приложения
        self._loggerInit_()                                 # Инициализация логгера
        self._consHandlerInit_()                            # Инициализация хэндлера для ошибок в консоле
        self.excptHandl.logger = self.logger                # Назначение логгера в классе exceptionHandler

        self.logger.info("JMScript_Detail object created")

        self._infoMsg_ = 'JMScript_Detail (c)'              # Текущее сообщение для вывода пользователю
        self.platf = sys.platform                           # Платформа
        
        print("\n\n* * * * JMScript_Details (ver. 4) * * * *")
        print("\n  * * * Класс для сбора и классификации данных сэмплеров JMeter * * *")
        print("\n\n                   Copyright (c) 2020 Лобов Евгений                    \n\n")

## Декоратор для проверки валидности ключа
    def valid_key(meth):
        def wrapper(*args, **kwargs):
            if meth.__name__ == 'setValueByKeyScrFunc':
                if len(args[0].retEntityByVal(args[2][0])) == 0:
                    args[0]._infoMsg_ = "Не выбраны (отмечены) значения для изменения.\nТакже см. опцию Все знач."
                    raise excpt.NoKeyFoundInDict
                else:
                    ret = meth(*args)
            elif (isinstance(args[1], tuple)) and (meth.__name__ != 'setValueByKeyScrFunc'):
                if len(args[0].retEntityByVal(args[1][0])) == 0:
                    args[0]._infoMsg_ = "По ключу '" + args[1][0] + "' ничего не найдено.\nВозможно не отмечена опция Автовыбор"
                    raise excpt.NoKeyFoundInDict
                else:
                    ret = meth(*args, **kwargs)
            elif (isinstance(args[1], str)) and (meth.__name__ != 'setValueByKeyScrFunc'):
                if len(args[0].retEntityByVal(args[1])) == 0:
                    args[0]._infoMsg_ = "По ключу '" + args[1] + "' ничего не найдено.\nВозможно не отмечена опция Автовыбор"
                    raise excpt.NoKeyFoundInDict
                else:
                    ret = meth(*args, **kwargs)
            elif not (isinstance(args[1], str)) and not (isinstance(args[1], tuple)):
                args[0].logger.error("Unknown item '" + str(args) + "' passed to meth '" + meth.__name__ + "'") 
                raise excpt.UnknownStructItem
            else:
                pass
            return ret
        return wrapper
        
## Декоратор для проверки возвращаемого списка по переданным условиям
    def valid_request_params(meth):
        def wrapper(*args, **kwargs):
            res = meth(*args, **kwargs)
            if len(res) == 0:
                args[0]._infoMsg_ = "По заданным значениям '" + str(tuple(args[1])) + "'\nв коллекции ничего не найдено.\nПроверьте корректность значений\nи/или опцию Автовыбор"
                raise excpt.NoDataInDictsWithFilter
            else:
                return res
        return wrapper
		
## Необработанные исключения перенаправляются в логгер
    def _unhandledExcept_(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys._excepthook_(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("Exception", exc_info = (exc_type, exc_value, exc_traceback))

## Определение логгера
    def _loggerInit_(self):
        self.logger = logging.getLogger('jmscript.detail')
        self.logger.setLevel(logging.INFO)

## Добавление хэндлера для вывода ошибок в консоль
    def _consHandlerInit_(self):
        self.logHandler = logging.StreamHandler()
        self.logHandler.setLevel(logging.ERROR)
        self.logFormat = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        self.logHandler.setFormatter(self.logFormat)
        self.logger.addHandler(self.logHandler)

## Перемещение лога сессии работы с приложения в дамп-директорию
    def _moveLogToDmp_(self):
        self.logger.info("Run app log to be moved to " + self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/jmscript_detail.log')
        fAppLog = open(self.setClassDir + '/jmscript.log', '+r')
        fAppLog.seek(self._logOffset_)
        buffAppLog = fAppLog.read()
        fAppLog.close()
        fDetLog = open(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/jmscript_detail.log', '+w')
        fDetLog.write(buffAppLog)
        fDetLog.close()
        logger = self.logger.manager.loggerDict['jmscript']
        handler = self.logger.manager.loggerDict['jmscript'].handlers[0]
        logger.removeHandler(handler)
        logHandler = logging.FileHandler(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/jmscript_detail.log')
        logHandler.setLevel(logging.INFO)
        logFormat = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        logHandler.setFormatter(logFormat)
        logger.addHandler(logHandler)
        del buffAppLog

## Проверка что существует директория для дампов
    def _checkDmpDirExst_(self):
        tmpDmpDirLst = [dir for dir in os.listdir(self.setPATH) if dir == 'jmProj_dumps']
        if len(tmpDmpDirLst) == 0:
            self.logger.info("Dump directory doesn't exist, will be created")
            os.mkdir('jmProj_dumps')
        del tmpDmpDirLst
 
## Вспомогательный метод для добавления изменненого значения словаря во временное структуру '_linksToUpdate_'

    def _storeLinkFromSet_(self, *lnks):
        tmpLst = [h for h in lnks[0]]
        tmpLst.append(self.getEntity())
        lnk_to_stre = tuple(tmpLst)
        tmpLst = [a for a in self._linksToUpdate_]
        tmpLst.append(lnk_to_stre)
        self._linksToUpdate_ = tuple(tmpLst)
        del tmpLst

## Метод загрузки .jmx-файла и создания xml-дерева

    def getJMXFileAndMakeTree(self, fName = True):
        xSet = self._pumpUpXPathToBuild_('rootElemHashTree')
        tmpFlLst = []
        ifFExst = bool(len([f for f in self.scrFlsLst if f == self.setFName]) == 1)
        if (ifFExst):
            self._checkDmpDirExst_()
            self._xmlTree_ = ET.parse(self.setFName)
            self._xTreeRoot_["elem"] = self._xmlTree_.getroot().find(xSet[0])
            self._xTreeRoot_["hashTree"] = self._xmlTree_.getroot().find(xSet[1])
            self.logger.info("JMX-file parsed and loaded, xml-tree created")
            self._infoMsg_ = "Загружен файл " + self.setFName
            if (self._ifCutUrlInSmpl_):
                self.truncSmplrName()
        else:
            self.logger.info("Can't load jmx-file")
            self._infoMsg_ = "Такой *.jmx файл не найден"

## Метод извлечения названий каталогов в директории setPATH

    def catchJMXFilesInPath(self):
        tmpLst = []
        try:
            os.chdir(self.setPATH)
        except FileNotFoundError:
            self._infoMsg_ = "Директория не найдена"
            return -1
        self.scrFlsLst = os.listdir('.')
        tmpLst = [f for f in self.scrFlsLst if f[len(f)-4:].find(".jmx")!=-1]
        self.scrFlsLst = tmpLst
        if len(self.scrFlsLst) == 0:
            self._infoMsg_ = "Тут jmx-файлов не обнаружено"
            return -1
        del tmpLst
        return 0
        
## Метод получения струткуры нодов элементов класса Контроллер (точнее типа, Контроллеры различаются),
## а также генерация аналогичной с уникальными идентификаторами (Name).
## После окончания работы с основными (не вспомогательными) коллекциями 
## все ориг. названия можно восстановить из файлов дампа

    def xmlTreeStructToUnqNams(self):
        xSet = self._pumpUpXPathToBuild_('TestPlan')
        if self._getNodeClass_(self._xTreeRoot_["elem"]) != "TestPlan":
            logger.error("Wrong root element, class of _xTreeRoot_ is " + self._getNodeClass_(self._xTreeRoot_["elem"]))
            self._infoMsg_ = "Некорректное знач. корня дерева,\n см. лог"
        else:
            self._sessDmpDir_()
            self._extrThreadGroupNode_()
            self._extrCntrllNode_()
            self._dctSmplThru_ = {}
            self._currBkpCntrLst_ = self._thrGrpLst_.copy()
            self._currDumpFName_ = 'pcklUnqNm_TstPl-' + self._getNodeName_(self._xTreeRoot_["elem"]).replace(' ', '%') 
            self._dumpOrigCntrlNm_()
            self.xmlTreeToFile(True, "Нужно сгенерировать осн. коллекц.\nдля ThreadGroup")

## Метод задания локального root элемента

    def _setLocalRootNode_(self, node):
        if node.tag != "hashTree":
            self._xTreeLocalRoot_["elem"] = node
            self._xTreeLocalRoot_["hashTree"] = self._getNodeElemHashTree_(node)
        
## Метод извлечения Нодов для всех элементов ThreadGroup
    
    def _extrThreadGroupNode_(self):
        self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
        xSet = self._pumpUpXPathToBuild_('ThreadGroups')
        tmpNodeLst = self._xTreeLocalRoot_["hashTree"].findall(xSet[0])
        self._currBkpCntrLst_.clear()
        tmpThGrLst = tmpNodeLst.copy()
        self._xElmUniqueName_(tmpNodeLst, 'TestPlan')
        if len(self._currBkpCntrLst_) == 0:
            self._thrGrpLst_ = [tuple([thgr, '--', '--', '--', self._getNodeName_(thgr)]) for thgr in tmpThGrLst]
        else:
            self._thrGrpLst_ = self._currBkpCntrLst_.copy()
            self._thrGrpLst_.reverse()
        self.logger.info("All ThreadGroups in TestPlan extracted")
        del tmpNodeLst
        del tmpThGrLst
        
## Метод, который будет использоваться вместо _checkIfxElmIsCntrll_
## достаточно вызова с параметром имени класса для проверки

    def _checkElmTypeClls_(self, node, ndClass=None):
        fndClss = self._getNodeClass_(node)
        return bool(fndClss.find(ndClass)!=-1)

## Метод извлечения Нодов для всех элементов класса Controller для каждого элемента ThreadGroup

    def _extrCntrllNode_(self, cntrlLst = None, thgrName = None, nodeClass = "Controller"):
        tmpLst = []
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        if nodeClass == "Controller":
            tmpLst = [[itm for itm in self._getNodeElemHashTree_(thgr[0]).findall(xSet[0]) if (self._checkElmTypeClls_(itm, "Controller"))] for thgr in self._thrGrpLst_]
            if self._smplThruVar_ == "TestPlan":
                smplrLst = [itm for itm in self._xTreeRoot_["hashTree"].findall(xSet[0]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))]
                self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
                self._xElmUniqueName_(smplrLst, "TestPlan", smplrsThru = True)
                del smplrLst
        elif nodeClass == "Sampler":
            tmpLst = [[itm for itm in self._getNodeElemHashTree_(cntrl).findall(xSet[1]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))] for cntrl in cntrlLst]
        else:
            raise Exception
        for itmLst in tmpLst:
            self._currBkpCntrLst_.clear()
            if nodeClass == "Controller":
                itmLstCpy = itmLst.copy()
                self._setLocalRootNode_(self._thrGrpLst_[tmpLst.index(itmLst)][0])
                self._xElmNestedMapp_(itmLst, 'ThreadGroup')
                self._xElmUniqueName_(itmLst, 'ThreadGroup')
                self._currDumpFName_ = 'pcklUnqNm_ThGr-' + self._getNodeName_(self._xTreeLocalRoot_["elem"]).replace(" ", "%")
                self.logger.info("Nodes from ThreadGroup %s exctracted", self._getNodeName_(self._xTreeLocalRoot_["elem"]))
                if self._smplThruVar_ == "ThreadGroup":
                    smplrLst = [itm for itm in self._xTreeLocalRoot_["hashTree"].findall(xSet[0]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))]
                    self._xElmUniqueName_(smplrLst, "ThreadGroup", smplrsThru = True)
                    del smplrLst
                self._dumpOrigCntrlNm_()
                self._extrCntrllNode_(itmLstCpy, self._getNodeName_(self._xTreeLocalRoot_["elem"]), nodeClass = "Sampler")
            elif nodeClass == "Sampler":
                self._setLocalRootNode_(cntrlLst[tmpLst.index(itmLst)])
                cntrlClass = self._getNodeClass_(self._xTreeLocalRoot_["elem"])
                tmpThru = (self._smplThruVar_ in ("ThreadGroup", "TestPlan"))
                self._xElmUniqueName_(itmLst, cntrlClass, smplrsThru = tmpThru, thGrIfSmplr = thgrName)
                self._currDumpFName_ = 'pcklUnqNm_Cntrl-' + thgrName.replace(' ', '%') + '-' + self._getNodeName_(self._xTreeLocalRoot_["elem"]).replace(" ", "%")
                self.logger.info("Nodes from Controller %s exctracted", self._getNodeName_(self._xTreeLocalRoot_["elem"]))
                self._dumpOrigCntrlNm_()
                del tmpThru
            else:
                raise Exception
        del tmpLst
        self._currBkpCntrLst_.clear()

## Метод создание префиксов для структуры составных вложенных элементов (для идентификации в коллекции)
        
    def _xElmNestedMapp_(self, cntrLst, parntNdClass):
        tmpLst = []
        tmpVar = None
        tmpVarNew = None
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('nodeProps')
        for nd in cntrLst:
            tmpLst = [j for j in self._getNodeElemHashTree_(nd).findall(xSet[0]) if cntrLst[cntrLst.index(nd):].count(j)!=0]
            if len(tmpLst) != 0:
                for itm in tmpLst:
                    if (self._checkElmTypeClls_(itm, "Controller")):
                        prop = self._getNodeName_(itm)
                        newPropVal = self.setPrefTrailInUniqNames["pref"] + prop
                        self._setNodeName_(itm, newPropVal)
                        elmJmClass = self._getNodeClass_(itm)
                        self._extrParntNodes_(itm, parntNdClass)
                        prntNdName = self._getNodeName_(self._ancstNode_["elem"])
                        self._storeOrigXElm_(itm, prntNdName, elmJmClass, prop, newPropVal)
        del tmpLst
        del tmpVar
        del tmpVarNew

## Метод создание нумерации для структуры составных элементов (для идентификации в коллекции)

    def _xElmUniqueName_(self, revCntrLst, parntNdClass, smplrsThru = False, thGrIfSmplr = None):
        tmpVar = None
        tmpVarNode = None
        tmpVarNew = None
        bkpCntrLst = self._currBkpCntrLst_
        revCntrLst.reverse()
        tmpLst = [self._getNodeName_(pr) for pr in revCntrLst]
        tmpThGrIfSmplr = []
        tmpThGrIfSmplr.append(thGrIfSmplr)
        tmpThGrIfSmplr.append(None)
        tmpThGrIfSmplr = list(filter(lambda a: a != None, tmpThGrIfSmplr))
        while(len(tmpLst)!=0):
            itm = tmpLst[0]
            itmCnt = tmpLst.count(itm)
            if itmCnt == 1:
                if (smplrsThru) and (itm in self._dctSmplThru_.keys()):
                    elmJmClass = self._getNodeClass_(revCntrLst[0])
                    self._extrParntNodes_(revCntrLst[0], parntNdClass)
                    prntNdName = self._getNodeName_(self._ancstNode_["elem"])
                    self._storeOrigXElm_(revCntrLst[0], *tmpThGrIfSmplr, prntNdName, elmJmClass, self._dctSmplThru_[itm], itm)
                tmpLst.pop(0)
                revCntrLst.pop(0)
                continue
            while(itmCnt>0):
                itmIndx = tmpLst.index(itm)
                propName = self._getNodeName_(revCntrLst[itmIndx])
                propNameNew = propName +  self.setPrefTrailInUniqNames["trail"] + str(itmCnt)
                self._setNodeName_(revCntrLst[itmIndx], propNameNew)
                elmJmClass = self._getNodeClass_(revCntrLst[itmIndx])
                self._extrParntNodes_(revCntrLst[itmIndx], parntNdClass)
                prntNdName = self._getNodeName_(self._ancstNode_["elem"])
                if (smplrsThru):
                    self._dctSmplThru_[propNameNew] = propName
                else:
                    self._storeOrigXElm_(revCntrLst[itmIndx], *tmpThGrIfSmplr, prntNdName, elmJmClass, propName, propNameNew)
                tmpLst.pop(itmIndx)
                revCntrLst.pop(itmIndx)
                itmCnt = tmpLst.count(itm)
                del propName
                del propNameNew
        del tmpLst
        del tmpVarNode
        del tmpThGrIfSmplr
        ##bkpCntrLst.reverse()
        self._currBkpCntrLst_ = bkpCntrLst
        
## Метод получения родительских нодов 

    def _extrParntNodes_(self, node, upprNodeClass=None):
        ndName = self._getNodeName_(node)
        ndClass = self._getNodeClass_(node)
        self._xPathUsrParam_.append('')
        self._xPathUsrParam_.append(ndClass)
        self._xPathUsrParam_.append(ndName)
        self._xPathUsrParam_.append('')
        tmpLst = []
        tmpLst.append(self._pumpUpXPathToBuild_('anyNode'))
        tmpLst.append(self._pumpUpXPathToBuild_('nodesWithClass'))
        tmpLst.append(self._pumpUpXPathToBuild_('nodesWithName'))
        tmpLst.append(self._pumpUpXPathToBuild_('parntNode'))
        xSetStr = self._xPthBuild_(*tmpLst)
        parentHashTree = self._xTreeLocalRoot_["hashTree"].find(xSetStr)
        parentElemTag = self._getNodeElemTag_(parentHashTree)
        self._ancstNode_["elem"] = parentElemTag
        self._ancstNode_["hashTree"] = parentHashTree
        del tmpLst
        while((upprNodeClass!=None) and (upprNodeClass!=self._getNodeClass_(self._ancstNode_["elem"]))):
            self._extrParntNodes_(self._ancstNode_["elem"], upprNodeClass)
            
    def _getNodeElemTag_(self, hashTr):
        return self._getNodeElem_('hashTree', hashTr)
        
    def _getNodeElemHashTree_(self, nodeTag):
        return self._getNodeElem_('elem', nodeTag)
            
    @functools.lru_cache(maxsize = None)        
    def _getNodeElem_(self, itmType, item):
        xSet = self._pumpUpXPathToBuild_('all_hashTrees')
        xSet_1 = self._pumpUpXPathToBuild_('dirChldNode')
        xSet_2 = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        hostHashTr = None
        if item == self._xTreeRoot_[itmType]:
            hostHashTr = self._xmlTree_.getroot().find(xSet[1])
        else:
            hashTrLst = self._xTreeRoot_["hashTree"].findall(xSet[0])
            hashTrLst.insert(0, self._xTreeRoot_["hashTree"])
            shiftPos = 0
            tmpLst = []
            while (tmpLst.count(item) < 1):
                hostHashTr = hashTrLst[shiftPos]
                tmpLst = hostHashTr.findall(xSet[1]) if itmType == 'hashTree' else hostHashTr.findall(xSet_2[1])
                shiftPos += 1
                ###Needs to be debugged due to it seems there are xcesive calls when extr threadgroups
            del tmpLst
        tmpLstSiblElms = hostHashTr.findall(xSet_1[0])
        try:
            return tmpLstSiblElms[tmpLstSiblElms.index(item) - 1] if itmType == 'hashTree' else tmpLstSiblElms[tmpLstSiblElms.index(item) + 1]
        except:
            self.logger.error("Got error while retrieving item for " + itmType , str(sys.exc_info()[0]))
            return None
            
            
## Метод извлечения хостового нода для свойств и т.д.

    def _extrHostNode_(self, prop):
        self._xPathUsrParam_.append('')
        self._xPathUsrParam_.append(prop)
        xSetStr = self._xPthBuild_(self._pumpUpXPathToBuild_('anyNode'), self._pumpUpXPathToBuild_('nodesWithName'))
        tmpNode = self._xTreeLocalRoot_["hashTree"].find(xSetStr)
        tmpHashTree = self._getNodeElemHashTree_(tmpNode)
        self._currNode_["elem"] = tmpNode
        self._currNode_["hashTree"] = tmpHashTree
        del tmpNode
        del tmpHashTree

## Метод заполнения коллекции оригинальных элементов и их оригинальных названий

    def _storeOrigXElm_(self, *vals):
        if isinstance(vals[1], tuple):
            vals = tuple(vals[1])
        tmpLst = [itm[0] for itm in self._currBkpCntrLst_]
        tmpVar = (vals)
        if tmpLst.count(vals[0]) != 0:
            indx = tmpLst.index(vals[0])
            exstOrigName = [val for val in self._currBkpCntrLst_[indx]][len(self._currBkpCntrLst_[indx])-2]
            valsLst = [vl for vl in vals]
            valsLst[len(vals)-2] = exstOrigName
            tmpVar = valsLst
            self._currBkpCntrLst_[indx] = tuple(tmpVar)
        else: 
            self._currBkpCntrLst_.append(vals)
        del tmpLst
        del tmpVar
        
## Метод удаляет все ссылки (объекты) дерева из коллекции для бэкапа, остаются только текстовые параметры

    def _cutxElmPartInRestoCllctn_(self):
        tmpLst = [tuple([pars for pars in clItm[1:]]) for clItm in self._currBkpCntrLst_]
        self._currBkpCntrLst_ = tmpLst
        del tmpLst
        
## Метод дампа коллекции с ориг. и изменными названиями нодов в файл
        
    def _dumpOrigCntrlNm_(self):
        self._cutxElmPartInRestoCllctn_()
        try:
            with open(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/' + self._currDumpFName_ + '.txt', 'wb+') as fObj:
                self.logger.info("Dump file %s stored in dump directory", self._currDumpFName_)
                pickle.dump(self._currBkpCntrLst_, fObj)
            fObj.close()
            return False
        except:
            print('Ошибка при дампе коллекции: ' + str(sys.exc_info()[0]))
            return True

## Метод восстановления ориг. названий нодов из сохраненных в файлах коллекциях
        
    def restorOrigCntrlNm(self):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        tmpResLst = []
        self._extrThreadGroupNode_()
        self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
        smplrLst = [itm for itm in self._xTreeRoot_["hashTree"].findall(xSet[0]) if ((self._checkElmTypeClls_(itm, "Controller")) and (itm.tag != "elementProp"))]
        if not (self._ifNotRestoreSamplrs_):
            tmpResLst.append(self._restorOrigCntrlNm_(smplrLst, 'Cntrl'))
        tmpResLst.append(self._restorOrigCntrlNm_(self._thrGrpLst_, 'ThGr'))
        tmpResLst.append(self._restorOrigCntrlNm_([(self._xTreeRoot_["elem"], '--', '--', '--',self._getNodeName_(self._xTreeRoot_["elem"]).replace(' ', '%'))], 'TstPl'))
        if tmpResLst.count(-1) != 0:
            self._infoMsg_ = "Ошибка при восстановлении\nориг. назв. элем. дерева,\nнужно проверить дампы.\nСм. лог"
        else:
            msgText = "Файл с оригинальными(восстан.)\nназв. элементов дерева создан ---" + self.outFileRestrdOrig + "---"
            if (self._ifNotRestoreSamplrs_):
                msgText = msgText + "\n--------"
                msgText = msgText + "\nБез восст. оригинал. назв. сэмплеров\n(признак = True)."
            self.xmlTreeToFile(False, msgText)
        del smplrLst
        
## Вспомогательный метод для загрузки коллекций из файлов и восстановления

    def _restorOrigCntrlNm_(self, elmLst, fPstfx):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('prop_nodeName')
        tmpElmNm = None
        cntrlLst = []
        tmpFlLst = []
        flLst = []
        if fPstfx == "Cntrl":
            cntrlLst = [self._getNodeName_(itm) for itm in elmLst]
            os.chdir('jmProj_dumps/'+ self._currDumpDir_)
            tmpFlLst = os.listdir('.')
            tmpFlLst = [fl.split('-') for fl in tmpFlLst if fl.split('-')[0] == "pcklUnqNm_Cntrl"]
            for flItm in tmpFlLst:
                if cntrlLst.count(flItm[2][:len(flItm[2]) - 4].replace('%', ' ')) != 0:
                    flLst.append('-'.join(flItm))
                    cntrlLst.remove(flItm[2][:len(flItm[2]) - 4].replace('%', ' '))
            if len(cntrlLst) != 0:
                self.logger.error("Error while loading collection for controllers: " + str(', '.join(cntrlLst)))
                return -1
            os.chdir(self.setPATH)
        else:
            flLst = ['pcklUnqNm_' + fPstfx + '-' + fl[4].replace(' ', '%') + '.txt' for fl in elmLst]
        flLst.sort()
        for flNm in flLst:
            try:
                with open('jmProj_dumps/'+ self._currDumpDir_ + '/' + flNm, 'rb') as fObj:
                    cllctn = pickle.load(fObj)
                fObj.close()
            except:
                self.logger.error("Error while loading collection from a file (" + flNm + "): " + str(sys.exc_info()[0]))
                return -1
            if len(cllctn) == 0:
                continue
            if fPstfx == "Cntrl":
                self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
                self._extrHostNode_(cllctn[0][0])
                tmpUppElm = [cntrl for cntrl in self._currNode_["hashTree"].findall(xSet[0]) if self._getNodeName_(cntrl) == cllctn[0][1]].pop(0)
            else:
                tmpUppElm = [k[0] for k in elmLst if self._getNodeName_(k[0]) == cllctn[0][0]].pop(0)
            self._setLocalRootNode_(tmpUppElm)
            self._appendXElmToCllctnItm_(cllctn)
            self._constrictBkpCl_()
            self.logger.info("Collection succesfully restored from file " + flNm)
        del cntrlLst
        del tmpFlLst
        del flLst
        return 0
        
## Метод дополнения элементов загруженной из файла коллекции соответствующим элементом (объектом) дерева

    def _appendXElmToCllctnItm_(self, rstrCl):
        self._currBkpCntrLst_.clear()
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        tmpLst = []
        for itm in rstrCl:
            self._extrHostNode_(itm[len(rstrCl[0])-1])
            tmpLst = [atr for atr in itm]
            tmpLst.insert(0, self._currNode_["elem"])
            itm = tuple(tmpLst)
            self._storeOrigXElm_(self, itm)
        del tmpLst
        
    def _getCurrNode_(self):
        node = self._currNode_
        return node
        
    def _constrictBkpCl_(self):
        for elm in self._currBkpCntrLst_:
            elm[0].attrib["testname"] = elm[len(self._currBkpCntrLst_[0])-2]

## Метод дополнения файлов дампа текущей датой
## !!! нужно сделать проверку при запуске на присутствие файлов с постфиксом текущей даты и что с ними делать

    def _sessDmpDir_(self, elmPstfx = 'deflt'):
        dtPostFx = self.dtPrefWithZero(self._currDate_.day) + self.dtPrefWithZero(self._currDate_.month) + str(self._currDate_.year)
        dtExstFlLst = [fl for fl in os.listdir('jmProj_dumps') if fl.find('dump_' + self.setFName.rpartition('.')[0] + '_' + dtPostFx) != -1]
        if len(dtExstFlLst) == 0:
            dtExstFlLst.append('empty_elem_0')
        dtExstFlLst.sort(key = lambda flNum: int(flNum.rpartition('_')[2]))
        lastDtFlNum = int(dtExstFlLst[len(dtExstFlLst)-1].rpartition('_')[2])
        self._currDumpDir_ = 'dump_' + self.setFName.rpartition('.')[0] + '_' + dtPostFx + '_' + str(lastDtFlNum + 1)
        os.mkdir('jmProj_dumps/' + self._currDumpDir_)
        self.logger.info("Working directory " + self.setPATH + "/jmProj_dumps/" + self._currDumpDir_ + " created")
        self._moveLogToDmp_()

## Метод добавляет нули, если месяц или число возвращаются одним символом (1, 4 и т.д.)

    def dtPrefWithZero(self, num):
        if len(str(num)) == 1:
            return '0' + str(num)
        return str(num)

		
## Метод сохранения xml-дерева в файл

    def xmlTreeToFile(self, flagUnq = True, info_msg = 'Коллекция успешно записана в файл'):
        try:
            if (flagUnq):
                self._xmlTree_.write(self.outFileUniqueNames)
                self.logger.info("File with unified xml-tree %s created", self.outFileUniqueNames)
            else:
                self._xmlTree_.write(self.outFileRestrdOrig)
                self.logger.info("File with original (restored) xml-tree %s created", self.outFileRestrdOrig)
            self._infoMsg_ = info_msg
        except Exception as e:
            self.logger.error('Error while saving XML-tree to file: ' + str(e) + '\n' + str(sys.exc_info()[0]))
            self._infoMsg_ = "Ошибка при сохранении XML-дерева"

            
### Здесь и далее до аналогичного комментария - попытка переписать метода под XML, названия попплывут для удобства

    def extrHTTPDataNamesAndLinks(self):
        self._linksToUpdate_ = tuple()
        self._curList_.clear()
        self._curLinkList_.clear()
        self.setFName = self.outFileUniqueNames
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('samplArgs_coll')
        xSet_2 = self._pumpUpXPathToBuild_('arg_NameAndValue')
        xSet_3 = self._pumpUpXPathToBuild_('samplPath')
        self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
        self._extrThreadGroupNode_()
        thrGrIndx = [thgr[4] for thgr in self._thrGrpLst_].index(self._currThrGrNam_)
        self._setLocalRootNode_(self._thrGrpLst_[thrGrIndx][0])
        allTreeNodes = self._xTreeLocalRoot_["hashTree"].findall(xSet[0])
        allSmplElms = [elm for elm in allTreeNodes if self._checkElmTypeClls_(elm, 'HTTPSampler')]
        self._currBkpCntrLst_.clear()
        tmpLst = []
        self._curList_.extend([s.find(xSet_2[0]).text for f in [i.findall(xSet_1[0]) for i in allSmplElms] for s in f if len(f)>0])
        self._curLinkList_.extend([j.find(xSet_3[0]).text for j in allSmplElms])
        tmpLst = self._delDublValsFrColl_(self._curList_)
        self._curList_.clear()
        self._curList_.extend(tmpLst)
        tmpLst = self._delDublValsFrColl_(self._curLinkList_)
        self._curLinkList_.clear()
        self._curLinkList_.extend(tmpLst)
        del tmpLst
        self.sbmDataDict = {x: [] for x in self._curList_}
        self.sbmActLinkDict = {a: [] for a in self._curLinkList_}
        self._curDict_ = self.sbmDataDict
        self._curLinkDict_ = self.sbmActLinkDict
        resDtTmp = []
        tmpLst = []
        tmpLinkLst = []
        for j in allSmplElms:
            self._currNode_["elem"] = j
            self._currNode_["hashTree"] = None
            smplrNm = self._getNodeName_(j)
            smplrCl = self._getNodeClass_(j)
            self._setNodeName_(j, 'someText_' + str(allSmplElms.index(j)))
            self._extrParntNodes_(self._currNode_["elem"])
            prntCntrlNm = self._getNodeName_(self._ancstNode_["elem"])
            self._storeOrigXElm_(j, prntCntrlNm, smplrCl, smplrNm, '--')
            tmpLinkLst = [self._curLinkDict_[p].append((prntCntrlNm, (smplrNm, None, 0))) for p in self._curLinkList_ if p==j.find(xSet_3[0]).text]
            jArgsLst = [l for l in j.findall(xSet_1[0])]
            for z in jArgsLst:
                tmpLst=[self._curDict_[k].append((prntCntrlNm, (smplrNm, z.find(xSet_2[1]).text, 0))) for k in self._curList_ if k == z.find(xSet_2[0]).text]
            
        del tmpLst
        del resDtTmp
        del tmpLinkLst
        self._optimDataDict_()
        self._constrictBkpCl_()
        self._infoMsg_ = "Сгенерирована коллекция элементов для ThreadGroup\n---" + self._currThrGrNam_ + "---"
        self.logger.info("Working collection of elements accumulated")
###
            

## Метод заполнения струткуры 'sbmNamesLst'

    def extrSbmDataNames(self):
        sRegItmDatNam = self._pumpUpRegsToBuild_('extrSbmDataNames')
        self._extrSomeKeysFromFunc_(sRegItmDatNam[0], sRegItmDatNam[1])

## Метод заполнения структуры данных 'wbUrlParamLst'

    def extrWebUrlNames(self):
        sRegWebUrlDatPar = self._pumpUpRegsToBuild_('extrWebUrlNames')
        self._extrSomeKeysFromFunc_(sRegWebUrlDatPar[0], sRegWebUrlDatPar[1])

## Метод заполнения структуры данных 'refSbmNameList'

    def extrSbmRefNames(self):
        sRegSbmRefNam = self._pumpUpRegsToBuild_('extrSbmRefNames')
        self._extrSomeKeysFromFunc_(sRegSbmRefNam[0], sRegSbmRefNam[1])

## Метод заполнения структуры данных 'refWbNameLst'

    def extrWebRefNames(self):
        sRegWbRefNam = self._pumpUpRegsToBuild_('extrWebRefNames')
        self._extrSomeKeysFromFunc_(sRegWbRefNam[0], sRegWbRefNam[1])

## Вспомогательный метод для извлечения ключей из струткуры для различных функций

    def _extrSomeKeysFromFunc_(self, *regExps):
        self.setEntity(self.getEntity())
        resItmDat = ''
        tmpLst = []
        for t in self.scrFldLst:
            os.chdir('./' + t)
            fileObj = open("Action.c", 'r', encoding='utf-8')
            resItmDat = self._regBuild_((regExps[0], ''), reDtAll = True).findall(fileObj.read())
            fileObj.close()
            os.chdir('..')
            self._curList_.extend([s for f in [self._regBuild_((regExps[1],''), reDtAll=False).findall(i[1]) for i in resItmDat] for s in f])
            self._curLinkList_.extend([j[0] for j in resItmDat])
        del resItmDat
        tmpLst = self._delDublValsFrColl_(self._curList_)
        self._curList_.clear()
        self._curList_.extend(tmpLst)
        tmpLst = self._delDublValsFrColl_(self._curLinkList_)
        self._curLinkList_.clear()
        self._curLinkList_.extend(tmpLst)
        del tmpLst

## Вспомогательный метод для очищения повторяющихся значей в рабочих списках и списках данных функций

    def _delDublValsFrColl_(self, lstToUpd):
        lstToUpd.reverse()
        if len(lstToUpd) > 0:
            for m in lstToUpd:
                lstToUpd = [n for n in lstToUpd if n != m]
                lstToUpd.insert(0, m)
        return lstToUpd

## Вспомогательный метод для работы со словарями данных, параметер - тип C-функции

    def _makeDataDicts_(self, dctType):
        if dctType == 'web_submit_data':
            if len(self.sbmNamesLst) == 0:
                print(" !> Список имен 'sbmNamesLst' пуст, метод 'extrSbmDataNames' будет запущен. Займет время...")
                self.extrSbmDataNames()
            self.sbmDataDict = {x: [] for x in self.sbmNamesLst}
            self.sbmActLinkDict = {a: [] for a in self.sbmActLinkList}
        elif dctType == 'webSubmit_Ref':
            if len(self.refSbmNameList) == 0:
                print(" !> Список имен 'refSbmNameList' пуст, метод 'extrSbmRefNames' будет запущен. Займет время...")
                self.extrSbmRefNames()
            self.refSbmDataDict = {x: [] for x in self.refSbmNameList}
            self.refSbmLinkDict = {a: [] for a in self.refSbmLinkList}
        elif dctType == 'web_url':
            if len(self.wbUrlParamLst) == 0:
                print(" !> Спсиок URL-деталей 'wbUrlParamLst' пуст, метод 'extrWebUrlNames' будет запущен. Займет время...")
                self.extrWebUrlNames()
            self.wbUrlDatalDict = {y: [] for y in self.wbUrlParamLst}
            self.wbURLLinkDict = {b: [] for b in self.wbURLLinkList}
        elif dctType == 'webUrl_Ref':
            if len(self.refWbLinkList) == 0:
                print(" !> Спсиок URL-деталей 'refWbLinkList' пуст, метод 'extrWebRefNames' будет запущен. Займет время...")
                self.extrWebRefNames()
            self.refWbDataDict = {z: [] for z in self.refWbNameLst}
            self.refWbLinkDict = {b: [] for b in self.refWbLinkList}

## Метод заполнения словаря данных 'sbmDataDict'

    def extrSbmItemData(self):
        self._makeDataDicts_('web_submit_data')
        sRegFSbmDat = self._pumpUpRegsToBuild_('extrSbmItemData')
        self._extrSomeDataFromFunc_(sRegFSbmDat[0], lambda k: (sRegFSbmDat[1], k), (sRegFSbmDat[2], ''))

## Метод заполнения словаря данных 'wbUrlDatalDict'

    def extrWebUrlData(self):
        self._makeDataDicts_('web_url')
        sRegFUrlDat = self._pumpUpRegsToBuild_('extrWebUrlData')
        self._extrSomeDataFromFunc_(sRegFUrlDat[0], lambda k: (k, sRegFUrlDat[1]), ('', ''))

## Метод заполнения словаря данных 'refSbmDataDict'

    def extrSbmRefData(self):
        self._makeDataDicts_('webSubmit_Ref')
        sRegFSmbRefDat = self._pumpUpRegsToBuild_('extrSbmRefData')
        self._extrSomeDataFromFunc_(sRegFSmbRefDat[0], lambda k: (k, sRegFSmbRefDat[1]), ('', ''))

## Метод заполнения словаря данных 'refWbDataDict'

    def extrWebRefData(self):
        self._makeDataDicts_('webUrl_Ref')
        sRegFSmbRefDat = self._pumpUpRegsToBuild_('extrWebRefData')
        self._extrSomeDataFromFunc_(sRegFSmbRefDat[0], lambda k: (k, sRegFSmbRefDat[1]), ('', ''))

## Вспомогательный метод для извлечения данных по ключам из струткуры для различных функций

    def _extrSomeDataFromFunc_(self, *regExps):
        self.setEntity(self.getEntity())
        resDtTmp = []
        tmpLst = []
        tmpLinkLst = []
        regDtTmp = self._regBuild_((regExps[0], ''), reDtAll=True)
        for i in self.scrFldLst:
            os.chdir('./' + i)
            fileObj = open("Action.c", 'r', encoding='utf-8')
            resDtTmp = regDtTmp.findall(fileObj.read())
            fileObj.close()
            os.chdir('..')
            for j in resDtTmp:
                tmpLst=[(k,self._regExec_(self._regBuild_(regExps[1](k),regExps[2],reDtAll=False),j[2],1)) for k in self._curList_]
                [self._curDict_[l].append((i, (j[0], m[1]))) for l in self._curList_ for m in tmpLst if l==m[0] and m[1] != None]
                tmpLinkLst = [self._curLinkDict_[p].append((i, (j[0], None))) for p in self._curLinkList_ if p==j[1]]
        del tmpLst
        del resDtTmp
        del tmpLinkLst
        self._optimDataDict_()

## Вспомогательный метод оптимизации словарей данных (очищает повторяющиеся значения)

    def _optimDataDict_(self):
        b = []
        for a in self._curDict_:
            b = self._curDict_[a]
            self._curDict_[a] = [(c, tuple([d[1] for d in b if d[0] == c])) for c in list(set([e[0] for e in b]))]
        for a in self._curLinkDict_:
            b = self._curLinkDict_[a]
            self._curLinkDict_[a] = [(c, tuple([d[1] for d in b if d[0] == c])) for c in list(set([e[0] for e in b]))]
        del b

## Метод получения Сущности по значению (ссылка или параметр)
## !!!Внимание: может вернуть несколько сущностей

    def retEntityByVal(self, valToChk):
        retEntityVal = []
        if len([t for t in self.sbmNamesLst if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[2])
        if len([t for t in self.sbmActLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[2])
        if len([t for t in self.wbUrlParamLst if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[0])
        if len([t for t in self.wbURLLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[0])
        if len([t for t in self.refSbmNameList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[3])
        if len([t for t in self.refSbmLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[3])
        if len([t for t in self.refWbNameLst if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[1])
        if len([t for t in self.refWbLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[1])
        return retEntityVal

## Вспомогательный метод - возвращает позицию в списке, если ключ найден в неск. сущностях

    def _ifKeyNoneSinge_(self, key_link):
        if (len(self.retEntityByVal(key_link)) > 1) and (self.retEntityByVal(key_link)[0] != self.getEntity()):
            print(""" !> Значение ключа соответствует нескольким сущностям...
                Операция будет выполнена со значением текущей.
                Можно перевыполнить операцию, изменив сущность.
                При обновлении словаря внесите обратные изменения предыдущим значением.""")
            posInt = [self.retEntityByVal(key_link).index(q) for q in self.retEntityByVal(key_link) if q == self.getEntity()].pop(0)
        else:
            posInt = 0
        return posInt

## Метод для получения всех значений для заданного ключа(параметер или ссылка) в виде списка кортежей
## None значения для ссылок означают, что изменения для данных функций и скриптов не менялись
## Необходимо следить за значением 'Entity' перед запуском - может вернуть запись не из того словаря

    @valid_key
    def getDataDictItem(self, key_link):
        pos = self._ifKeyNoneSinge_(key_link)
        self.setEntity(self.retEntityByVal(key_link)[pos])
        tmpLst = self._curDict_.get(key_link)
        if tmpLst != None:
            return self._curDict_[key_link]
        else:
            return self._curLinkDict_[key_link]
        del tmpLst
        del pos

## Метод получения списка всех скриптов (с указанием названия функций при установленном флаге 'funcFlag')
## где используется, переданный в параметре, ключ 'keyName'

    @valid_key
    def getScrListByKey(self, key_link, funcFlag = True):
        pos = self._ifKeyNoneSinge_(key_link)
        self.setEntity(self.retEntityByVal(key_link)[pos])
        tmpLst = self._curDict_.get(key_link)
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
        else:
            wrkDict = self._curLinkDict_
        if funcFlag is False:
            return [k[0] for k in wrkDict[key_link]]
        else:
            return [(l[0], tuple([m[0] for m in l[1]])) for l in wrkDict[key_link]]
        del tmpLst
        del wrkDict
        del pos

## Метод получения списка всех скриптов (с указанием названия функций при установленном флаге 'funcFlag')
## где используется, переданный в параметре, ключ 'linkKey'

    def _getScrListByLink_(self, linkKey, funcFlag = True):
        if funcFlag is False:
            return [k[0] for k in self._curLinkDict_[linkKey]]
        else:
            return [(l[0], tuple([m[0] for m in l[1]])) for l in self._curLinkDict_[linkKey]]

## Метод получения списка всех скриптов (с указанием названия функций при установленном флаге 'funcFlag')
## где используется заданный ключ с определенным значением - вх. параметер '*keyValue' (картеж вида (key, value))

    @valid_key
    @valid_request_params
    def getScrFuncByKeyValue(self, *keyValue, funcFlag = True):
        k_val = keyValue[0]
        pos = self._ifKeyNoneSinge_(k_val[0])
        self.setEntity(self.retEntityByVal(k_val[0])[pos])
        tmpLst = self._curDict_.get(k_val[0])
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
        else:
            wrkDict = self._curLinkDict_
        tmpLst = [(n[0], tuple([p[0] for p in n[1] if p[1] == k_val[1]])) for n in wrkDict[k_val[0]]]
        if funcFlag is False:
            return [r[0] for r in tmpLst if len(r[1]) != 0]
        else:
            return [r for r in tmpLst if len(r[1]) != 0]
        del tmpLst
        del pos

## Метод получения значения по ключу, названию скрипта, названию функции - 
## вх. параметер '*keyScrFunc' (картеж вида (key, script, funcName))

    @valid_key
    @valid_request_params
    def getValueByKeyScrFunc(self, *keyScrFunc):
        k_s_f = keyScrFunc[0]
        pos = self._ifKeyNoneSinge_(k_s_f[0])
        self.setEntity(self.retEntityByVal(k_s_f[0])[pos])
        tmpLst = self._curDict_.get(k_s_f[0])
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
        else:
            wrkDict = self._curLinkDict_
        del pos
        return [fl for itm in [[(q[0], ((v),)) for v in q[1] if v[0]==k_s_f[2]] for q in wrkDict[k_s_f[0]] if q[0] == k_s_f[1]] for fl in itm]

    def getAllSbmFuncFromScr(self, scrName):
        return None

## Метод внесения изменений в словарь данных по ключу, названию скрипта, названию функции - 
## вх. параметер '*keyScrFunc' (картеж вида (key, script, funcName))
## новое значение - вх. параметер 'newVal'

    @valid_key
    def setValueByKeyScrFunc(self, newVal, *keyScrFunc):
        k_s_f = keyScrFunc[0]
        pos = self._ifKeyNoneSinge_(k_s_f[0])
        self.setEntity(self.retEntityByVal(k_s_f[0])[pos])
        tmpLst = self._curDict_.get(k_s_f[0])
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
            k_s_f = [b for b in k_s_f]
            k_s_f.append('d')
            k_s_f = tuple(k_s_f)
        else:
            wrkDict = self._curLinkDict_
            k_s_f = [b for b in k_s_f]
            k_s_f.append('l')
            k_s_f = tuple(k_s_f)
        tmpScrInd = [wrkDict[k_s_f[0]].index(w) for w in wrkDict[k_s_f[0]] if w[0] == k_s_f[1]].pop(0)
        tmpFuncInd = [wrkDict[k_s_f[0]][tmpScrInd][1].index(x) for x in wrkDict[k_s_f[0]][tmpScrInd][1] if x[0]==k_s_f[2]].pop(0)
        tmpScrData = wrkDict[k_s_f[0]][tmpScrInd]
        tmpFuncData = wrkDict[k_s_f[0]][tmpScrInd][1]
        tmpFuncDataLst = [y for y in tmpFuncData]
        tmpFuncDataLst[tmpFuncInd] = (wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][0], newVal, 1)
        tmpFuncData = tuple(tmpFuncDataLst)
        del tmpFuncDataLst
        tmpScrDataLst = [z for z in tmpScrData]
        tmpScrDataLst[1] = tmpFuncData
        tmpScrData = tuple(tmpScrDataLst)
        del tmpScrDataLst
        wrkDict[k_s_f[0]][tmpScrInd] = tmpScrData
        del tmpFuncData
        del tmpScrData
        self.logger.info("New value = " + str(wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][:2]) + " set in controller '" + k_s_f[1] + "'")
        print("Новое значение = " + str(wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][:2]) + " установлено в контроллере '" + k_s_f[1] + "'")
        del tmpScrInd, tmpFuncInd
        del pos
        self._storeLinkFromSet_(k_s_f)

## Метод получения текущей рабочей сущности '_curEntity_'

    def getEntity(self):
        if self._curEntity_ == '':
            print(" !> Установите значение Entity - метод 'setEntity'")
        return self._curEntity_

## Метод установки текущей рабочей сущности '_curEntity_'

    def setEntity(self, entityName):
        if entityName not in ('webUrl_URL', 'webUrl_Ref', 'webSubmit_Item', 'webSubmit_Ref'):
            print(" !> Неверное имя сущности! Должно быть одно из списка:")
            print("    " + str(self.entityNames))
        else:
            self._curEntity_ = entityName
            if self._curEntity_ == 'webUrl_URL':
                self._curDict_ = self.wbUrlDatalDict
                self._curList_ = self.wbUrlParamLst
                self._curLinkList_ = self.wbURLLinkList
                self._curLinkDict_ = self.wbURLLinkDict
            elif self._curEntity_ == 'webUrl_Ref':
                self._curDict_ = self.refWbDataDict
                self._curList_ = self.refWbNameLst
                self._curLinkList_ = self.refWbLinkList
                self._curLinkDict_ = self.refWbLinkDict
            elif self._curEntity_ == 'webSubmit_Item':
                self._curDict_ = self.sbmDataDict
                self._curList_ = self.sbmNamesLst
                self._curLinkList_ = self.sbmActLinkList
                self._curLinkDict_ = self.sbmActLinkDict
            elif self._curEntity_ == 'webSubmit_Ref':
                self._curDict_ = self.refSbmDataDict
                self._curList_ = self.refSbmNameList
                self._curLinkList_ = self.refSbmLinkList
                self._curLinkDict_ = self.refSbmLinkDict

## Метод обновления файлов скриптов данными из временной структуры '_linksToUpdate_'

###
    def updateXMLTree(self):
        if len(self._linksToUpdate_) != 0:
            set(self._linksToUpdate_)
            self._linksToUpdate_ = tuple(self._linksToUpdate_)
            xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
            xSet_1 = self._pumpUpXPathToBuild_('samplArgs_coll')
            xSet_2 = self._pumpUpXPathToBuild_('arg_NameAndValue')
            xSet_3 = self._pumpUpXPathToBuild_('samplPath')
            xSet_4 = self._pumpUpXPathToBuild_('rootElemHashTree')
            for lnk in self._linksToUpdate_:
                self.setEntity(lnk[4])
                self._extrHostNode_(lnk[1])
                tmpLst = self._currNode_["hashTree"].findall(xSet[0])
                nestSmplrs = [elm for elm in tmpLst if self._checkElmTypeClls_(elm, 'HTTPSampler')]
                smplr = [smpl for smpl in nestSmplrs if self._getNodeName_(smpl) == lnk[2]].pop(0)
                if lnk[3] == 'd':
                    tstElmArgs = smplr.findall(xSet_1[0])
                    arg = [argN for argN in tstElmArgs if argN.find(xSet_2[0]).text == lnk[0]].pop(0)
                    strToInsert = self.getValueByKeyScrFunc(lnk)[0][1][0][1]
                    arg.find(xSet_2[1]).text = strToInsert
                    del tstElmArgs
                elif lnk[3] == 'l':
                    strToInsert = self.getValueByKeyScrFunc(lnk)[0][1][0][1]
                    smplr.find(xSet_3[0]).text = strToInsert
            del tmpLst
            del nestSmplrs
            del smplr
            self._linksToUpdate_ = tuple()
            self.logger.info("XML-tree successfully updated")
            self._infoMsg_ = "Текущее XML-дерево успешно обновлено"
        else:
            self.logger.info("Attempt to store empty list of changes to XML-tree")
            self._infoMsg_ = "Изменений в словаре не было - нечего обновлять"
        self._xTreeRoot_["elem"] = self._xmlTree_.getroot().find(xSet_4[0])
        self._xTreeRoot_["hashTree"] = self._xmlTree_.getroot().find(xSet_4[1])
            
    def wrtTreeToFile(self):
        self.xmlTreeToFile(True, "Коллекц. успешно запис. в файл\n---" + self.outFileUniqueNames + "---")
            
## Метод извлечения хранящихся строк для построение выражений XPath
            
    def _pumpUpXPathToBuild_(self, funcName=None):
        xAnyNode = './/*'
        xChldNodes = './'
        xAnyPropName = '[@testname="'
        xAnyPropClass = '[@testclass="'
        xAnyPropEndBrkts = '"]' 
        xReltvPrntNode = '/..'
        xAnyHashTree = './/hashTree'
        xChldHashTree = './hashTree'
        xNestNodesWithCls = './/*[@testclass][@testname]'
        xDirChldNodesWithCls = './*[@testclass][@testname]'
        xTestPlan = './/TestPlan'
        xThrdGrpNode = './/*[@testclass="ThreadGroup"]'
        xRootElem = './hashTree/TestPlan'
        xRootHashTree = './hashTree/hashTree'
        xSmplrArgs = './elementProp/collectionProp/'
        xArgName = './*[@name="Argument.name"]'
        xArgValue = './*[@name="Argument.value"]'
        xSmplrPath = './*[@name="HTTPSampler.path"]'

        if funcName == 'anyNode':
            return (xAnyNode, '')
        elif funcName == 'nodesWithName':
            return (xAnyPropName, xAnyPropEndBrkts)
        elif funcName == 'nodesWithClass':
            return (xAnyPropClass, xAnyPropEndBrkts)
        elif funcName == 'dirChldNode':
            return (xChldNodes, '')
        elif funcName == 'parntNode':
            return (xReltvPrntNode, '')
        elif funcName == 'all_nestNodes_cls':
            return (xNestNodesWithCls, xDirChldNodesWithCls)
        elif funcName == 'all_hashTrees':
            return (xAnyHashTree, xChldHashTree)
        elif funcName == 'TestPlan':
            return (xTestPlan, '')
        elif funcName == 'ThreadGroups':
            return (xThrdGrpNode, '')
        elif funcName == 'rootElemHashTree':
            return (xRootElem, xRootHashTree)
        elif funcName == 'samplArgs_coll':
            return (xSmplrArgs, '')
        elif funcName == 'arg_NameAndValue':
            return (xArgName, xArgValue)
        elif funcName == 'samplPath':
            return (xSmplrPath, '')
            
    def _getNodeName_(self, node):
        nodeName = None
        try:
            nodeName = node.attrib["testname"]
        except KeyError:
            nodeName = "no_Attribute"
            raise excpt.NodeAttributeError
        return nodeName
        
    def _setNodeName_(self, node, newVal):
        try:
            node.attrib["testname"] = newVal
        except KeyError:
            raise excpt.NodeAttributeError
            
    def _getNodeClass_(self, node):
        nodeClass = None
        try:
            nodeClass = node.attrib["testclass"]
        except KeyError:
            nodeClass = "no_Attribute"
            raise excpt.NodeAttributeError
        return nodeClass
        
## Метод сборки XPath 

    def _xPthBuild_(self, *cnctTpls):
        self._xPathUsrParam_.extend(['' for prm in range(abs(len(self._xPathUsrParam_)-len(cnctTpls)))])
        tmpLst = [k[0] + self._xPathUsrParam_.pop(0) + k[1] for k in cnctTpls]
        tmpStr = ''
        for xpPrt in tmpLst:
            tmpStr = tmpStr + xpPrt
        self._xPathUsrParam_.clear()
        del tmpLst
        return tmpStr

## Метод усечения названий сэмплеров

    def truncSmplrName(self):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        tmpLst = [itm for itm in self._xTreeRoot_["hashTree"].findall(xSet[0]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))]
        smplrCntErr = 0
        for smplr in tmpLst:
            try:
                origName = self._getNodeName_(smplr)
                newNameParts = urlpars.urlparse(origName)
                newNamePth = newNameParts.path.split('/')
                newName = newNamePth[len(newNamePth) - 1]
                smplr.attrib["testname"] = newName
            except:
                smplrCntErr += 1
                smplr.attrib["testname"] = newName
                self.logger.error("Truncating sampler name (%s) went wrong: " + str(sys.exc_info()[0]), origName)
        if smplrCntErr == 0:
            self.logger.info("Sampler names were succesfully truncated.")
        self._infoMsg_ = self._infoMsg_ + "\n--------"
        self._infoMsg_ = self._infoMsg_ + "\nПроизведено усечение назв. сэмплеров\n(признак = True)."
        if smplrCntErr != 0:
            self._infoMsg_ = self._infoMsg_ + "\n!!! ----"
            self._infoMsg_ = self._infoMsg_ + "\nОшибка при усечении назв. сэмплеров\n(всего " + str(smplrCntErr) + " ошибок)\nПодробнее в логе."
        del tmpLst
        
## Метод подсчета изменяемости значения параметров

    def calcVolatility(self):
        if len(self._curDict_.keys()) == 0:
            self._infoMsg_ = "Не сформирована коллекция.\nНеобходимо аккум. рабочую коллекц."
            return 0
        self.calcDictRes = {}
        tmpLst = []
        allVals = 0
        diffVals = 0
        isVolatile = None
        for key in self._curDict_.keys():
            tmpLst.clear()
            tmpLst = [smplr[1] for cntrl in self._curDict_[key] for smplr in cntrl[1]]
            allVals = len(tmpLst)
            diffVals = len(list(set(tmpLst)))
            if diffVals == 1:
                isVolatile = False
                self.calcDictRes[key] = (allVals, isVolatile)
            else:
                isVolatile = True
                if allVals != diffVals:
                    self.calcDictRes[key] = (abs(round(math.log(allVals) / math.log(diffVals/allVals), 2)), isVolatile)
                else:
                    devider = 1
                    divInt = 1
                    while (divInt > 0):
                        devider = devider * 10
                        divInt = allVals // devider
                    self.calcDictRes[key] = (abs(round(math.log(allVals ** allVals) / -(1 - allVals / devider), 2)), isVolatile)
        del tmpLst
        return 1
        
## Метод извлечения волатильности параметров из словаря

    def getVolatilParams(self):
        if self.calcVolatility() == 0:
            return 0
        tmpDct = {prm: val for prm, val in self.calcDictRes.items() if val[1] == self._ifVolatileParam_}
        if len(tmpDct.keys()) == 0:
            self._infoMsg_ = "Коллекция не содержит параметров\nс признаком волатильности = " + str(self._ifVolatileParam_)
            return 0
        tmpDct = {prm: val for prm, val in sorted(tmpDct.items(), key = lambda item: item[1][0], reverse = True)}
        self._infoMsg_ = "Сформирована статистика по параметрам;\nс признаком волатильности = " + str(self._ifVolatileParam_)
        return list(tmpDct.keys())
        
## Метод определения пользовательской правки параметров

    def editnIndicatInParams(self, key, controller = None, sampler = None):
        cntAll = 0
        cntEdtd = 0
        tmpLst = self.getDataDictItem(key)
        tmpIntersctLst = [itm for itm in tmpLst if itm[0] == controller]
        tmpLst = tmpIntersctLst if any(tmpIntersctLst) else tmpLst
        for cntrl in tmpLst:
            for smplr in cntrl[1]:
                if smplr[0] == sampler:
                    cntAll = 1
                    cntEdtd = smplr[2]
                    break
                cntAll += 1
                if smplr[2] == 1:
                    cntEdtd += 1
        try:
            res = cntEdtd / cntAll
            if res == 0:
                return "new"
            elif res == 1:
                return "edited"
            else:
                return "inProgress"
        except ZeroDivisionError:
            self.logger.error("Empty samplers list for controller. Check XML-tree.")
            raise excpt.NoneSamplersInController
            
        ##print(self.getDataDictItem(key))
=======
# coding: utf8

##Copyright (c) 2020 Лобов Евгений
## <ewhenel@gmail.com>
## <evgenel@yandex.ru>

## This file is part of JMScript_Detail.
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
##    along with JMScript_Detail.  If not, see <http://www.gnu.org/licenses/>.
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
import re
import sys
import math
import urllib
import datetime
import pickle
import logging
import functools
from collections import deque
import xml.etree.ElementTree as ET
import urllib.parse as urlpars
import exceptionHandler as excpt

class JMScriptItems:

    """Get details from scripts"""

## Инициализация при создании объекта

    def __init__(self):
        self.setPATH = "C:/Users/Public/work/NT/Projects/Calc_Stat"                   # Рабочая директория
        self.setDirMASK = '^uc[_0-9]+'                      # Маска для фильтра скриптов
        self.setPrefTrailInUniqNames = {"pref": '~', "trail": "#"} # Задаем символы префикса начала и разделителя перед номер для уник. имен
        
        self.setFName = 'example.jmx'                       # Название .jmx файла, должно присутствовать в каталоге self.scrFlsLst  
        
        self.setClassDir = os.getcwd()                      # Путь к директории с данным классом
        
        self._currDate_ = datetime.datetime.today()         # Текущая дата
        self._xmlTree_ = None                               # Полученное xml-дерево из файла скрипта JMeter
        self._xTreeRoot_ = {"elem": None, "hashTree": None} # Корневой элемент xml-дерева
        self._xTreeLocalRoot_ = {"elem": None, "hashTree": None} # Локальный корневой элемент xml-дерева, например для итериций внутри одной ThreadGroup
        self._thrGrpLst_ = []                               # Список ThreadGroup с названиями
        self._currThrGrNam_ = None                          # Имя выбранной ThreadGroup
        self._currBkpCntrLst_ = []                          # Список с указанием ориг. и изменных названий для дампа и восстановления названий нодов
        self._currDumpFName_ = None                         # Название файла для текущей коллекции
        self._currDumpDir_ = None                           # Название папки дампа сессии
        self.outFileUniqueNames = 'outputUnq.jmx'           # Файл для сохранения xml-дерева с уникальными названиями нодов (внутри ThreadGroup)
        self.outFileRestrdOrig = 'restoredOrig.jmx'         # Файл для восстановления xml-дерева с уникальными названиями нодов (внутри ThreadGroup)
        self._xPathUsrParam_ = []                           # ??Список пользовательских параметров для формирования xPath
        self._currNode_ = {"elem": None, "hashTree": None}  # Текущий нод
        self._ancstNode_ = {"elem": None, "hashTree": None} # Нод предка
        self.ancstNodeChain = deque()
        self._ancstNdClass_ = None                          # Класс нода предка
        self._nestedElemsOfType_ = []                       # Список дочерних элементов определенного типа, одно или многоуровой вложенности
        
        self._curEntity_ = ''                               # Текущая заданная сущность (рабочая)
        self._curDict_ = {}                                 # Текущий заданый словарь (рабочий)
        self._curList_ = []                                 # Текущий заданый список ключей (рабочий)
        self._curLinkList_ = []                             # Текущий заданый список ссылок (рабочий)
        self._curLinkDict_ = {}                             # Текущий заданый словарь ссылок (рабочий
        self.entityNames = ('webUrl_URL', 'webUrl_Ref', 'webSubmit_Item', 'webSubmit_Ref')    # Список возможных сущностей (расширяется, при добавлении соответствующих методов обработки)
        os.chdir(self.setPATH)
        self.scrFlsLst = []                                 # Список файлов .jmx в рабочей директории
        self.scrFldLst = []                                 # Список каталогов в рабочей директории (папок со скриптами)
        self.sbmNamesLst = []                               # Список ключей для значений параметров (ItemData) функции web_submit_data
        self.sbmDataDict = {}                               # Словарь данных для сущности 'webSubmit_Item'
        self.sbmActLinkList = []                            # Список ссылок в строке Action функции web_submit_data
        self.sbmActLinkDict = {}                            # Словарь ссылок в строке Action функции web_submit_data
        self.refSbmLinkList = []                            # Список ссылок в строке Referer функции web_submit_data
        self.refSbmLinkDict = {}                            # Словарь ссылок в строке Referer функции web_submit_data
        self.refSbmNameList = []                            # Список ключей для ссылки в строке Referer функции web_submit_data
        self.refSbmDataDict = {}                            # Словарь данных для ссылки в строке Referer функции web_submit_data
        self.wbUrlParamLst = []                             # Список ключей для параметров в поле URL функции wer_url
        self.refWbNameLst = []                              # Список ключей для параметров в поле Referer функции web_url
        self.wbUrlDatalDict = {}                            # Словарь данных для сущности 'webUrl_URL'
        self.wbURLLinkList = []                             # Список ссылок без парам. в строке URL функции web_url
        self.wbURLLinkDict = {}                             # Словарь ссылок без парам. в строке URL функции web_url
        self.refWbDataDict = {}                             # Словарь данных для сущности 'webUrl_Ref'
        self.refWbLinkList = []                             # Список ссылок в строке Referer функции web_url
        self.refWbLinkDict = {}                             # Словарь ссылок в строке Referer функции web_url
        self._linksToUpdate_ = tuple()                      # Вспомогательный картеж для хранения изменений перед обновлением файлов
        self._selctdKey_ = None                             # Текущий выбраный ключ
        self._dctSmplThru_ = {}                             # Словарь оригинальных названий при режиме сквозной нумерации
        self._smplThruVar_ = "Controller"                   # Переменная сквозной нумерации
        self._ifNotRestoreSamplrs_ = False                  # Переменная восстановления оригинальных названий сэмплеров
        self._ifCutUrlInSmpl_ = False                       # Переменная, включающая признак усечения названий сэмплеров
        self.calcDictRes = {}                               # Словарь волатильности параметров
        self._ifVolatileParam_ = False                      # Переменная признака волатильности 

        #self._checkDmpDirExst_()                           # Проверка, что общий каталог для дампов существует
        self.excptHandl = excpt.ExceptHandler()             # Создание объекта класса ExceptHandler
        self.logger = None                                  # Логгер 
        self._logOffset_ = 0                                # Текущая позиция в файле лога приложения
        self._loggerInit_()                                 # Инициализация логгера
        self._consHandlerInit_()                            # Инициализация хэндлера для ошибок в консоле
        self.excptHandl.logger = self.logger                # Назначение логгера в классе exceptionHandler

        self.logger.info("JMScript_Detail object created")

        self._infoMsg_ = 'JMScript_Detail (c)'              # Текущее сообщение для вывода пользователю
        self.platf = sys.platform                           # Платформа
        
        print("\n\n* * * * JMScript_Details (ver. 4) * * * *")
        print("\n  * * * Класс для сбора и классификации данных сэмплеров JMeter * * *")
        print("\n\n                   Copyright (c) 2020 Лобов Евгений                    \n\n")

## Декоратор для проверки валидности ключа
    def valid_key(meth):
        def wrapper(*args, **kwargs):
            if meth.__name__ == 'setValueByKeyScrFunc':
                if len(args[0].retEntityByVal(args[2][0])) == 0:
                    args[0]._infoMsg_ = "Не выбраны (отмечены) значения для изменения.\nТакже см. опцию Все знач."
                    raise excpt.NoKeyFoundInDict
                else:
                    ret = meth(*args)
            elif (isinstance(args[1], tuple)) and (meth.__name__ != 'setValueByKeyScrFunc'):
                if len(args[0].retEntityByVal(args[1][0])) == 0:
                    args[0]._infoMsg_ = "По ключу '" + args[1][0] + "' ничего не найдено.\nВозможно не отмечена опция Автовыбор"
                    raise excpt.NoKeyFoundInDict
                else:
                    ret = meth(*args, **kwargs)
            elif (isinstance(args[1], str)) and (meth.__name__ != 'setValueByKeyScrFunc'):
                if len(args[0].retEntityByVal(args[1])) == 0:
                    args[0]._infoMsg_ = "По ключу '" + args[1] + "' ничего не найдено.\nВозможно не отмечена опция Автовыбор"
                    raise excpt.NoKeyFoundInDict
                else:
                    ret = meth(*args, **kwargs)
            elif not (isinstance(args[1], str)) and not (isinstance(args[1], tuple)):
                args[0].logger.error("Unknown item '" + str(args) + "' passed to meth '" + meth.__name__ + "'") 
                raise excpt.UnknownStructItem
            else:
                pass
            return ret
        return wrapper
        
## Декоратор для проверки возвращаемого списка по переданным условиям
    def valid_request_params(meth):
        def wrapper(*args, **kwargs):
            res = meth(*args, **kwargs)
            if len(res) == 0:
                args[0]._infoMsg_ = "По заданным значениям '" + str(tuple(args[1])) + "'\nв коллекции ничего не найдено.\nПроверьте корректность значений\nи/или опцию Автовыбор"
                raise excpt.NoDataInDictsWithFilter
            else:
                return res
        return wrapper
		
## Необработанные исключения перенаправляются в логгер
    def _unhandledExcept_(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys._excepthook_(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("Exception", exc_info = (exc_type, exc_value, exc_traceback))

## Определение логгера
    def _loggerInit_(self):
        self.logger = logging.getLogger('jmscript.detail')
        self.logger.setLevel(logging.INFO)

## Добавление хэндлера для вывода ошибок в консоль
    def _consHandlerInit_(self):
        self.logHandler = logging.StreamHandler()
        self.logHandler.setLevel(logging.ERROR)
        self.logFormat = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        self.logHandler.setFormatter(self.logFormat)
        self.logger.addHandler(self.logHandler)

## Перемещение лога сессии работы с приложения в дамп-директорию
    def _moveLogToDmp_(self):
        self.logger.info("Run app log to be moved to " + self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/jmscript_detail.log')
        fAppLog = open(self.setClassDir + '/jmscript.log', '+r')
        fAppLog.seek(self._logOffset_)
        buffAppLog = fAppLog.read()
        fAppLog.close()
        fDetLog = open(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/jmscript_detail.log', '+w')
        fDetLog.write(buffAppLog)
        fDetLog.close()
        logger = self.logger.manager.loggerDict['jmscript']
        handler = self.logger.manager.loggerDict['jmscript'].handlers[0]
        logger.removeHandler(handler)
        logHandler = logging.FileHandler(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/jmscript_detail.log')
        logHandler.setLevel(logging.INFO)
        logFormat = logging.Formatter('%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')
        logHandler.setFormatter(logFormat)
        logger.addHandler(logHandler)
        del buffAppLog

## Проверка что существует директория для дампов
    def _checkDmpDirExst_(self):
        tmpDmpDirLst = [dir for dir in os.listdir(self.setPATH) if dir == 'jmProj_dumps']
        if len(tmpDmpDirLst) == 0:
            self.logger.info("Dump directory doesn't exist, will be created")
            os.mkdir('jmProj_dumps')
        del tmpDmpDirLst
 
## Вспомогательный метод для добавления изменненого значения словаря во временное структуру '_linksToUpdate_'

    def _storeLinkFromSet_(self, *lnks):
        tmpLst = [h for h in lnks[0]]
        tmpLst.append(self.getEntity())
        lnk_to_stre = tuple(tmpLst)
        tmpLst = [a for a in self._linksToUpdate_]
        tmpLst.append(lnk_to_stre)
        self._linksToUpdate_ = tuple(tmpLst)
        del tmpLst

## Метод загрузки .jmx-файла и создания xml-дерева

    def getJMXFileAndMakeTree(self, fName = True):
        xSet = self._pumpUpXPathToBuild_('rootElemHashTree')
        tmpFlLst = []
        ifFExst = bool(len([f for f in self.scrFlsLst if f == self.setFName]) == 1)
        if (ifFExst):
            self._checkDmpDirExst_()
            self._xmlTree_ = ET.parse(self.setFName)
            self._xTreeRoot_["elem"] = self._xmlTree_.getroot().find(xSet[0])
            self._xTreeRoot_["hashTree"] = self._xmlTree_.getroot().find(xSet[1])
            self.logger.info("JMX-file parsed and loaded, xml-tree created")
            self._infoMsg_ = "Загружен файл " + self.setFName
            if (self._ifCutUrlInSmpl_):
                self.truncSmplrName()
        else:
            self.logger.info("Can't load jmx-file")
            self._infoMsg_ = "Такой *.jmx файл не найден"

## Метод извлечения названий каталогов в директории setPATH

    def catchJMXFilesInPath(self):
        tmpLst = []
        try:
            os.chdir(self.setPATH)
        except FileNotFoundError:
            self._infoMsg_ = "Директория не найдена"
            return -1
        self.scrFlsLst = os.listdir('.')
        tmpLst = [f for f in self.scrFlsLst if f[len(f)-4:].find(".jmx")!=-1]
        self.scrFlsLst = tmpLst
        if len(self.scrFlsLst) == 0:
            self._infoMsg_ = "Тут jmx-файлов не обнаружено"
            return -1
        del tmpLst
        return 0
        
## Метод получения струткуры нодов элементов класса Контроллер (точнее типа, Контроллеры различаются),
## а также генерация аналогичной с уникальными идентификаторами (Name).
## После окончания работы с основными (не вспомогательными) коллекциями 
## все ориг. названия можно восстановить из файлов дампа

    def xmlTreeStructToUnqNams(self):
        xSet = self._pumpUpXPathToBuild_('TestPlan')
        if self._getNodeClass_(self._xTreeRoot_["elem"]) != "TestPlan":
            logger.error("Wrong root element, class of _xTreeRoot_ is " + self._getNodeClass_(self._xTreeRoot_["elem"]))
            self._infoMsg_ = "Некорректное знач. корня дерева,\n см. лог"
        else:
            self._sessDmpDir_()
            self._extrThreadGroupNode_()
            self._extrCntrllNode_()
            self._dctSmplThru_ = {}
            self._currBkpCntrLst_ = self._thrGrpLst_.copy()
            self._currDumpFName_ = 'pcklUnqNm_TstPl-' + self._getNodeName_(self._xTreeRoot_["elem"]).replace(' ', '%') 
            self._dumpOrigCntrlNm_()
            self.xmlTreeToFile(True, "Нужно сгенерировать осн. коллекц.\nдля ThreadGroup")

## Метод задания локального root элемента

    def _setLocalRootNode_(self, node):
        if node.tag != "hashTree":
            self._xTreeLocalRoot_["elem"] = node
            self._xTreeLocalRoot_["hashTree"] = self._getNodeElemHashTree_(node)
        
## Метод извлечения Нодов для всех элементов ThreadGroup
    
    def _extrThreadGroupNode_(self):
        self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
        xSet = self._pumpUpXPathToBuild_('ThreadGroups')
        tmpNodeLst = self._xTreeLocalRoot_["hashTree"].findall(xSet[0])
        self._currBkpCntrLst_.clear()
        tmpThGrLst = tmpNodeLst.copy()
        self._xElmUniqueName_(tmpNodeLst, 'TestPlan')
        if len(self._currBkpCntrLst_) == 0:
            self._thrGrpLst_ = [tuple([thgr, '--', '--', '--', self._getNodeName_(thgr)]) for thgr in tmpThGrLst]
        else:
            self._thrGrpLst_ = self._currBkpCntrLst_.copy()
            self._thrGrpLst_.reverse()
        self.logger.info("All ThreadGroups in TestPlan extracted")
        del tmpNodeLst
        del tmpThGrLst
        
## Метод, который будет использоваться вместо _checkIfxElmIsCntrll_
## достаточно вызова с параметром имени класса для проверки

    def _checkElmTypeClls_(self, node, ndClass=None):
        fndClss = self._getNodeClass_(node)
        return bool(fndClss.find(ndClass)!=-1)

## Метод извлечения Нодов для всех элементов класса Controller для каждого элемента ThreadGroup

    def _extrCntrllNode_(self, cntrlLst = None, thgrName = None, nodeClass = "Controller"):
        tmpLst = []
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        if nodeClass == "Controller":
            tmpLst = [[itm for itm in self._getNodeElemHashTree_(thgr[0]).findall(xSet[0]) if (self._checkElmTypeClls_(itm, "Controller"))] for thgr in self._thrGrpLst_]
            if self._smplThruVar_ == "TestPlan":
                smplrLst = [itm for itm in self._xTreeRoot_["hashTree"].findall(xSet[0]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))]
                self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
                self._xElmUniqueName_(smplrLst, "TestPlan", smplrsThru = True)
                del smplrLst
        elif nodeClass == "Sampler":
            tmpLst = [[itm for itm in self._getNodeElemHashTree_(cntrl).findall(xSet[1]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))] for cntrl in cntrlLst]
        else:
            raise Exception
        for itmLst in tmpLst:
            self._currBkpCntrLst_.clear()
            if nodeClass == "Controller":
                itmLstCpy = itmLst.copy()
                self._setLocalRootNode_(self._thrGrpLst_[tmpLst.index(itmLst)][0])
                self._xElmNestedMapp_(itmLst, 'ThreadGroup')
                self._xElmUniqueName_(itmLst, 'ThreadGroup')
                self._currDumpFName_ = 'pcklUnqNm_ThGr-' + self._getNodeName_(self._xTreeLocalRoot_["elem"]).replace(" ", "%")
                self.logger.info("Nodes from ThreadGroup %s exctracted", self._getNodeName_(self._xTreeLocalRoot_["elem"]))
                if self._smplThruVar_ == "ThreadGroup":
                    smplrLst = [itm for itm in self._xTreeLocalRoot_["hashTree"].findall(xSet[0]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))]
                    self._xElmUniqueName_(smplrLst, "ThreadGroup", smplrsThru = True)
                    del smplrLst
                self._dumpOrigCntrlNm_()
                self._extrCntrllNode_(itmLstCpy, self._getNodeName_(self._xTreeLocalRoot_["elem"]), nodeClass = "Sampler")
            elif nodeClass == "Sampler":
                self._setLocalRootNode_(cntrlLst[tmpLst.index(itmLst)])
                cntrlClass = self._getNodeClass_(self._xTreeLocalRoot_["elem"])
                tmpThru = (self._smplThruVar_ in ("ThreadGroup", "TestPlan"))
                self._xElmUniqueName_(itmLst, cntrlClass, smplrsThru = tmpThru, thGrIfSmplr = thgrName)
                self._currDumpFName_ = 'pcklUnqNm_Cntrl-' + thgrName.replace(' ', '%') + '-' + self._getNodeName_(self._xTreeLocalRoot_["elem"]).replace(" ", "%")
                self.logger.info("Nodes from Controller %s exctracted", self._getNodeName_(self._xTreeLocalRoot_["elem"]))
                self._dumpOrigCntrlNm_()
                del tmpThru
            else:
                raise Exception
        del tmpLst
        self._currBkpCntrLst_.clear()

## Метод создание префиксов для структуры составных вложенных элементов (для идентификации в коллекции)
        
    def _xElmNestedMapp_(self, cntrLst, parntNdClass):
        tmpLst = []
        tmpVar = None
        tmpVarNew = None
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('nodeProps')
        for nd in cntrLst:
            tmpLst = [j for j in self._getNodeElemHashTree_(nd).findall(xSet[0]) if cntrLst[cntrLst.index(nd):].count(j)!=0]
            if len(tmpLst) != 0:
                for itm in tmpLst:
                    if (self._checkElmTypeClls_(itm, "Controller")):
                        prop = self._getNodeName_(itm)
                        newPropVal = self.setPrefTrailInUniqNames["pref"] + prop
                        self._setNodeName_(itm, newPropVal)
                        elmJmClass = self._getNodeClass_(itm)
                        self._extrParntNodes_(itm, parntNdClass)
                        prntNdName = self._getNodeName_(self._ancstNode_["elem"])
                        self._storeOrigXElm_(itm, prntNdName, elmJmClass, prop, newPropVal)
        del tmpLst
        del tmpVar
        del tmpVarNew

## Метод создание нумерации для структуры составных элементов (для идентификации в коллекции)

    def _xElmUniqueName_(self, revCntrLst, parntNdClass, smplrsThru = False, thGrIfSmplr = None):
        tmpVar = None
        tmpVarNode = None
        tmpVarNew = None
        bkpCntrLst = self._currBkpCntrLst_
        revCntrLst.reverse()
        tmpLst = [self._getNodeName_(pr) for pr in revCntrLst]
        tmpThGrIfSmplr = []
        tmpThGrIfSmplr.append(thGrIfSmplr)
        tmpThGrIfSmplr.append(None)
        tmpThGrIfSmplr = list(filter(lambda a: a != None, tmpThGrIfSmplr))
        while(len(tmpLst)!=0):
            itm = tmpLst[0]
            itmCnt = tmpLst.count(itm)
            if itmCnt == 1:
                if (smplrsThru) and (itm in self._dctSmplThru_.keys()):
                    elmJmClass = self._getNodeClass_(revCntrLst[0])
                    self._extrParntNodes_(revCntrLst[0], parntNdClass)
                    prntNdName = self._getNodeName_(self._ancstNode_["elem"])
                    self._storeOrigXElm_(revCntrLst[0], *tmpThGrIfSmplr, prntNdName, elmJmClass, self._dctSmplThru_[itm], itm)
                tmpLst.pop(0)
                revCntrLst.pop(0)
                continue
            while(itmCnt>0):
                itmIndx = tmpLst.index(itm)
                propName = self._getNodeName_(revCntrLst[itmIndx])
                propNameNew = propName +  self.setPrefTrailInUniqNames["trail"] + str(itmCnt)
                self._setNodeName_(revCntrLst[itmIndx], propNameNew)
                elmJmClass = self._getNodeClass_(revCntrLst[itmIndx])
                self._extrParntNodes_(revCntrLst[itmIndx], parntNdClass)
                prntNdName = self._getNodeName_(self._ancstNode_["elem"])
                if (smplrsThru):
                    self._dctSmplThru_[propNameNew] = propName
                else:
                    self._storeOrigXElm_(revCntrLst[itmIndx], *tmpThGrIfSmplr, prntNdName, elmJmClass, propName, propNameNew)
                tmpLst.pop(itmIndx)
                revCntrLst.pop(itmIndx)
                itmCnt = tmpLst.count(itm)
                del propName
                del propNameNew
        del tmpLst
        del tmpVarNode
        del tmpThGrIfSmplr
        ##bkpCntrLst.reverse()
        self._currBkpCntrLst_ = bkpCntrLst
        
## Метод получения родительских нодов 

    def _extrParntNodes_(self, node, upprNodeClass=None, apndQueue = False):
        ndName = self._getNodeName_(node)
        ndClass = self._getNodeClass_(node)
        self._xPathUsrParam_.append('')
        self._xPathUsrParam_.append(ndClass)
        self._xPathUsrParam_.append(ndName)
        self._xPathUsrParam_.append('')
        tmpLst = []
        tmpLst.append(self._pumpUpXPathToBuild_('anyNode'))
        tmpLst.append(self._pumpUpXPathToBuild_('nodesWithClass'))
        tmpLst.append(self._pumpUpXPathToBuild_('nodesWithName'))
        tmpLst.append(self._pumpUpXPathToBuild_('parntNode'))
        xSetStr = self._xPthBuild_(*tmpLst)
        parentHashTree = self._xTreeLocalRoot_["hashTree"].find(xSetStr)
        parentElemTag = self._getNodeElemTag_(parentHashTree)
        self._ancstNode_["elem"] = parentElemTag
        self._ancstNode_["hashTree"] = parentHashTree
        tmpVar = self._ancstNode_
        if (apndQueue):
            self.ancstNodeChain.append(tmpVar.copy())
        del tmpLst
        while((upprNodeClass!=None) and (upprNodeClass!=self._getNodeClass_(self._ancstNode_["elem"]))):
            self._extrParntNodes_(self._ancstNode_["elem"], upprNodeClass, apndQueue)


    def _getNestedElemsOfType_(self, node, elemType_class, stopOnType_class = '_DummyClass_'):
        tmpLst = []
        self._xPathUsrParam_.append(elemType_class)
        tmpLst.append(self._pumpUpXPathToBuild_('nodesWithClass'))
        xSetStr = self._xPthBuild_(*tmpLst)
        self._xPathUsrParam_.append(stopOnType_class)
        xSetStr_lim = self._xPthBuild_(*tmpLst)
        print(xSetStr)
        self._currNode_['elem'] = node
        self._currNode_['hashTree'] = self._getNodeElemHashTree_(node)
        xSet_1 = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        #resLst.append(self._currNode_['hashTree'].findall(xSet_1[0]))
        tmpLst = self._currNode_['hashTree'].findall(xSet_1[1])
        for elm in tmpLst:
            if (elm.find(xSetStr) is not None):
                self._nestedElemsOfType_.append(elm)
            elif (elm.find(xSetStr_lim) is None):
                self._getNestedElemsOfType_(elm, elemType_class, stopOnType_class)
            else:
                pass
        #resLst.appe[itm for itm in tmpLst if itm.find(xSetStr) != None]
        #while ((stopOnType_class != None) and ())

            
    def _getNodeElemTag_(self, hashTr):
        return self._getNodeElem_('hashTree', hashTr)
        
    def _getNodeElemHashTree_(self, nodeTag):
        return self._getNodeElem_('elem', nodeTag)
            
    @functools.lru_cache(maxsize = None)        
    def _getNodeElem_(self, itmType, item):
        xSet = self._pumpUpXPathToBuild_('all_hashTrees')
        xSet_1 = self._pumpUpXPathToBuild_('dirChldNode')
        xSet_2 = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        hostHashTr = None
        if item == self._xTreeRoot_[itmType]:
            hostHashTr = self._xmlTree_.getroot().find(xSet[1])
        else:
            hashTrLst = self._xTreeRoot_["hashTree"].findall(xSet[0])
            hashTrLst.insert(0, self._xTreeRoot_["hashTree"])
            shiftPos = 0
            tmpLst = []
            while (tmpLst.count(item) < 1):
                hostHashTr = hashTrLst[shiftPos]
                tmpLst = hostHashTr.findall(xSet[1]) if itmType == 'hashTree' else hostHashTr.findall(xSet_2[1])
                shiftPos += 1
                ###Needs to be debugged due to it seems there are xcesive calls when extr threadgroups
            del tmpLst
        tmpLstSiblElms = hostHashTr.findall(xSet_1[0])
        try:
            return tmpLstSiblElms[tmpLstSiblElms.index(item) - 1] if itmType == 'hashTree' else tmpLstSiblElms[tmpLstSiblElms.index(item) + 1]
        except:
            self.logger.error("Got error while retrieving item for " + itmType , str(sys.exc_info()[0]))
            return None
            
            
## Метод извлечения хостового нода для свойств и т.д.

    def _extrHostNode_(self, prop):
        self._xPathUsrParam_.append('')
        self._xPathUsrParam_.append(prop)
        xSetStr = self._xPthBuild_(self._pumpUpXPathToBuild_('anyNode'), self._pumpUpXPathToBuild_('nodesWithName'))
        tmpNode = self._xTreeLocalRoot_["hashTree"].find(xSetStr)
        tmpHashTree = self._getNodeElemHashTree_(tmpNode)
        self._currNode_["elem"] = tmpNode
        self._currNode_["hashTree"] = tmpHashTree
        del tmpNode
        del tmpHashTree

## Метод заполнения коллекции оригинальных элементов и их оригинальных названий

    def _storeOrigXElm_(self, *vals):
        if isinstance(vals[1], tuple):
            vals = tuple(vals[1])
        tmpLst = [itm[0] for itm in self._currBkpCntrLst_]
        tmpVar = (vals)
        if tmpLst.count(vals[0]) != 0:
            indx = tmpLst.index(vals[0])
            exstOrigName = [val for val in self._currBkpCntrLst_[indx]][len(self._currBkpCntrLst_[indx])-2]
            valsLst = [vl for vl in vals]
            valsLst[len(vals)-2] = exstOrigName
            tmpVar = valsLst
            self._currBkpCntrLst_[indx] = tuple(tmpVar)
        else: 
            self._currBkpCntrLst_.append(vals)
        del tmpLst
        del tmpVar
        
## Метод удаляет все ссылки (объекты) дерева из коллекции для бэкапа, остаются только текстовые параметры

    def _cutxElmPartInRestoCllctn_(self):
        tmpLst = [tuple([pars for pars in clItm[1:]]) for clItm in self._currBkpCntrLst_]
        self._currBkpCntrLst_ = tmpLst
        del tmpLst
        
## Метод дампа коллекции с ориг. и изменными названиями нодов в файл
        
    def _dumpOrigCntrlNm_(self):
        self._cutxElmPartInRestoCllctn_()
        # try:
        #     with open(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/' + self._currDumpFName_ + '.txt', 'wb+') as fObj:
        #         self.logger.info("Dump file %s stored in dump directory", self._currDumpFName_)
        #         pickle.dump(self._currBkpCntrLst_, fObj)
        #     fObj.close()
        #     return False
        # except:
        #     print('Ошибка при дампе коллекции: ' + str(sys.exc_info()[0]))
        #     return True
        with open(self.setPATH + '/jmProj_dumps/' + self._currDumpDir_ + '/' + self._currDumpFName_ + '.txt',
                  'wb+') as fObj:
            self.logger.info("Dump file %s stored in dump directory", self._currDumpFName_)
            pickle.dump(self._currBkpCntrLst_, fObj)
        #fObj.close()
        return False

## Метод восстановления ориг. названий нодов из сохраненных в файлах коллекциях
        
    def restorOrigCntrlNm(self):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        tmpResLst = []
        self._extrThreadGroupNode_()
        self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
        smplrLst = [itm for itm in self._xTreeRoot_["hashTree"].findall(xSet[0]) if ((self._checkElmTypeClls_(itm, "Controller")) and (itm.tag != "elementProp"))]
        if not (self._ifNotRestoreSamplrs_):
            tmpResLst.append(self._restorOrigCntrlNm_(smplrLst, 'Cntrl'))
        tmpResLst.append(self._restorOrigCntrlNm_(self._thrGrpLst_, 'ThGr'))
        tmpResLst.append(self._restorOrigCntrlNm_([(self._xTreeRoot_["elem"], '--', '--', '--',self._getNodeName_(self._xTreeRoot_["elem"]).replace(' ', '%'))], 'TstPl'))
        if tmpResLst.count(-1) != 0:
            self._infoMsg_ = "Ошибка при восстановлении\nориг. назв. элем. дерева,\nнужно проверить дампы.\nСм. лог"
        else:
            msgText = "Файл с оригинальными(восстан.)\nназв. элементов дерева создан ---" + self.outFileRestrdOrig + "---"
            if (self._ifNotRestoreSamplrs_):
                msgText = msgText + "\n--------"
                msgText = msgText + "\nБез восст. оригинал. назв. сэмплеров\n(признак = True)."
            self.xmlTreeToFile(False, msgText)
        del smplrLst
        
## Вспомогательный метод для загрузки коллекций из файлов и восстановления

    def _restorOrigCntrlNm_(self, elmLst, fPstfx):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('prop_nodeName')
        tmpElmNm = None
        cntrlLst = []
        tmpFlLst = []
        flLst = []
        if fPstfx == "Cntrl":
            cntrlLst = [self._getNodeName_(itm) for itm in elmLst]
            os.chdir('jmProj_dumps/'+ self._currDumpDir_)
            tmpFlLst = os.listdir('.')
            tmpFlLst = [fl.split('-') for fl in tmpFlLst if fl.split('-')[0] == "pcklUnqNm_Cntrl"]
            for flItm in tmpFlLst:
                if cntrlLst.count(flItm[2][:len(flItm[2]) - 4].replace('%', ' ')) != 0:
                    flLst.append('-'.join(flItm))
                    cntrlLst.remove(flItm[2][:len(flItm[2]) - 4].replace('%', ' '))
            if len(cntrlLst) != 0:
                self.logger.error("Error while loading collection for controllers: " + str(', '.join(cntrlLst)))
                return -1
            os.chdir(self.setPATH)
        else:
            flLst = ['pcklUnqNm_' + fPstfx + '-' + fl[4].replace(' ', '%') + '.txt' for fl in elmLst]
        flLst.sort()
        for flNm in flLst:
            try:
                with open('jmProj_dumps/'+ self._currDumpDir_ + '/' + flNm, 'rb') as fObj:
                    cllctn = pickle.load(fObj)
                fObj.close()
            except:
                self.logger.error("Error while loading collection from a file (" + flNm + "): " + str(sys.exc_info()[0]))
                return -1
            if len(cllctn) == 0:
                continue
            if fPstfx == "Cntrl":
                self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
                self._extrHostNode_(cllctn[0][0])
                tmpUppElm = [cntrl for cntrl in self._currNode_["hashTree"].findall(xSet[0]) if self._getNodeName_(cntrl) == cllctn[0][1]].pop(0)
            else:
                tmpUppElm = [k[0] for k in elmLst if self._getNodeName_(k[0]) == cllctn[0][0]].pop(0)
            self._setLocalRootNode_(tmpUppElm)
            self._appendXElmToCllctnItm_(cllctn)
            self._constrictBkpCl_()
            self.logger.info("Collection succesfully restored from file " + flNm)
        del cntrlLst
        del tmpFlLst
        del flLst
        return 0
        
## Метод дополнения элементов загруженной из файла коллекции соответствующим элементом (объектом) дерева

    def _appendXElmToCllctnItm_(self, rstrCl):
        self._currBkpCntrLst_.clear()
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        tmpLst = []
        for itm in rstrCl:
            self._extrHostNode_(itm[len(rstrCl[0])-1])
            tmpLst = [atr for atr in itm]
            tmpLst.insert(0, self._currNode_["elem"])
            itm = tuple(tmpLst)
            self._storeOrigXElm_(self, itm)
        del tmpLst
        
    def _getCurrNode_(self):
        node = self._currNode_
        return node
        
    def _constrictBkpCl_(self):
        for elm in self._currBkpCntrLst_:
            elm[0].attrib["testname"] = elm[len(self._currBkpCntrLst_[0])-2]

## Метод дополнения файлов дампа текущей датой
## !!! нужно сделать проверку при запуске на присутствие файлов с постфиксом текущей даты и что с ними делать

    def _sessDmpDir_(self, elmPstfx = 'deflt'):
        dtPostFx = self.dtPrefWithZero(self._currDate_.day) + self.dtPrefWithZero(self._currDate_.month) + str(self._currDate_.year)
        dtExstFlLst = [fl for fl in os.listdir('jmProj_dumps') if fl.find('dump_' + self.setFName.rpartition('.')[0] + '_' + dtPostFx) != -1]
        if len(dtExstFlLst) == 0:
            dtExstFlLst.append('empty_elem_0')
        dtExstFlLst.sort(key = lambda flNum: int(flNum.rpartition('_')[2]))
        lastDtFlNum = int(dtExstFlLst[len(dtExstFlLst)-1].rpartition('_')[2])
        self._currDumpDir_ = 'dump_' + self.setFName.rpartition('.')[0] + '_' + dtPostFx + '_' + str(lastDtFlNum + 1)
        os.mkdir('jmProj_dumps/' + self._currDumpDir_)
        self.logger.info("Working directory " + self.setPATH + "/jmProj_dumps/" + self._currDumpDir_ + " created")
        self._moveLogToDmp_()

## Метод добавляет нули, если месяц или число возвращаются одним символом (1, 4 и т.д.)

    def dtPrefWithZero(self, num):
        if len(str(num)) == 1:
            return '0' + str(num)
        return str(num)

		
## Метод сохранения xml-дерева в файл

    def xmlTreeToFile(self, flagUnq = True, info_msg = 'Коллекция успешно записана в файл'):
        try:
            if (flagUnq):
                self._xmlTree_.write(self.outFileUniqueNames)
                self.logger.info("File with unified xml-tree %s created", self.outFileUniqueNames)
            else:
                self._xmlTree_.write(self.outFileRestrdOrig)
                self.logger.info("File with original (restored) xml-tree %s created", self.outFileRestrdOrig)
            self._infoMsg_ = info_msg
        except Exception as e:
            self.logger.error('Error while saving XML-tree to file: ' + str(e) + '\n' + str(sys.exc_info()[0]))
            self._infoMsg_ = "Ошибка при сохранении XML-дерева"

            
### Здесь и далее до аналогичного комментария - попытка переписать метода под XML, названия попплывут для удобства

    def extrHTTPDataNamesAndLinks(self):
        self._linksToUpdate_ = tuple()
        self._curList_.clear()
        self._curLinkList_.clear()
        self.setFName = self.outFileUniqueNames
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('samplArgs_coll')
        xSet_2 = self._pumpUpXPathToBuild_('arg_NameAndValue')
        xSet_3 = self._pumpUpXPathToBuild_('samplPath')
        self._xTreeLocalRoot_ = self._xTreeRoot_.copy()
        self._extrThreadGroupNode_()
        thrGrIndx = [thgr[4] for thgr in self._thrGrpLst_].index(self._currThrGrNam_)
        self._setLocalRootNode_(self._thrGrpLst_[thrGrIndx][0])
        allTreeNodes = self._xTreeLocalRoot_["hashTree"].findall(xSet[0])
        allSmplElms = [elm for elm in allTreeNodes if self._checkElmTypeClls_(elm, 'HTTPSampler')]
        self._currBkpCntrLst_.clear()
        tmpLst = []
        ###
        tmpLst = [k for tmp in [i.findall(xSet_1[0]) for i in allSmplElms] for k in tmp if k.find(xSet_2[0]) is None]
        ##self._curList_.extend([s.find(xSet_2[0]).text for f in [i.findall(xSet_1[0]) for i in allSmplElms] for s in f if len(f)>0])
        self._curList_.extend([s.find(xSet_2[0]).text for f in [i.findall(xSet_1[0]) for i in allSmplElms] for s in f if len(f) > 0 if s .find(xSet_2[0]) is not None])
        ##self._curList_.extend([name for name in [s.find(xSet_2[0]) for f in [i.findall(xSet_1[0]) for i in allSmplElms] for s in f if len(f) > 0] if name is not None])
        ###
        self._curLinkList_.extend([j.find(xSet_3[0]).text for j in allSmplElms])
        tmpLst = self._delDublValsFrColl_(self._curList_)
        self._curList_.clear()
        self._curList_.extend(tmpLst)
        tmpLst = self._delDublValsFrColl_(self._curLinkList_)
        self._curLinkList_.clear()
        self._curLinkList_.extend(tmpLst)
        del tmpLst
        self.sbmDataDict = {x: [] for x in self._curList_}
        self.sbmActLinkDict = {a: [] for a in self._curLinkList_}
        self._curDict_ = self.sbmDataDict
        self._curLinkDict_ = self.sbmActLinkDict
        resDtTmp = []
        tmpLst = []
        tmpLinkLst = []
        for j in allSmplElms:
            self._currNode_["elem"] = j
            self._currNode_["hashTree"] = None
            smplrNm = self._getNodeName_(j)
            smplrCl = self._getNodeClass_(j)
            self._setNodeName_(j, 'someText_' + str(allSmplElms.index(j)))
            self._extrParntNodes_(self._currNode_["elem"])
            prntCntrlNm = self._getNodeName_(self._ancstNode_["elem"])
            self._storeOrigXElm_(j, prntCntrlNm, smplrCl, smplrNm, '--')
            tmpLinkLst = [self._curLinkDict_[p].append((prntCntrlNm, (smplrNm, None, 0))) for p in self._curLinkList_ if p==j.find(xSet_3[0]).text]
            jArgsLst = [l for l in j.findall(xSet_1[0]) if l.find(xSet_2[0]) is not None]
            if (len(jArgsLst) > 0):
                for z in jArgsLst:
                    tmpLst = [self._curDict_[k].append((prntCntrlNm, (smplrNm, z.find(xSet_2[1]).text, 0))) for k in
                              self._curList_ if k == z.find(xSet_2[0]).text]
            
        del tmpLst
        del resDtTmp
        del tmpLinkLst
        self._optimDataDict_()
        self._constrictBkpCl_()
        self._infoMsg_ = "Сгенерирована коллекция элементов для ThreadGroup\n---" + self._currThrGrNam_ + "---"
        self.logger.info("Working collection of elements accumulated")
###
            

## Метод заполнения струткуры 'sbmNamesLst'

    def extrSbmDataNames(self):
        sRegItmDatNam = self._pumpUpRegsToBuild_('extrSbmDataNames')
        self._extrSomeKeysFromFunc_(sRegItmDatNam[0], sRegItmDatNam[1])

## Метод заполнения структуры данных 'wbUrlParamLst'

    def extrWebUrlNames(self):
        sRegWebUrlDatPar = self._pumpUpRegsToBuild_('extrWebUrlNames')
        self._extrSomeKeysFromFunc_(sRegWebUrlDatPar[0], sRegWebUrlDatPar[1])

## Метод заполнения структуры данных 'refSbmNameList'

    def extrSbmRefNames(self):
        sRegSbmRefNam = self._pumpUpRegsToBuild_('extrSbmRefNames')
        self._extrSomeKeysFromFunc_(sRegSbmRefNam[0], sRegSbmRefNam[1])

## Метод заполнения структуры данных 'refWbNameLst'

    def extrWebRefNames(self):
        sRegWbRefNam = self._pumpUpRegsToBuild_('extrWebRefNames')
        self._extrSomeKeysFromFunc_(sRegWbRefNam[0], sRegWbRefNam[1])

## Вспомогательный метод для извлечения ключей из струткуры для различных функций

    def _extrSomeKeysFromFunc_(self, *regExps):
        self.setEntity(self.getEntity())
        resItmDat = ''
        tmpLst = []
        for t in self.scrFldLst:
            os.chdir('./' + t)
            fileObj = open("Action.c", 'r', encoding='utf-8')
            resItmDat = self._regBuild_((regExps[0], ''), reDtAll = True).findall(fileObj.read())
            fileObj.close()
            os.chdir('..')
            self._curList_.extend([s for f in [self._regBuild_((regExps[1],''), reDtAll=False).findall(i[1]) for i in resItmDat] for s in f])
            self._curLinkList_.extend([j[0] for j in resItmDat])
        del resItmDat
        tmpLst = self._delDublValsFrColl_(self._curList_)
        self._curList_.clear()
        self._curList_.extend(tmpLst)
        tmpLst = self._delDublValsFrColl_(self._curLinkList_)
        self._curLinkList_.clear()
        self._curLinkList_.extend(tmpLst)
        del tmpLst

## Вспомогательный метод для очищения повторяющихся значей в рабочих списках и списках данных функций

    def _delDublValsFrColl_(self, lstToUpd):
        lstToUpd.reverse()
        if len(lstToUpd) > 0:
            for m in lstToUpd:
                lstToUpd = [n for n in lstToUpd if n != m]
                lstToUpd.insert(0, m)
        return lstToUpd

## Вспомогательный метод для работы со словарями данных, параметер - тип C-функции

    def _makeDataDicts_(self, dctType):
        if dctType == 'web_submit_data':
            if len(self.sbmNamesLst) == 0:
                print(" !> Список имен 'sbmNamesLst' пуст, метод 'extrSbmDataNames' будет запущен. Займет время...")
                self.extrSbmDataNames()
            self.sbmDataDict = {x: [] for x in self.sbmNamesLst}
            self.sbmActLinkDict = {a: [] for a in self.sbmActLinkList}
        elif dctType == 'webSubmit_Ref':
            if len(self.refSbmNameList) == 0:
                print(" !> Список имен 'refSbmNameList' пуст, метод 'extrSbmRefNames' будет запущен. Займет время...")
                self.extrSbmRefNames()
            self.refSbmDataDict = {x: [] for x in self.refSbmNameList}
            self.refSbmLinkDict = {a: [] for a in self.refSbmLinkList}
        elif dctType == 'web_url':
            if len(self.wbUrlParamLst) == 0:
                print(" !> Спсиок URL-деталей 'wbUrlParamLst' пуст, метод 'extrWebUrlNames' будет запущен. Займет время...")
                self.extrWebUrlNames()
            self.wbUrlDatalDict = {y: [] for y in self.wbUrlParamLst}
            self.wbURLLinkDict = {b: [] for b in self.wbURLLinkList}
        elif dctType == 'webUrl_Ref':
            if len(self.refWbLinkList) == 0:
                print(" !> Спсиок URL-деталей 'refWbLinkList' пуст, метод 'extrWebRefNames' будет запущен. Займет время...")
                self.extrWebRefNames()
            self.refWbDataDict = {z: [] for z in self.refWbNameLst}
            self.refWbLinkDict = {b: [] for b in self.refWbLinkList}

## Метод заполнения словаря данных 'sbmDataDict'

    def extrSbmItemData(self):
        self._makeDataDicts_('web_submit_data')
        sRegFSbmDat = self._pumpUpRegsToBuild_('extrSbmItemData')
        self._extrSomeDataFromFunc_(sRegFSbmDat[0], lambda k: (sRegFSbmDat[1], k), (sRegFSbmDat[2], ''))

## Метод заполнения словаря данных 'wbUrlDatalDict'

    def extrWebUrlData(self):
        self._makeDataDicts_('web_url')
        sRegFUrlDat = self._pumpUpRegsToBuild_('extrWebUrlData')
        self._extrSomeDataFromFunc_(sRegFUrlDat[0], lambda k: (k, sRegFUrlDat[1]), ('', ''))

## Метод заполнения словаря данных 'refSbmDataDict'

    def extrSbmRefData(self):
        self._makeDataDicts_('webSubmit_Ref')
        sRegFSmbRefDat = self._pumpUpRegsToBuild_('extrSbmRefData')
        self._extrSomeDataFromFunc_(sRegFSmbRefDat[0], lambda k: (k, sRegFSmbRefDat[1]), ('', ''))

## Метод заполнения словаря данных 'refWbDataDict'

    def extrWebRefData(self):
        self._makeDataDicts_('webUrl_Ref')
        sRegFSmbRefDat = self._pumpUpRegsToBuild_('extrWebRefData')
        self._extrSomeDataFromFunc_(sRegFSmbRefDat[0], lambda k: (k, sRegFSmbRefDat[1]), ('', ''))

## Вспомогательный метод для извлечения данных по ключам из струткуры для различных функций

    def _extrSomeDataFromFunc_(self, *regExps):
        self.setEntity(self.getEntity())
        resDtTmp = []
        tmpLst = []
        tmpLinkLst = []
        regDtTmp = self._regBuild_((regExps[0], ''), reDtAll=True)
        for i in self.scrFldLst:
            os.chdir('./' + i)
            fileObj = open("Action.c", 'r', encoding='utf-8')
            resDtTmp = regDtTmp.findall(fileObj.read())
            fileObj.close()
            os.chdir('..')
            for j in resDtTmp:
                tmpLst=[(k,self._regExec_(self._regBuild_(regExps[1](k),regExps[2],reDtAll=False),j[2],1)) for k in self._curList_]
                [self._curDict_[l].append((i, (j[0], m[1]))) for l in self._curList_ for m in tmpLst if l==m[0] and m[1] != None]
                tmpLinkLst = [self._curLinkDict_[p].append((i, (j[0], None))) for p in self._curLinkList_ if p==j[1]]
        del tmpLst
        del resDtTmp
        del tmpLinkLst
        self._optimDataDict_()

## Вспомогательный метод оптимизации словарей данных (очищает повторяющиеся значения)

    def _optimDataDict_(self):
        b = []
        for a in self._curDict_:
            b = self._curDict_[a]
            self._curDict_[a] = [(c, tuple([d[1] for d in b if d[0] == c])) for c in list(set([e[0] for e in b]))]
        for a in self._curLinkDict_:
            b = self._curLinkDict_[a]
            self._curLinkDict_[a] = [(c, tuple([d[1] for d in b if d[0] == c])) for c in list(set([e[0] for e in b]))]
        del b

## Метод получения Сущности по значению (ссылка или параметр)
## !!!Внимание: может вернуть несколько сущностей

    def retEntityByVal(self, valToChk):
        retEntityVal = []
        if len([t for t in self.sbmNamesLst if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[2])
        if len([t for t in self.sbmActLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[2])
        if len([t for t in self.wbUrlParamLst if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[0])
        if len([t for t in self.wbURLLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[0])
        if len([t for t in self.refSbmNameList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[3])
        if len([t for t in self.refSbmLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[3])
        if len([t for t in self.refWbNameLst if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[1])
        if len([t for t in self.refWbLinkList if t==valToChk]) > 0:
            retEntityVal.append(self.entityNames[1])
        return retEntityVal

## Вспомогательный метод - возвращает позицию в списке, если ключ найден в неск. сущностях

    def _ifKeyNoneSinge_(self, key_link):
        if (len(self.retEntityByVal(key_link)) > 1) and (self.retEntityByVal(key_link)[0] != self.getEntity()):
            print(""" !> Значение ключа соответствует нескольким сущностям...
                Операция будет выполнена со значением текущей.
                Можно перевыполнить операцию, изменив сущность.
                При обновлении словаря внесите обратные изменения предыдущим значением.""")
            posInt = [self.retEntityByVal(key_link).index(q) for q in self.retEntityByVal(key_link) if q == self.getEntity()].pop(0)
        else:
            posInt = 0
        return posInt

## Метод для получения всех значений для заданного ключа(параметер или ссылка) в виде списка кортежей
## None значения для ссылок означают, что изменения для данных функций и скриптов не менялись
## Необходимо следить за значением 'Entity' перед запуском - может вернуть запись не из того словаря

    @valid_key
    def getDataDictItem(self, key_link):
        pos = self._ifKeyNoneSinge_(key_link)
        self.setEntity(self.retEntityByVal(key_link)[pos])
        tmpLst = self._curDict_.get(key_link)
        if tmpLst != None:
            return self._curDict_[key_link]
        else:
            return self._curLinkDict_[key_link]
        del tmpLst
        del pos

## Метод получения списка всех скриптов (с указанием названия функций при установленном флаге 'funcFlag')
## где используется, переданный в параметре, ключ 'keyName'

    @valid_key
    def getScrListByKey(self, key_link, funcFlag = True):
        pos = self._ifKeyNoneSinge_(key_link)
        self.setEntity(self.retEntityByVal(key_link)[pos])
        tmpLst = self._curDict_.get(key_link)
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
        else:
            wrkDict = self._curLinkDict_
        if funcFlag is False:
            return [k[0] for k in wrkDict[key_link]]
        else:
            return [(l[0], tuple([m[0] for m in l[1]])) for l in wrkDict[key_link]]
        del tmpLst
        del wrkDict
        del pos

## Метод получения списка всех скриптов (с указанием названия функций при установленном флаге 'funcFlag')
## где используется, переданный в параметре, ключ 'linkKey'

    def _getScrListByLink_(self, linkKey, funcFlag = True):
        if funcFlag is False:
            return [k[0] for k in self._curLinkDict_[linkKey]]
        else:
            return [(l[0], tuple([m[0] for m in l[1]])) for l in self._curLinkDict_[linkKey]]

## Метод получения списка всех скриптов (с указанием названия функций при установленном флаге 'funcFlag')
## где используется заданный ключ с определенным значением - вх. параметер '*keyValue' (картеж вида (key, value))

    @valid_key
    @valid_request_params
    def getScrFuncByKeyValue(self, *keyValue, funcFlag = True):
        k_val = keyValue[0]
        pos = self._ifKeyNoneSinge_(k_val[0])
        self.setEntity(self.retEntityByVal(k_val[0])[pos])
        tmpLst = self._curDict_.get(k_val[0])
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
        else:
            wrkDict = self._curLinkDict_
        tmpLst = [(n[0], tuple([p[0] for p in n[1] if p[1] == k_val[1]])) for n in wrkDict[k_val[0]]]
        if funcFlag is False:
            return [r[0] for r in tmpLst if len(r[1]) != 0]
        else:
            return [r for r in tmpLst if len(r[1]) != 0]
        del tmpLst
        del pos

## Метод получения значения по ключу, названию скрипта, названию функции - 
## вх. параметер '*keyScrFunc' (картеж вида (key, script, funcName))

    @valid_key
    @valid_request_params
    def getValueByKeyScrFunc(self, *keyScrFunc):
        k_s_f = keyScrFunc[0]
        pos = self._ifKeyNoneSinge_(k_s_f[0])
        self.setEntity(self.retEntityByVal(k_s_f[0])[pos])
        tmpLst = self._curDict_.get(k_s_f[0])
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
        else:
            wrkDict = self._curLinkDict_
        del pos
        return [fl for itm in [[(q[0], ((v),)) for v in q[1] if v[0]==k_s_f[2]] for q in wrkDict[k_s_f[0]] if q[0] == k_s_f[1]] for fl in itm]

    def getAllSbmFuncFromScr(self, scrName):
        return None

## Метод внесения изменений в словарь данных по ключу, названию скрипта, названию функции - 
## вх. параметер '*keyScrFunc' (картеж вида (key, script, funcName))
## новое значение - вх. параметер 'newVal'

    @valid_key
    def setValueByKeyScrFunc(self, newVal, *keyScrFunc):
        k_s_f = keyScrFunc[0]
        pos = self._ifKeyNoneSinge_(k_s_f[0])
        self.setEntity(self.retEntityByVal(k_s_f[0])[pos])
        tmpLst = self._curDict_.get(k_s_f[0])
        wrkDict = {}
        if tmpLst != None:
            wrkDict = self._curDict_
            k_s_f = [b for b in k_s_f]
            k_s_f.append('d')
            k_s_f = tuple(k_s_f)
        else:
            wrkDict = self._curLinkDict_
            k_s_f = [b for b in k_s_f]
            k_s_f.append('l')
            k_s_f = tuple(k_s_f)
        tmpScrInd = [wrkDict[k_s_f[0]].index(w) for w in wrkDict[k_s_f[0]] if w[0] == k_s_f[1]].pop(0)
        tmpFuncInd = [wrkDict[k_s_f[0]][tmpScrInd][1].index(x) for x in wrkDict[k_s_f[0]][tmpScrInd][1] if x[0]==k_s_f[2]].pop(0)
        tmpScrData = wrkDict[k_s_f[0]][tmpScrInd]
        tmpFuncData = wrkDict[k_s_f[0]][tmpScrInd][1]
        tmpFuncDataLst = [y for y in tmpFuncData]
        tmpFuncDataLst[tmpFuncInd] = (wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][0], newVal, 1)
        tmpFuncData = tuple(tmpFuncDataLst)
        del tmpFuncDataLst
        tmpScrDataLst = [z for z in tmpScrData]
        tmpScrDataLst[1] = tmpFuncData
        tmpScrData = tuple(tmpScrDataLst)
        del tmpScrDataLst
        wrkDict[k_s_f[0]][tmpScrInd] = tmpScrData
        del tmpFuncData
        del tmpScrData
        self.logger.info("New value = " + str(wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][:2]) + " set in controller '" + k_s_f[1] + "'")
        print("Новое значение = " + str(wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][:2]) + " установлено в контроллере '" + k_s_f[1] + "'")
        del tmpScrInd, tmpFuncInd
        del pos
        self._storeLinkFromSet_(k_s_f)

## Метод получения текущей рабочей сущности '_curEntity_'

    def getEntity(self):
        if self._curEntity_ == '':
            print(" !> Установите значение Entity - метод 'setEntity'")
        return self._curEntity_

## Метод установки текущей рабочей сущности '_curEntity_'

    def setEntity(self, entityName):
        if entityName not in ('webUrl_URL', 'webUrl_Ref', 'webSubmit_Item', 'webSubmit_Ref'):
            print(" !> Неверное имя сущности! Должно быть одно из списка:")
            print("    " + str(self.entityNames))
        else:
            self._curEntity_ = entityName
            if self._curEntity_ == 'webUrl_URL':
                self._curDict_ = self.wbUrlDatalDict
                self._curList_ = self.wbUrlParamLst
                self._curLinkList_ = self.wbURLLinkList
                self._curLinkDict_ = self.wbURLLinkDict
            elif self._curEntity_ == 'webUrl_Ref':
                self._curDict_ = self.refWbDataDict
                self._curList_ = self.refWbNameLst
                self._curLinkList_ = self.refWbLinkList
                self._curLinkDict_ = self.refWbLinkDict
            elif self._curEntity_ == 'webSubmit_Item':
                self._curDict_ = self.sbmDataDict
                self._curList_ = self.sbmNamesLst
                self._curLinkList_ = self.sbmActLinkList
                self._curLinkDict_ = self.sbmActLinkDict
            elif self._curEntity_ == 'webSubmit_Ref':
                self._curDict_ = self.refSbmDataDict
                self._curList_ = self.refSbmNameList
                self._curLinkList_ = self.refSbmLinkList
                self._curLinkDict_ = self.refSbmLinkDict

## Метод обновления файлов скриптов данными из временной структуры '_linksToUpdate_'

###
    def updateXMLTree(self):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        xSet_1 = self._pumpUpXPathToBuild_('samplArgs_coll')
        xSet_2 = self._pumpUpXPathToBuild_('arg_NameAndValue')
        xSet_3 = self._pumpUpXPathToBuild_('samplPath')
        xSet_4 = self._pumpUpXPathToBuild_('rootElemHashTree')
        if len(self._linksToUpdate_) != 0:
            set(self._linksToUpdate_)
            self._linksToUpdate_ = tuple(self._linksToUpdate_)
            for lnk in self._linksToUpdate_:
                self.setEntity(lnk[4])
                self._extrHostNode_(lnk[1])
                tmpLst = self._currNode_["hashTree"].findall(xSet[0])
                nestSmplrs = [elm for elm in tmpLst if self._checkElmTypeClls_(elm, 'HTTPSampler')]
                smplr = [smpl for smpl in nestSmplrs if self._getNodeName_(smpl) == lnk[2]].pop(0)
                if lnk[3] == 'd':
                    tstElmArgs = smplr.findall(xSet_1[0])
                    arg = [argN for argN in tstElmArgs if argN.find(xSet_2[0]).text == lnk[0]].pop(0)
                    strToInsert = self.getValueByKeyScrFunc(lnk)[0][1][0][1]
                    arg.find(xSet_2[1]).text = strToInsert
                    del tstElmArgs
                elif lnk[3] == 'l':
                    strToInsert = self.getValueByKeyScrFunc(lnk)[0][1][0][1]
                    smplr.find(xSet_3[0]).text = strToInsert
            del tmpLst
            del nestSmplrs
            del smplr
            self._linksToUpdate_ = tuple()
            self.logger.info("XML-tree successfully updated")
            self._infoMsg_ = "Текущее XML-дерево успешно обновлено"
        else:
            self.logger.info("Attempt to store empty list of changes to XML-tree")
            self._infoMsg_ = "Изменений в словаре не было - нечего обновлять"
        self._xTreeRoot_["elem"] = self._xmlTree_.getroot().find(xSet_4[0])
        self._xTreeRoot_["hashTree"] = self._xmlTree_.getroot().find(xSet_4[1])
            
    def wrtTreeToFile(self):
        self.xmlTreeToFile(True, "Коллекц. успешно запис. в файл\n---" + self.outFileUniqueNames + "---")
            
## Метод извлечения хранящихся строк для построение выражений XPath
            
    def _pumpUpXPathToBuild_(self, funcName=None):
        xAnyNode = './/*'
        xChldNodes = './'
        xChldNodesFltrd = './*'
        xAnyPropName = '[@testname="'
        xAnyPropClass = '[@testclass="'
        xAnyPropEndBrkts = '"]' 
        xReltvPrntNode = '/..'
        xAnyHashTree = './/hashTree'
        xChldHashTree = './hashTree'
        xNestNodesWithCls = './/*[@testclass][@testname]'
        xDirChldNodesWithCls = './*[@testclass][@testname]'
        xTestPlan = './/TestPlan'
        xThrdGrpNode = './/*[@testclass="ThreadGroup"]'
        xRootElem = './hashTree/TestPlan'
        xRootHashTree = './hashTree/hashTree'
        xSmplrArgs = './elementProp/collectionProp/'
        xArgName = './*[@name="Argument.name"]'
        xArgValue = './*[@name="Argument.value"]'
        xSmplrPath = './*[@name="HTTPSampler.path"]'

        if funcName == 'anyNode':
            return (xAnyNode, '')
        elif funcName == 'nodesWithName':
            return (xAnyPropName, xAnyPropEndBrkts)
        elif funcName == 'nodesWithClass':
            return (xAnyPropClass, xAnyPropEndBrkts)
        elif funcName == 'dirChldNode':
            return (xChldNodes, '')
        elif funcName == 'dirChldNodeFtlrd':
            return (xChldNodesFltrd, '')
        elif funcName == 'parntNode':
            return (xReltvPrntNode, '')
        elif funcName == 'all_nestNodes_cls':
            return (xNestNodesWithCls, xDirChldNodesWithCls)
        elif funcName == 'all_hashTrees':
            return (xAnyHashTree, xChldHashTree)
        elif funcName == 'TestPlan':
            return (xTestPlan, '')
        elif funcName == 'ThreadGroups':
            return (xThrdGrpNode, '')
        elif funcName == 'rootElemHashTree':
            return (xRootElem, xRootHashTree)
        elif funcName == 'samplArgs_coll':
            return (xSmplrArgs, '')
        elif funcName == 'arg_NameAndValue':
            return (xArgName, xArgValue)
        elif funcName == 'samplPath':
            return (xSmplrPath, '')
            
    def _getNodeName_(self, node):
        nodeName = None
        try:
            nodeName = node.attrib["testname"]
        except KeyError:
            nodeName = "no_Attribute"
            raise excpt.NodeAttributeError
        return nodeName
        
    def _setNodeName_(self, node, newVal):
        try:
            node.attrib["testname"] = newVal
        except KeyError:
            raise excpt.NodeAttributeError
            
    def _getNodeClass_(self, node):
        nodeClass = None
        try:
            nodeClass = node.attrib["testclass"]
        except KeyError:
            nodeClass = "no_Attribute"
            raise excpt.NodeAttributeError
        return nodeClass
        
## Метод сборки XPath 

    def _xPthBuild_(self, *cnctTpls):
        self._xPathUsrParam_.extend(['' for prm in range(abs(len(self._xPathUsrParam_)-len(cnctTpls)))])
        tmpLst = [k[0] + self._xPathUsrParam_.pop(0) + k[1] for k in cnctTpls]
        tmpStr = ''
        for xpPrt in tmpLst:
            tmpStr = tmpStr + xpPrt
        self._xPathUsrParam_.clear()
        del tmpLst
        return tmpStr

## Метод усечения названий сэмплеров

    def truncSmplrName(self):
        xSet = self._pumpUpXPathToBuild_('all_nestNodes_cls')
        tmpLst = [itm for itm in self._xTreeRoot_["hashTree"].findall(xSet[0]) if (self._checkElmTypeClls_(itm, "HTTPSampler"))]
        smplrCntErr = 0
        for smplr in tmpLst:
            try:
                origName = self._getNodeName_(smplr)
                newNameParts = urlpars.urlparse(origName)
                newNamePth = newNameParts.path.split('/')
                newName = newNamePth[len(newNamePth) - 1]
                smplr.attrib["testname"] = newName
            except:
                smplrCntErr += 1
                smplr.attrib["testname"] = newName
                self.logger.error("Truncating sampler name (%s) went wrong: " + str(sys.exc_info()[0]), origName)
        if smplrCntErr == 0:
            self.logger.info("Sampler names were succesfully truncated.")
        self._infoMsg_ = self._infoMsg_ + "\n--------"
        self._infoMsg_ = self._infoMsg_ + "\nПроизведено усечение назв. сэмплеров\n(признак = True)."
        if smplrCntErr != 0:
            self._infoMsg_ = self._infoMsg_ + "\n!!! ----"
            self._infoMsg_ = self._infoMsg_ + "\nОшибка при усечении назв. сэмплеров\n(всего " + str(smplrCntErr) + " ошибок)\nПодробнее в логе."
        del tmpLst
        
## Метод подсчета изменяемости значения параметров

    def calcVolatility(self):
        if len(self._curDict_.keys()) == 0:
            self._infoMsg_ = "Не сформирована коллекция.\nНеобходимо аккум. рабочую коллекц."
            return 0
        self.calcDictRes = {}
        tmpLst = []
        allVals = 0
        diffVals = 0
        isVolatile = None
        for key in self._curDict_.keys():
            tmpLst.clear()
            tmpLst = [smplr[1] for cntrl in self._curDict_[key] for smplr in cntrl[1]]
            allVals = len(tmpLst)
            diffVals = len(list(set(tmpLst)))
            if diffVals == 1:
                isVolatile = False
                self.calcDictRes[key] = (allVals, isVolatile)
            else:
                isVolatile = True
                if allVals != diffVals:
                    self.calcDictRes[key] = (abs(round(math.log(allVals) / math.log(diffVals/allVals), 2)), isVolatile)
                else:
                    devider = 1
                    divInt = 1
                    while (divInt > 0):
                        devider = devider * 10
                        divInt = allVals // devider
                    self.calcDictRes[key] = (abs(round(math.log(allVals ** allVals) / -(1 - allVals / devider), 2)), isVolatile)
        del tmpLst
        return 1
        
## Метод извлечения волатильности параметров из словаря

    def getVolatilParams(self):
        if self.calcVolatility() == 0:
            return 0
        tmpDct = {prm: val for prm, val in self.calcDictRes.items() if val[1] == self._ifVolatileParam_}
        if len(tmpDct.keys()) == 0:
            self._infoMsg_ = "Коллекция не содержит параметров\nс признаком волатильности = " + str(self._ifVolatileParam_)
            return 0
        tmpDct = {prm: val for prm, val in sorted(tmpDct.items(), key = lambda item: item[1][0], reverse = True)}
        self._infoMsg_ = "Сформирована статистика по параметрам;\nс признаком волатильности = " + str(self._ifVolatileParam_)
        return list(tmpDct.keys())
        
## Метод определения пользовательской правки параметров

    def editnIndicatInParams(self, key, controller = None, sampler = None):
        cntAll = 0
        cntEdtd = 0
        tmpLst = self.getDataDictItem(key)
        tmpIntersctLst = [itm for itm in tmpLst if itm[0] == controller]
        tmpLst = tmpIntersctLst if any(tmpIntersctLst) else tmpLst
        for cntrl in tmpLst:
            for smplr in cntrl[1]:
                if smplr[0] == sampler:
                    cntAll = 1
                    cntEdtd = smplr[2]
                    break
                cntAll += 1
                if smplr[2] == 1:
                    cntEdtd += 1
        try:
            res = cntEdtd / cntAll
            if res == 0:
                return "new"
            elif res == 1:
                return "edited"
            else:
                return "inProgress"
        except ZeroDivisionError:
            self.logger.error("Empty samplers list for controller. Check XML-tree.")
            raise excpt.NoneSamplersInController
            
        ##print(self.getDataDictItem(key))
>>>>>>> 8e8e3fed728e5fdc7c806ff5af614dda86b2f7f3
