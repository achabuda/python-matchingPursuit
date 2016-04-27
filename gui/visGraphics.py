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


class visWindowUI(object):
    def setupUi(self, visWindow):
        visWindow.setObjectName(_fromUtf8("visWindow"))
        visWindow.setEnabled(True)
        # visWindow.resize(500 , 200)
        # visWindow.setMinimumSize(QtCore.QSize(500 , 200))
        # visWindow.setMaximumSize(QtCore.QSize(500 , 200))
        # visWindow.move(0,0)

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(visWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        layout = QtGui.QGridLayout()
        self.centralwidget.setLayout(layout)

    def retranslateUi(self, calcWindow):
        
        visWindow.setWindowTitle(_translate("visWindow", "python-MatchingPursuit -- visualiser", None))

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    print 'Using this class without it\'s functional parts may be possible, but'
    print 'it would be completely useless.'