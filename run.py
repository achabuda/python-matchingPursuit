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

from src.dictionary import gaussEnvelope, generateDictionary

import matplotlib.pyplot as plt
import numpy             as np


if __name__ == '__main__':

	time  = np.arange(1 , 1000)
	config = {}
	config['minS']    = 10
	config['maxS']    = 30
	config['density'] = 0.01

	flags = {}
	flags['useAsymA'] = 0
	flags['useRectA'] = 0

	config['flags']   = flags

	dictionary = generateDictionary(time , config)

	# print len(dictionary)

	# print dictionary[0]
	# print '----------------'
	# print dictionary[-1]

	# sigma = 10
	# (envelope , p , k , sr) = gaussEnvelope(sigma , time , 1)
	# plt.subplot(2,1,1)
	# plt.plot(time , envelope)

	# sigma = 100
	# (envelope , p , k , sr) = gaussEnvelope(sigma , time , 2)
	# plt.subplot(2,1,2)
	# plt.plot(time , envelope)

	# plt.show()