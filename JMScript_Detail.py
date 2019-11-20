# coding: utf8

##Copyright (c) 2017 Лобов Евгений
## <ewhenel@gmail.com>
## <evgenel@yandex.ru>

## This file is part of LRScript_Detail.
##
##    LRScript_Detail is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    LRScript_Detail is distributed in the hope that it will be useful,
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
import re
import sys
import urllib
import datetime
import pickle
import xml.etree.ElementTree as ET

class JMScriptItems:

    """Get details from scripts"""

## Инициализация при создании объекта

    def __init__(self):
        self.setPATH = "/home/evgen/work"                   # Рабочая директория
        self.setDirMASK = '^uc[_0-9]+'                      # Маска для фильтра скриптов
        
        self.setFName = 'example.jmx'                       # Название .jmx файла, должно присутствовать в каталоге self.scrFlsLst  
        
        self.setClassDir = "/home/evgen/work/JM_proj_curr"       # Путь к директории с данным классом
        
        self._currDate_ = datetime.datetime.today()         # Текущая дата
        self._xmlTree_ = None                               # Полученное xml-дерево из файла скрипта JMeter
        self._xTreeRoot_ = None                             # Корневой элемент xml-дерева
        self._xTreeLocalRoot_ = None                        # Локальный корневой элемент xml-дерева, например для итериций внутри одной ThreadGroup
        self._thrGrpLst_ = []                               # Список ThreadGroup с названиями
        self._currThrGrNam_ = None                          # Имя выбранной ThreadGroup
        self._currBkpCntrLst_ = []                          # Список с указанием ориг. и изменных названий для дампа и восстановления названий нодов
        self._currDumpFName_ = None                         # Название файла для текущей коллекции
        self._currDumpDir_ = None                           # Название папки дампа сессии
        self.outFileUniqueNames = 'outputUnq.jmx'           # Файл для сохранения xml-дерева с уникальными названиями нодов (внутри ThreadGroup)
        self.outFileRestrdOrig = 'restoredOrig.jmx'         # Файл для восстановления xml-дерева с уникальными названиями нодов (внутри ThreadGroup)
        self._xPathUsrParam_ = []                           # ??Список пользовательских параметров для формирования xPath
        self._currNode_ = None                              # Текущий нод
        self._ancstNode_ = None                             # Нод предка
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
        self._selctdKey_ = None

        self._checkDmpDirExst_()                            # Проверка, что общий каталог для дампов существует
        
        print("\n\n* * * * JMScript_Details (ver. 1.3) * * * *")
        print("\n  * * * Класс для сбора и классификации данных сэмплеров JMeter * * *")
        print("\n\n                   Copyright (c) 2019 Лобов Евгений                    \n\n")

## Проверка что существует директория для дампов
    def _checkDmpDirExst_(self):
        tmpDmpDirLst = [dir for dir in os.listdir(self.setPATH) if dir == 'jmProj_dumps']
        if len(tmpDmpDirLst) == 0:
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
        tmpFlLst = []
        ifFExst = bool(len([f for f in self.scrFlsLst if f == self.setFName]) == 1)
        if (ifFExst):
            tree = ET.parse(self.setFName)            
        else:
            print(" !> Не найдено файлов по заданной маске, проверить можно тут 'setFName', или не та директория - тут'setPATH'")
            tree = None
        self._xmlTree_ = tree
        self._xTreeRoot_ = self._xmlTree_.getroot()

## Метод извлечения названий каталогов в директории setPATH

    def catchJMXFilesInPath(self):
        tmpLst = []
        os.chdir(self.setPATH)
        self.scrFlsLst = os.listdir('.')
        tmpLst = [f for f in self.scrFlsLst if f[len(f)-4:].find(".jmx")!=-1]
        self.scrFlsLst = tmpLst
        del tmpLst
        
## Метод получения струткуры нодов элементов класса Контроллер (точнее типа, Контроллеры различаются),
## а также генерация аналогичной с уникальными идентификаторами (Name).
## После окончания работы с основными (не вспомогательными) коллекциями 
## все ориг. названия можно восстановить из файлов дампа

    def xmlTreeStructToUnqNams(self):
        #self._xTreeLocalRoot_ = self._xTreeRoot_
        self._sessDmpDir_()
        self._extrThreadGroupNode_()
        self._extrCntrllNode_()
        self._currBkpCntrLst_ = self._thrGrpLst_.copy()
        #self._currDumpFName_ = 'pcklUnqNm' + self._appendDateToDmpFile_('TstPl')
        self._currDumpFName_ = 'pcklUnqNm_TstPl'
        self._dumpOrigCntrlNm_()
        try:
            self._xmlTree_.write(self.outFileUniqueNames)
        except:
            print('Ошибка при сохранении дерева: ' + str(sys.exc_info()[0]))
        
        

