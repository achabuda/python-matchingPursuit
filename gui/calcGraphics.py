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


class calcWindowUI(object):
    def setupUi(self, calcWindow):
        calcWindow.setObjectName(_fromUtf8("calcWindow"))
        calcWindow.setEnabled(True)
        calcWindow.resize(500 , 200)
        calcWindow.setMinimumSize(QtCore.QSize(500 , 200))
        calcWindow.setMaximumSize(QtCore.QSize(500 , 200))
        calcWindow.move(300,300)

# CENTRAL WIDGET:
        self.centralwidget = QtGui.QWidget(calcWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        layout = QtGui.QGridLayout()
        self.centralwidget.setLayout(layout)

        self.lbl_file = QtGui.QLabel()
        self.lbl_file.setObjectName(_fromUtf8("lbl_file"))
        layout.addWidget(self.lbl_file,0,0)

        self.prb_file = QtGui.QProgressBar()
        self.prb_file.setMinimum(0)
        layout.addWidget(self.prb_file,0,1)

        self.lbl_channel = QtGui.QLabel()
        self.lbl_channel.setObjectName(_fromUtf8("lbl_channel"))
        layout.addWidget(self.lbl_channel,1,0)

        self.prb_channel = QtGui.QProgressBar()
        self.prb_channel.setMinimum(0)
        layout.addWidget(self.prb_channel,1,1)

        self.lbl_trial = QtGui.QLabel()
        self.lbl_trial.setObjectName(_fromUtf8("lbl_trial"))
        layout.addWidget(self.lbl_trial,2,0)

        self.prb_trial = QtGui.QProgressBar()
        self.prb_trial.setMinimum(0)
        layout.addWidget(self.prb_trial,2,1)

        # self.prb_atom = QtGui.QProgressBar()
        # layout.addWidget(self.prb_atom,3,1)

        layout.setRowStretch(3, 1)
        
        self.btn_stop = QtGui.QPushButton()
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.btn_stop)
        hbox.addStretch(1)

        layout.addLayout(hbox,4,0,1,2)

        calcWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(calcWindow)
        QtCore.QMetaObject.connectSlotsByName(calcWindow)


    def retranslateUi(self, calcWindow):
        
        calcWindow.setWindowTitle(_translate("calcWindow", "python-MatchingPursuit -- calculations", None))

        self.btn_stop.setText(_translate("calcWindow", "Cancel", None))

        self.lbl_file.setText(_translate("calcWindow", "Files - (xx/xx)", None))
        self.lbl_channel.setText(_translate("calcWindow", "Channels - (xx/xx)", None))
        self.lbl_trial.setText(_translate("calcWindow", "Trials - (xx/xx)", None))

###################################################################################################################################################
###################################################################################################################################################

if __name__ == '__main__':
    print 'Using this class without it\'s functional parts may be possible, but'
    print 'it would be completely useless.'