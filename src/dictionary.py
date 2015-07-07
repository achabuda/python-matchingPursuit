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

from scipy.optimize import fmin

def generateDictionary(time , params):
	'''
	params:dictionary - parameters
	minS - minimal sigma
	maxS - maximal sigma
	density - dictionary density
	
	time:list - original time vector
	'''

	time    = np.arange(1,3*len(time))

	minS    = params['minS']#    = 10
	maxS    = params['maxS']#    = 30
	density = params['density']# = 0.01

	sigma_start = (minS + maxS)/2
	(gc , p , k , sr) = gaussEnvelope(sigma_start , time)
	sigma_stop        = fmin(func=minSigEnerg , x0=sigma_start, args=(gc,density,time))

	print 'Start={}, stop={}'.format(sigma_start,sigma_stop)

def gaussEnvelope(sigma , time , shapeType=1):
	'''
	shapeTypes:int
	1 - standard gaussian shape
	2 - flatten on top
	'''
	eps = 1e-4
	mi  = time[-1]/2
	x   = (mi - time) / sigma

	if shapeType == 1:
		y = np.exp(-1 * x**2 /2)
	elif shapeType == 2:
		y = np.exp(-7 * x**8 /8)
	
	ind      = np.where(y>eps)[0]
	poczatek = ind[0]
	koniec   = ind[-1]
	srodek   = (poczatek + koniec)/2 - poczatek + 1
	envelope = y / np.linalg.norm(y)
	
	return (envelope , poczatek , koniec , srodek)

def minSigEnerg(testSigma , testEnvelope , density , time):
	(gx , p , k , sr) = gaussEnvelope(testSigma , time)
	return np.abs(1 - density - np.dot(gx , testEnvelope))