## Метод извлечения Нодов для всех элементов ThreadGroup

    def _extrThreadGroupNode_(self):
        self._xTreeLocalRoot_ = self._xTreeRoot_
        xSet = self._pumpUpXPathToBuild_('ThreadGroups')
        tmpNodeLst = self._xTreeLocalRoot_.findall(xSet[0])
        self._currBkpCntrLst_.clear()
        tmpThGrLst = tmpNodeLst.copy()
        self._xElmUniqueName_(tmpNodeLst, 'org.apache.jmeter.testelement.TestPlan')
        if len(self._currBkpCntrLst_) == 0:
            self._thrGrpLst_ = [tuple([thgr, '--', '--', '--', thgr.find(xSet[1]).text]) for thgr in tmpThGrLst]
            #print(self._thrGrpLst_)
        else:
            self._thrGrpLst_ = self._currBkpCntrLst_.copy()
        del tmpNodeLst
        del tmpThGrLst
        
## Метод проверки, что класс Нода относится к классу Controller
        
    def _checkIfxElmIsCntrll_(self, node):
        xSet = self._pumpUpXPathToBuild_('prop_nodeName')
        prop = node.find(xSet[0])
        tmpProp = prop.text.__str__()
        return bool(tmpProp.find('Controller')!=-1)
        #return bool(prop.text.find('Controller')!=-1)
        
## Метод, который будет использоваться вместо _checkIfxElmIsCntrll_
## достаточно вызова с параметром имени класса для проверки

    def _checkElmTypeClls_(self, node, ndClass=None):
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        fndClss = node.find(xSet[0])
        return bool(fndClss.text.find(ndClass)!=-1)
    
## Метод извлечения Нодов для всех элементов класса Controller для каждого элемента ThreadGroup

    def _extrCntrllNode_(self):
        tmpLst = []
        xSet = self._pumpUpXPathToBuild_('all_nestNodes')
        print(self._thrGrpLst_)
        tmpLst = [[itm for itm in thgr[0].findall(xSet[0]) if (self._checkIfxElmIsCntrll_(itm))] for thgr in self._thrGrpLst_]
        for ctLst in tmpLst:
            self._currBkpCntrLst_.clear()
            self._xTreeLocalRoot_ = self._thrGrpLst_[tmpLst.index(ctLst)][0]
            self._xElmNestedMapp_(ctLst, 'org.apache.jmeter.threads.ThreadGroup')
            self._xElmUniqueName_(ctLst, 'org.apache.jmeter.threads.ThreadGroup')
            ##self._currDumpFName_ = 'pcklUnqNm' + self._appendDateToDmpFile_('ThGr_' + str(tmpLst.index(ctLst) + 1))
            #self._currDumpFName_ = 'pcklUnqNm' + self._appendDateToDmpFile_('ThGr_' + str(tmpLst.count([])))
            self._currDumpFName_ = 'pcklUnqNm_ThGr_' + str(tmpLst.count([]))
            self._dumpOrigCntrlNm_()
        del tmpLst
    
## Метод создание префиксов для структуры составных вложенных элементов (для идентификации в коллекции)
        
    def _xElmNestedMapp_(self, cntrLst, parntNdClass):
        tmpVar = None
        tmpVarNew = None
        xSet = self._pumpUpXPathToBuild_('all_nestNodes')
        xSet_1 = self._pumpUpXPathToBuild_('nodeProps')
        for nd in cntrLst:
            tmpLst = [j for j in nd.findall(xSet[0]) if cntrLst[cntrLst.index(nd):].count(j)!=0]
            if len(tmpLst) != 0:
                for itm in tmpLst:
                    if (self._checkIfxElmIsCntrll_(itm)):
                        prop = itm.find(xSet[2])
                        tmpVar = prop.text
                        tmpVarNew = '_' + prop.text
                        prop.text = tmpVarNew
                        elmJmClass = itm.find(xSet[1]).text
                        self._extrParntNodes_(itm, parntNdClass)
                        prntNdName = self._ancstNode_.find(xSet_1[1]).text
                        self._storeOrigXElm_(itm, prntNdName, elmJmClass, tmpVar, tmpVarNew)
        del tmpLst
        del tmpVar
        del tmpVarNew

