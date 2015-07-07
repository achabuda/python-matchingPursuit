#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import division
import numpy as np

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

def gaussEnvelope(sigma , time):
    eps = 1e-4
    mi  = time[-1]/2
    x   = (mi - time) / sigma
    y   = np.exp(-1 * x**2 /2)
    ind = np.where(y>eps)[0]

    poczatek   = ind[0]
    koniec     = ind[-1]
    srodek     = (poczatek + koniec)/2 - poczatek + 1
    envelope   = y / np.linalg.norm(y)

    return (envelope , poczatek , koniec , srodek)