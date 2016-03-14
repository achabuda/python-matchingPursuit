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

from PyQt4 import QtCore, QtGui
import time
from platform import system

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class mainWindowUI(object):
    ''' GUI graphical part for the main window.

    Class governing the graphical part of the default graphical user interface.
    It describes only parameters of used widgets, all operational functions
    are placed in separate class - gui_functional.

    '''

    def setupUi(self, mainWindow):

        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.setEnabled(True)
        mainWindow.resize(100, 100)
        mainWindow.setMinimumSize(QtCore.QSize(100, 100))
        mainWindow.setMaximumSize(QtCore.QSize(100, 100))
        # icon = QtGui.QIcon()
        # 
        # if system() == 'Windows':
        #     icon1path = _fromUtf8("./Pictures/settings.png")
        # else:
        #     icon1path = _fromUtf8("./Pictures/settings.svg")
        # 
        # icon.addPixmap(QtGui.QPixmap(icon1path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # mainWindow.setWindowIcon(icon)
        
        self.screenSize = QtGui.QDesktopWidget().screenGeometry()
        #print screenSize.width(), screenSize.height()

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))


# SET ALL THINGS UP:
        mainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        
        mainWindow.setWindowTitle(_translate("mainWindow", "python-MatchingPursui -- main window", None))

###################################################################################################################################################
###################################################################################################################################################


if __name__ == '__main__':
    print 'Using this class without it\'s functional part may be possible, but'
    print 'it would be completely useless.'