## Метод создание нумерации для структуры составных элементов (для идентификации в коллекции)

    def _xElmUniqueName_(self, revCntrLst, parntNdClass):
        tmpVar = None
        tmpVarNode = None
        tmpVarNew = None
        xSet = self._pumpUpXPathToBuild_('all_nestNodes')
        xSet_1 = self._pumpUpXPathToBuild_('nodeProps')
        bkpCntrLst = self._currBkpCntrLst_
        revCntrLst.reverse()
        tmpLst = [pr.find(xSet[2]).text for pr in revCntrLst]
        while(len(tmpLst)!=0):
            itm = tmpLst[0]
            itmCnt = tmpLst.count(itm)
            if itmCnt == 1:
                tmpLst.pop(0)
                revCntrLst.pop(0)
                continue
            while(itmCnt>0):
                itmIndx = tmpLst.index(itm)
                prop = revCntrLst[itmIndx].find(xSet[2])
                tmpVar = prop.text
                tmpVarNew = prop.text + '_' + str(itmCnt)
                prop.text = tmpVarNew
                elmJmClass = revCntrLst[itmIndx].find(xSet[1]).text
                self._extrParntNodes_(revCntrLst[itmIndx], parntNdClass)
                prntNdName = self._ancstNode_.find(xSet_1[1]).text
                self._storeOrigXElm_(revCntrLst[itmIndx], prntNdName, elmJmClass, tmpVar, tmpVarNew)
                tmpLst.pop(itmIndx)
                revCntrLst.pop(itmIndx)
                itmCnt = tmpLst.count(itm)
        del tmpLst
        del tmpVar
        del tmpVarNode
        del tmpVarNew
        ##bkpCntrLst.reverse()
        self._currBkpCntrLst_ = bkpCntrLst
        
## Метод получения родительских нодов 

    def _extrParntNodes_(self, node, upprNodeClass=None):
        self._currNode_ = node
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        ndName = self._currNode_.find(xSet[1]).text
        self._xPathUsrParam_.append(ndName)
        xSetStr = self._xPthBuild_(self._pumpUpXPathToBuild_('propText_allXElms'), self._pumpUpXPathToBuild_('parntNode'))
        self._ancstNode_ = self._xTreeLocalRoot_.find(xSetStr)
        while((upprNodeClass!=None) and (upprNodeClass!=self._ancstNode_.find(xSet[0]).text)):
            self._extrParntNodes_(self._ancstNode_, upprNodeClass)
            
## Метод извлечения хостового нода для свойств и т.д.

    def _extrHostNode_(self, prop):
        self._xPathUsrParam_.append(prop)
        xSetStr = self._xPthBuild_(self._pumpUpXPathToBuild_('propText_allXElms'), self._pumpUpXPathToBuild_('hostNode'))
        tmpVar = self._xTreeLocalRoot_.find(xSetStr)
        self._currNode_ = tmpVar
        del tmpVar
        
## Метод генерации уникальных идентификаторов для вложенных нодов и нодов с одинаковыми названиями
## метод запускает два метода _xElmNestedMapp_ и _xElmUniqueName_, возможно их удастся объединить в один (желательно)
    
    #def _xElmRunUniqNamMapp_(self, cntrLst, thGrName):
        #self._xElmNestedMapp_(cntrLst, thGrName)
        #isFWrtnErr = self._dumpOrigCntrlNm_(self._currBkpCntrLst_, self._currDumpFName_)
        #Вместо pass должна быть обработка события неуспешного дампа коллекции, и видимо восстановление из текущей коллекции и стоп !!!
        #if (isFWrtnErr):
        #    pass
        #self._xElmUniqueName_(cntrLst, thGrName)
        #isFWrtnErr = self._dumpOrigCntrlNm_(self._currBkpCntrLst_, self._currDumpFName_)
        #if (isFWrtnErr):
        #    pass

## Метод заполнения коллекции оригинальных элементов и их оригинальных названий

    def _storeOrigXElm_(self, *vals):
        if isinstance(vals[1], tuple):
            vals = tuple(vals[1])
        tmpLst = [itm[0] for itm in self._currBkpCntrLst_]
        tmpVar = []
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
                pickle.dump(self._currBkpCntrLst_, fObj)
            fObj.close()
            return False
        except:
            print('Ошибка при дампе коллекции: ' + str(sys.exc_info()[0]))
            return True

## Метод восстановления ориг. названий нодов из сохраненных в файлах коллекциях
        
    def restorOrigCntrlNm(self):
        ##Для чего-то были добавлены вызовы методов??
        ##self.catchJMXFilesInPath()
        ##self.getJMXFileAndMakeTree()
        self._extrThreadGroupNode_()
        self._restorOrigCntrlNm_(self._thrGrpLst_, 'ThGr')
        #self._xTreeLocalRoot_ = self._xTreeRoot_
        self._restorOrigCntrlNm_([(self._xTreeRoot_, 'Test_Plan')], 'TstPl')
        try:
            self._xmlTree_.write(self.outFileRestrdOrig)
        except:
            print('Ошибка при сохранении дерева: ' + str(sys.exc_info()[0]))
        
