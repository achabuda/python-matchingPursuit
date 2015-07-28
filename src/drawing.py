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

from scipy.signal import resample


def plotIter(book,signal,time,number):
	plt.figure()
	plt.subplot(2,1,1)
	plt.plot(time,signal)
	plt.subplot(2,1,2)
	plt.plot(time,book['reconstruction'][number].real)
	plt.show()

def calculateTFMap(book,time,samplingFrequency):
	mapFsize = 1000
	mapTsize = np.array([2000 , time.shape[0]]).min()

	if time.shape[0] > mapTsize:
		timeFinal = time[-1] * np.linspace(0,1,mapTsize) / samplingFrequency
	else:
		timeFinal = (time[-1] - time[0]) / samplingFrequency * np.linspace(0,1,mapTsize)

	frequenciesFinal = samplingFrequency / 2 * np.linspace(0,1,mapFsize)
	timeFreqMap      = np.zeros([frequenciesFinal.shape[0] , timeFinal.shape[0]])

	smoothingWindow = tukey(time.shape[0] , 0.1)

	for index, atom in book.iterrows():
		timeCourse = atom['reconstruction'][:].real
		signal2fft = timeCourse * smoothingWindow

		zz = np.fft.fft(signal2fft)
		z  = np.abs( zz[0 : np.floor(zz.shape[0]/2+1)] )
		z  = halfWidthGauss(z)
		z  = resample(z, frequenciesFinal.shape[0])   # = resample(z,finalFlen,length(z));
		z  = z / z.max()

		envelope = np.abs(atom['envelope'])
		envelope = resample(envelope , timeFinal.shape[0]) #= resample(env,finalTlen,length(env));

		timeFreqMap += np.outer(z , envelope)

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

def tukey(M, alpha=0.5, sym=True):
    '''
    We shoud just use scipy.signal.tukey from scipy 0.17+
    This is copied from there, sorry...
    '''
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, 'd')

    if alpha <= 0:
        return np.ones(M, 'd')
    elif alpha >= 1.0:
        return hann(M, sym=sym)

    odd = M % 2
    if not sym and not odd:
        M = M + 1

    n = np.arange(0, M)
    width = int(np.floor(alpha*(M-1)/2.0))
    n1 = n[0:width+1]
    n2 = n[width+1:M-width-1]
    n3 = n[M-width-1:]

    w1 = 0.5 * (1 + np.cos(np.pi * (-1 + 2.0*n1/alpha/(M-1))))
    w2 = np.ones(n2.shape)
    w3 = 0.5 * (1 + np.cos(np.pi * (-2.0/alpha + 1 + 2.0*n3/alpha/(M-1))))

    w = np.concatenate((w1, w2, w3))

    if not sym and not odd:
        w = w[:-1]
    return w