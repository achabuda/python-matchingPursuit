#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
#    This file is part of Matching Pursuit Python program (python-MP).
#
#    python-MP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-MP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-MP. If not, see <http://www.gnu.org/licenses/>.

author: Tomasz Spustek
e-mail: tomasz@spustek.pl
University of Warsaw, July 06, 2015
'''

# libraries imports #
import os
import time
from platform import system
from functools import partial
from PyQt4 import QtCore, QtGui

# gui imports #
from settingsGraphics import mainWindowUI

# modules imports #
# from saveAndLoadModule import loadDefaultValues, setDefaultSettings, saveSettings, loadSettings
# from processingModule  import processFile


class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        
        print '#################'
        print 'Application start'
        print 'Window creating...'
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainWindowUI()
        self.ui.setupUi(self)
        print 'done'