## Вспомогательный метод для загрузки коллекций из файлов и восстановления

    def _restorOrigCntrlNm_(self, elmLst, fPstfx):
        tmpElmNm = None 
        flLst = os.listdir('jmProj_dumps/' + self._currDumpDir_)
        xSet = self._pumpUpXPathToBuild_('all_nestNodes')
        tmpVar = len(elmLst)
        tmpLst = [fl for fl in flLst if fl.find('pcklUnqNm_' + fPstfx) != -1]
        tmpLst.sort()
        for flNm in tmpLst[len(tmpLst)-tmpVar:]:
            try:
                with open('jmProj_dumps/'+ self._currDumpDir_ + '/' + flNm, 'rb') as fObj:
                    cllctn = pickle.load(fObj)
                fObj.close()
            except:
                print('Ошибка при загрузке коллекции из файла: ' + str(sys.exc_info()[0]))
            if len(cllctn) == 0:
                continue
            tmpUppElm = [k[0] for k in elmLst if k[0].find(xSet[2]).text == cllctn[0][0]].pop(0)
            self._xTreeLocalRoot_ = tmpUppElm
            self._appendXElmToCllctnItm_(cllctn)
            self._constrictBkpCl_()
        del tmpVar
        del tmpLst
        
## Метод дополнения элементов загруженной из файла коллекции соответствующим элементом (объектом) дерева

    def _appendXElmToCllctnItm_(self, rstrCl):
        self._currBkpCntrLst_.clear()
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        tmpLst = []
        for itm in rstrCl:
            self._extrHostNode_(itm[len(rstrCl[0])-1])
            tmpLst = [atr for atr in itm]
            tmpElm = self._getCurrNode_()
            tmpLst.insert(0, tmpElm)
            itm = tuple(tmpLst)
            self._storeOrigXElm_(self, itm)
        del tmpLst
        
    def _getCurrNode_(self):
        node = self._currNode_
        return node
        
    def _constrictBkpCl_(self):
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        for elm in self._currBkpCntrLst_:
            elm[0].find(xSet[1]).text = elm[len(self._currBkpCntrLst_[0])-2]

## Метод дополнения файлов дампа текущей датой
## !!! нужно сделать проверку при запуске на присутствие файлов с постфиксом текущей даты и что с ними делать

    def _sessDmpDir_(self, elmPstfx = 'deflt'):
        dtPostFx = self.dtPrefWithZero(self._currDate_.day) + self.dtPrefWithZero(self._currDate_.month) + str(self._currDate_.year)
        #numOfExstFl = len([fl for fl in os.listdir('jmProj_dumps') if fl.find('_' + elmPstfx + '-' + dtPostFx) != -1])
        dtExstFlLst = [fl for fl in os.listdir('jmProj_dumps') if fl.find('dump_' + self.setFName.rpartition('.')[0] + '_' + dtPostFx) != -1]
        if len(dtExstFlLst) == 0:
            dtExstFlLst.append('empty_elem_0')
        dtExstFlLst.sort(key = lambda flNum: int(flNum.rpartition('_')[2]))
        lastDtFlNum = int(dtExstFlLst[len(dtExstFlLst)-1].rpartition('_')[2])
        self._currDumpDir_ = 'dump_' + self.setFName.rpartition('.')[0] + '_' + dtPostFx + '_' + str(lastDtFlNum + 1)
        os.mkdir('jmProj_dumps/' + self._currDumpDir_)

## Метод добавляет нули, если месяц или число возвращаются одним символом (1, 4 и т.д.)

    def dtPrefWithZero(self, num):
        if len(str(num)) == 1:
            return '0' + str(num)
        return str(num)
        
## Метод сохранения xml-дерева в файл
    
    def xmlTreeToFile(self, flagRstre = False):
        try:
            if (flagRstre):
                self.xmlTree.write(self.outFileUniqueNames)
            else:
                self.xmlTree.write(self.outFileRestrdOrig)
        except:
            print('Ошибка при сохранении дерева в файл: ' + + str(sys.exc_info()[0]))

            
