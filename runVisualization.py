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

from gui.visFunctions import visWindow
from PyQt4 import QtGui
import sys

def _pythonMatchingPursuitVisualizer(params):
    app = QtGui.QApplication(params)
    myapp = visWindow()
    myapp.show()
    return app.exec_()

if __name__ == "__main__":
    exit_code = _pythonMatchingPursuitVisualizer(sys.argv)
    sys.exit(exit_code)