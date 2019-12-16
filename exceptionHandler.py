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

import sys

class AppError(Exception):
    pass

class AppWarning(Warning):
    pass

class TkinterRuntimeExcept(AppError):
    def __init__(self, message):
        self.message = message

		
class ExceptHandler:

    def __init__(self):
        self.logger = None
        sys.excepthook = self._unhandledExcept_

    def tkinter_callback_except(self, exc, val, tb):
        raise TkinterRuntimeExcept("Reraised exception from tkinter mainloop")

    def _unhandledExcept_(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys._excepthook_(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("Exception", exc_info = (exc_type, exc_value, exc_traceback))