### Здесь и далее до аналогичного комментария - попытка переписать метода под XML, названия попплывут для удобства

    def _setXElmText_(self, elm, txt = 'default'):
        
        xSet = self._pumpUpXPathToBuild_('nodeProps')
        elem = self._currNode_.find(xSet[1])
        elem.text = txt

    def extrHTTPDataNamesAndLinks(self):
        self.setFName = self.outFileUniqueNames
        self.catchJMXFilesInPath()
        self.getJMXFileAndMakeTree()
        xSet = self._pumpUpXPathToBuild_('all_nestNodes')
        xSet_1 = self._pumpUpXPathToBuild_('smplr_Path')
        xSet_2 = self._pumpUpXPathToBuild_('nestTestElm')
        xSet_3 = self._pumpUpXPathToBuild_('nestCollectn')
        xSet_4 = self._pumpUpXPathToBuild_('directChldNodes')
        xSet_5 = self._pumpUpXPathToBuild_('argmntName')
        xSet_6 = self._pumpUpXPathToBuild_('argmntValue')
        self._xTreeLocalRoot_ = self._xTreeRoot_
        self._extrThreadGroupNode_()
        thrGrIndx = [thgr[4] for thgr in self._thrGrpLst_].index(self._currThrGrNam_)
        self._xTreeLocalRoot_ = self._thrGrpLst_[thrGrIndx][0]
        allTreeNodes = self._xTreeLocalRoot_.findall(xSet[0])
        allSmplElms = [elm for elm in allTreeNodes if self._checkElmTypeClls_(elm, 'HTTPSampler')]
        self._currBkpCntrLst_.clear()
        tmpLst = []
        self._curList_.extend([s.find(xSet_5[0]).text for f in [i.find(xSet_2[0]).find(xSet_2[0]).find(xSet_3[0]).findall(xSet_4[0]) for i in allSmplElms] for s in f if len(f)>0])
        self._curLinkList_.extend([j.find(xSet_1[0]).text for j in allSmplElms])
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
            self._currNode_ = j
            prntSmplr = j.find(xSet[2])
            prntSmplrNm = prntSmplr.text
            prntSmplrCl = j.find(xSet[1]).text
            self._setXElmText_(j, 'someText' + str(allSmplElms.index(j)))
            prntThGr = self._extrParntNodes_(self._currNode_)
            prntThGrNm = self._ancstNode_.find(xSet[2]).text
            prntThGrCl = self._ancstNode_.find(xSet[1]).text
            self._storeOrigXElm_(j, prntThGrNm, prntSmplrCl, prntSmplrNm, prntSmplr.text)
            tmpLinkLst = [self._curLinkDict_[p].append((prntThGrNm, (prntSmplrNm, None))) for p in self._curLinkList_ if p==j.find(xSet_1[0]).text]
            jArgsLst = [l for l in j.find(xSet_2[0]).find(xSet_2[0]).find(xSet_3[0]).findall(xSet_4[0])]
            for z in jArgsLst:
                tmpLst=[self._curDict_[k].append((prntThGrNm, (prntSmplrNm,z.find(xSet_6[0]).text))) for k in self._curList_ if k == z.find(xSet_5[0]).text]
            
        del tmpLst
        del resDtTmp
        del tmpLinkLst
        self._optimDataDict_()
        self._constrictBkpCl_()
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

    def getDataDictItem(self, key_link):
        pos = self._ifKeyNoneSinge_(key_link)
        print(self.retEntityByVal(key_link))
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
        return [[v[1] for v in q[1] if v[0]==k_s_f[2]].pop(0) for q in wrkDict[k_s_f[0]] if q[0] == k_s_f[1]].pop(0)

    def getAllSbmFuncFromScr(self, scrName):
        return None

## Метод внесения изменений в словарь данных по ключу, названию скрипта, названию функции - 
## вх. параметер '*keyScrFunc' (картеж вида (key, script, funcName))
## новое значение - вх. параметер 'newVal'

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
        tmpFuncDataLst[tmpFuncInd] = (wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd][0], newVal)
        tmpFuncData = tuple(tmpFuncDataLst)
        del tmpFuncDataLst
        tmpScrDataLst = [z for z in tmpScrData]
        tmpScrDataLst[1] = tmpFuncData
        tmpScrData = tuple(tmpScrDataLst)
        del tmpScrDataLst
        wrkDict[k_s_f[0]][tmpScrInd] = tmpScrData
        del tmpFuncData
        del tmpScrData
        print("Новое значение = " + str(wrkDict[k_s_f[0]][tmpScrInd][1][tmpFuncInd]) + " установлено в скрипте '" + k_s_f[1] + "'")
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
            #regsFuncTxt_, regsItemTxt_ = (), ()
            xSet = self._pumpUpXPathToBuild_('all_nestNodes')
            xSet_0 = self._pumpUpXPathToBuild_('directChldNodes')
            xSet_1 = self._pumpUpXPathToBuild_('nestTestElm')
            xSet_2 = self._pumpUpXPathToBuild_('nestCollectn')
            xSet_3 = self._pumpUpXPathToBuild_('argmntName')
            xSet_4 = self._pumpUpXPathToBuild_('argmntValue')
            xSet_5 = self._pumpUpXPathToBuild_('smplr_Path')
            for lnk in self._linksToUpdate_:
                self.setEntity(lnk[4])
                self._extrHostNode_(lnk[1])
                tmpLst = self._currNode_.findall(xSet[0])
                nestSmplrs = [elm for elm in tmpLst if self._checkElmTypeClls_(elm, 'HTTPSampler')]
                if lnk[3] == 'd':
                    tstElmArgs = [s for f in [i.find(xSet_1[0]).find(xSet_1[0]).find(xSet_2[0]).findall(xSet_0[0]) for i in nestSmplrs] for s in f if len(f)>0]
                    valsLst = [argN for argN in tstElmArgs if argN.find(xSet_3[0]).text == lnk[0]]
                    strToInsert = self.getValueByKeyScrFunc(lnk)
                    print(strToInsert)
                    for val in valsLst:
                        val.find(xSet_4[0]).text = strToInsert
                    del tstElmArgs
                elif lnk[3] == 'l':
                    valsLst = [pth for pth in nestSmplrs if pth.find(xSet[2]).text == lnk[2]]
                    strToInsert = self.getValueByKeyScrFunc(lnk)
                    for val in valsLst:
                        val.find(xSet_5[0]).text = strToInsert 
            del tmpLst
            del nestSmplrs
            del valsLst
            self._linksToUpdate_ = tuple()
        else:
            print("Изменений в словаре не было - нечего обновлять")
            
    def wrtTreeToFile(self):
        self._xmlTree_.write(self.outFileUniqueNames)

