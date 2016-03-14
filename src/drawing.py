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

from __future__ import division

import numpy             as np
import matplotlib.pyplot as plt
import pandas            as pd

from scipy.signal import resample
from scipy        import interpolate

from dictionary   import tukey


def plotIter(book,signal,time,number):
	plt.figure()
	plt.subplot(2,1,1)
	plt.plot(time,signal)
	plt.subplot(2,1,2)
	plt.plot(time,book['reconstruction'][number].real)
	plt.show()

def calculateTFMap(book,time,samplingFrequency,mapType,*argv):
	'''
	mapType:int
	- 0 - realvalued amplitude t-f map
	- 1 - comlex amplitude t-f map 
	'''
	if len(argv) == 2:
		mapStructFreqs  = argv[0]
		mapStructWidths = argv[1]
	else:
		mapStructFreqs  = [0.0 , samplingFrequency/2.0]
		mapStructWidths = [0.0 , 2 * time.shape[0]/samplingFrequency]

	mapFsize = 1000
	mapTsize = np.array([2000 , time.shape[0]]).min()

	if time.shape[0] > mapTsize:
		timeFinal = time[-1] * np.linspace(0,1,mapTsize) / samplingFrequency
	else:
		timeFinal = (time[-1] - time[0]) / samplingFrequency * np.linspace(0,1,mapTsize)

	print timeFinal.shape

	frequenciesFinal = samplingFrequency / 2 * np.linspace(0,1,mapFsize)

	if mapType == 0:
		timeFreqMap = np.zeros([frequenciesFinal.shape[0] , timeFinal.shape[0]])
	elif mapType == 1:
		timeFreqMap = np.zeros([frequenciesFinal.shape[0] , timeFinal.shape[0]] , dtype='complex')

	smoothingWindow = tukey(time.shape[0] , 0.1)

	for index, atom in book.iterrows():

		if (atom['freq'] >= mapStructFreqs[0] and atom['freq'] <= mapStructFreqs[1]) and (atom['width'] >= mapStructWidths[0] and atom['width'] <= mapStructWidths[1]):
			if mapType == 0:
				timeCourse = atom['reconstruction'][:].real
				signal2fft = timeCourse * smoothingWindow

				zz = np.fft.fft(signal2fft)
				z  = np.abs( zz[0 : np.floor(zz.shape[0]/2+1)] )
				z  = halfWidthGauss(z)

				if z.shape[0] > frequenciesFinal.shape[0]:
					z  = resample(z, frequenciesFinal.shape[0])
				else:
					x = np.arange(0, z.shape[0])
					f = interpolate.interp1d(x, z)
					z = f( np.arange(0, z.shape[0]-1 , (z.shape[0]-1)/frequenciesFinal.shape[0]) )

				z  = z / z.max()

				envelope = np.abs(atom['envelope']) * np.abs(atom['amplitude'])
				envelope = resample(envelope , timeFinal.shape[0])

				timeFreqMap += np.outer(z , envelope)

			elif mapType == 1:
				totalTimeCourse = atom['reconstruction'][:]
				
				signal2fft = totalTimeCourse * smoothingWindow
				zz = np.fft.fft(signal2fft)
				z  = np.abs( zz[0 : np.floor(zz.shape[0]/2+1)] )
				z  = halfWidthGauss(z)

				if z.shape[0] > frequenciesFinal.shape[0]:
					z  = resample(z, frequenciesFinal.shape[0])
				else:
					x = np.arange(0, z.shape[0])
					f = interpolate.interp1d(x, z)
					z = f( np.arange(0, z.shape[0]-1 , (z.shape[0]-1)/frequenciesFinal.shape[0]) )

				z  = z / z.max()

				timeFreqMap += np.outer(z , totalTimeCourse)

	return (timeFinal , frequenciesFinal , timeFreqMap)

def halfWidthGauss(z):
	mz  = z.max()
	mzi = z.argmax()

	ID  = np.where(z[0:mzi]-0.5*mz < 0)[0]
	if ID.shape[0] == 0:
		L = mzi
	else:
		L = mzi - ID[-1]

	ID = np.where(z[mzi:]-0.5*mz < 0)[0]
	if ID.shape[0] == 0:
		R = z.shape[0]
	else:
		R = ID[0]

	sigma = (L+R) / 2 / np.sqrt(np.log(4))
	t     = np.arange(1,z.shape[0])

	return mz * np.exp(-1*(t-mzi)**2 / 2 / (sigma**2))