###

    def updatFiles(self):
        if len(self._linksToUpdate_) != 0:
            set(self._linksToUpdate_)
            self._linksToUpdate_ = tuple(self._linksToUpdate_)
            regsFuncTxt_, regsItemTxt_ = (), ()
            for lnk in self._linksToUpdate_:
                self.setEntity(lnk[4])
                if lnk[3] == 'd':
                    regsFuncTxt_, regsItemTxt_ = self._pumpUpRegsToBuild_('updatFiles_d')
                elif lnk[3] == 'l':
                    regsFuncTxt_, regsItemTxt_ = self._pumpUpRegsToBuild_('updatFiles_f')
                else:
                    print("Тут ошибки")
                regFuncTxt = self._regBuild_((regsFuncTxt_[0], lnk[2]), (regsFuncTxt_[1], ''), reDtAll = True)
                regItemTxt = self._regBuild_((regsItemTxt_[0], lnk[0]), (regsItemTxt_[1], ''), reDtAll = True)
                os.chdir('./' + lnk[1])
                fileObj = open("Action.c", 'r', encoding='utf-8')
                fileTxt = fileObj.read()
                fileObj.close()
                resFuncTxt = regFuncTxt.search(fileTxt, re.M)
                coorFuncTxt = resFuncTxt.span()
                strFuncTxt = resFuncTxt.group(0)
                resItemTxt = regItemTxt.search(strFuncTxt)
                strToInsert = self.getValueByKeyScrFunc(lnk)
                coorStr = resItemTxt.span(1)
                strFuncTxt_ = strFuncTxt[:coorStr[0]] + strToInsert + strFuncTxt[coorStr[1]:]
                strScrTxt = fileTxt[:coorFuncTxt[0]] + strFuncTxt_ + fileTxt[coorFuncTxt[1]:]
                fileObj = open("Action.c", 'w', encoding='utf-8')
                fileObj.write(strScrTxt)
                fileObj.close()
                os.chdir('..')
            del fileTxt, strFuncTxt, strFuncTxt_
            del coorFuncTxt, coorStr
            del resFuncTxt, resItemTxt
            del strToInsert, strScrTxt
            self._linksToUpdate_ = tuple()
        else:
            print("Изменений в словаре не было - нечего обновлять")

## Метод извлечения хранящихся строк для построение рег. выражений

    def _pumpUpRegsToBuild_(self, funcName):
        sReFSbmt_1 = 'web_submit_data[(]["]' #web_submit_data[(]["].+?["]Action[=](.+?)["].+?ITEMDATA[,\s\n\t]+(.*?)LAST[)][;]Name=(.*?)["]
        sReFSbmt_2 = '["]Action[=](.+?)["]'
        sReFSbmt_3 = 'ITEMDATA[,\s\n\t]+(.*?)LAST[)][;]'
        sReFSbmt_4 = 'ITEMDATA[,\s\n]+.*?["]Name[=]'
        sRefSbmtVals_1 = 'Name=(.*?)["]'
        sRefSbmtVals_2 = '["]Name[=]'
        sRefSbmtVals_3 = '["][,] ["]Value[=](.*?)["]'
        sReFUrl_1 = 'web_url[(]["]'
        sReFUrl_2 = '["]URL[=](.+?)(?=["|?])'
        sReFUrl_3 = '[?]?(.*?)[",\s\t\n]+'
        sReFUrlParam_1 = '(?<=[?|&])(.+?)[=]'
        sReFUrlParam_2 = '(.*?)(?=[&]|$)'
        sRefSbmRef_1 = '["]Referer[=](.+?)(?=["|?])(.+?)[",\s\n\t]+$'
        sRefSbmRef_2 = '["]Referer[=](.+?)(?=["|?])'
        sReFComm_1 = '[,\s\n\t]+'
        sReFComm_2 = '.+?'
        sRefComm_3 = '(.+?)'
        sReHlp_1 = '^([А-Яа-яA-Za-z0-9\s]+?[(][\']' 
        sReHlp_2 = '[?][\'][)][:].+?)^\n'
        if funcName == 'extrSbmDataNames':
            return (sReFSbmt_1 + sReFComm_2 + sReFSbmt_2 + sReFComm_2 + sReFSbmt_3, sRefSbmtVals_1)
        elif funcName == 'extrWebUrlNames':
            return (sReFUrl_1 + sReFComm_2 + sReFUrl_2 + sReFComm_2 + sReFUrl_3, sReFUrlParam_1)
        elif funcName == 'extrSbmItemData':
            return (sReFSbmt_1+sRefComm_3+'["]'+sReFComm_1+'?'+sReFSbmt_2+sReFComm_2+sReFSbmt_3,sRefSbmtVals_2,sRefSbmtVals_3)
        elif funcName == 'extrWebUrlData':
            return (sReFUrl_1+sRefComm_3+'["]'+sReFComm_2+sReFUrl_2+sReFUrl_3, '[=]'+sReFUrlParam_2)
        elif funcName == 'extrSbmRefNames':
            return ('(?m)' + sReFSbmt_1 + sReFComm_2 + sRefSbmRef_2+sReFUrl_3, sReFUrlParam_1)
        elif funcName == 'extrSbmRefData':
            return ('(?m)'+sReFSbmt_1+sRefComm_3+'["]'+sReFComm_1+sReFComm_2+sRefSbmRef_2+sReFUrl_3, '[=]'+sReFUrlParam_2)
        elif funcName == 'extrWebRefNames':
            return ('(?m)'+ sReFUrl_1 + sReFComm_2 + sRefSbmRef_2+'[?]?(.*?)[,\s\t\n]+', sReFUrlParam_1)
        elif funcName == 'extrWebRefData':
            return ('(?m)'+sReFUrl_1+sRefComm_3+'["]'+sReFComm_1+sReFComm_2+sRefSbmRef_2+sReFUrl_3, '[=]'+sReFUrlParam_2)
        elif (funcName == 'updatFiles_d') and (self.getEntity() == 'webSubmit_Item'):
            return (sReFSbmt_1, sReFComm_2+sReFSbmt_3), (sReFSbmt_4, sRefSbmtVals_3+'[,][\s]ENDITEM[,]')
        elif (funcName == 'updatFiles_d') and (self.getEntity() == 'webUrl_URL'):
            return ('(?m)'+sReFUrl_1,'["]'+sReFComm_1+sReFUrl_2+sReFUrl_3+'$'),('(?<=[?|&])','[=](.*?)(?=[&|"])')
        elif (funcName == 'updatFiles_f') and (self.getEntity() == 'webSubmit_Item'):
            return (sReFSbmt_1, '["]'+sReFComm_1+sReFSbmt_2),('["]Action[=](', ')["]')
        elif (funcName == 'updatFiles_f') and (self.getEntity() == 'webUrl_URL'):
            return (sReFUrl_1, '["]'+sReFComm_1+sReFUrl_2), ('(?m)["]URL[=](', ')$')
        elif (funcName == 'updatFiles_d') and (self.getEntity() == 'webSubmit_Ref'):
            return ('(?m)' + sReFSbmt_1, '["]'+sReFComm_1+sReFComm_2+sRefSbmRef_2+sReFUrl_3), ('["]Referer'+sReFComm_2+'(?<=[?|&])','[=](.*?)(?=[&|"])')
        elif (funcName == 'updatFiles_f') and (self.getEntity() == 'webSubmit_Ref'):
            return ('(?m)'+sReFSbmt_1,'["]'+sReFComm_1+sReFComm_2+sRefSbmRef_2), ('["]Referer[=](', ')$')
        elif (funcName == 'updatFiles_d') and (self.getEntity() == 'webUrl_Ref'):
            return ('(?m)' + sReFUrl_1, '["]'+sReFComm_1+sReFComm_2+sRefSbmRef_2+sReFUrl_3), ('["]Referer'+sReFComm_2+'(?<=[?|&])','[=](.*?)(?=[&|"])')
        elif (funcName == 'updatFiles_f') and (self.getEntity() == 'webUrl_Ref'):
            return ('(?m)'+sReFUrl_1,'["]'+sReFComm_1+sReFComm_2+sRefSbmRef_2), ('["]Referer[=](', ')$')
        elif funcName == 'readDescript':
            return (lambda fl_: '(?m)'+sReHlp_1 + fl_, sReHlp_2)
        else:
            return None
            
## Метод извлечения хранящихся строк для построение выражений XPath

    def _pumpUpXPathToBuild_(self, funcName=None):
        xThrdGrpNode = './/*[@class="org.apache.jmeter.threads.ThreadGroup"]/..'
        xNodeName = './/testelement/*[@name="TestElement.name"]'
        xNodeClass = './/testelement/*[@name="TestElement.test_class"]'
        xNodePath = './/testelement/*[@name="HTTPSampler.path"]'
        xNestNodes = './/node'
        xTstElm = './/testelement'
        xCollctn = './/collection'
        xChldNodes = './*'
        xArgName = './*[@name="Argument.name"]'
        xArgValue = './*[@name="Argument.value"]'
        #parTstElem = root.find('.//*[property="__Simple Controller_1"]/../..')
        xAnyPropTxt_1 = './/*[property="'
        xAnyPropTxt_2 = '"]'
        xReltvPrntNode = '/../..'  
        xReltvHostNode = '/..' 
        if funcName == 'ThreadGroups':
            return (xThrdGrpNode, xNodeName)
        elif funcName == 'prop_nodeName':
            return (xNodeName,)
        elif funcName == 'all_nestNodes':
            return (xNestNodes, xNodeClass, xNodeName)
        elif funcName == 'nodeProps':
            return (xNodeClass, xNodeName)
        elif funcName == 'parntNode':
            return (xReltvPrntNode, '')
        elif funcName == 'hostNode':
            return (xReltvHostNode, '')
        elif funcName == 'propText_allXElms':
            return (xAnyPropTxt_1, xAnyPropTxt_2)
        elif funcName == 'smplr_Path':
            return (xNodePath, '')
        elif funcName == 'nestTestElm':
            return (xTstElm, '')
        elif funcName == 'nestCollectn':
            return (xCollctn, '')
        elif funcName == 'directChldNodes':
            return (xChldNodes, '')
        elif funcName == 'argmntName':
            return (xArgName, '')
        elif funcName == 'argmntValue':
            return (xArgValue, '')

## Метод генерации регулярного выражения из пар переданных картежом (*cnctTpls) вида ((a1, a2), (b2, b2), ...)

    def _regBuild_(self, *cnctTpls, reDtAll = False):
        tmpLst = [k[0]+k[1] for k in cnctTpls]
        tmpStr = ''
        if len(cnctTpls) > 1:
            for p in tmpLst:
                tmpStr = tmpStr + p
            if reDtAll == False:
                cmplReg = re.compile(tmpStr)
            else:
                cmplReg = re.compile(tmpStr, re.DOTALL)
        else:
            if reDtAll == False:
                cmplReg = re.compile(tmpLst.pop(0))
            else:
                cmplReg = re.compile(tmpLst.pop(0), re.DOTALL)
        del tmpLst
        return cmplReg
        
## 

    def _xPthBuild_(self, *cnctTpls):
        self._xPathUsrParam_.extend(['' for prm in range(abs(len(self._xPathUsrParam_)-len(cnctTpls)))])
        tmpLst = [k[0] + self._xPathUsrParam_.pop(0) + k[1] for k in cnctTpls]
        tmpStr = ''
        for xpPrt in tmpLst:
            tmpStr = tmpStr + xpPrt
        self._xPathUsrParam_.clear()
        del tmpLst
        return tmpStr
        

## Метод запуска выполнения регулярного выражения (re.search) с переданными в параметрах строкой и скомпилированным рег. выр.

    def _regExec_(self, cmpldReg, strToSearch, grFlagNum = None):
        regExecRes = cmpldReg.search(strToSearch)
        if regExecRes == None:
            return regExecRes
        elif regExecRes != None and grFlagNum != None:
            return regExecRes.group(grFlagNum)
        else:
            return regExecRes

## Метод для вызова описания класса и подсказок

    def readDescript(self, hlpPart = None):
        tmpPar = hlpPart
        os.chdir(self.setClassDir)
        fileObj = open('readMe.txt', 'r', encoding='utf-8')
        tmpStr = fileObj.read()
        fileObj.close()
        os.chdir(self.setPATH)
        if tmpPar == None:
            tmpPar = 'Dsc'
        regHlpFl = self._pumpUpRegsToBuild_('readDescript')
        tmpLst = [('Var','a'),('Ent','b'),('Stt','c'),('Mtd','d'),('DRc','e'), ('Rtn','f')]
        tmpLst.extend([('Dsc',None),('Dsc','g'),('Ful','h'), ('Nts', '')])
        tmpLst_ = [s[0] for s in tmpLst if s[1] == tmpPar]
        if len(tmpLst_) != 0:
            tmpPar = tmpLst_.pop(0)
        tmpLst_ = [s[0] for s in tmpLst if s[0] == tmpPar]
        if len(tmpLst_) != 0:
            tmpPar = tmpLst_.pop(0)
        else:
            tmpPar = 'Ful'
        if (tmpPar == 'Ful') or (tmpPar == 'g'):
            tmpPar = 'Dsc.+'
        resStr = self._regExec_(self._regBuild_((regHlpFl[0](tmpPar), regHlpFl[1]), reDtAll=True), tmpStr, grFlagNum=1)
        del tmpStr, resStr, tmpPar
        del tmpLst