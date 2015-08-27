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

from src.dictionary       import generateDictionary
from data.signalGenerator import generateTestSignal , simpleValues , advancedValues , masterValues
from src.processing       import calculateMP
from src.drawing          import calculateTFMap

import matplotlib.pyplot as plt
import numpy             as np

from matplotlib import gridspec, ticker
# from scipy.io   import savemat, loadmat


if __name__ == '__main__':
# create a synthetic signal
	
	(gaborParams , sinusParams , asymetricParams , rectParams , noiseRatio , samplingFrequency , numberOfSamples) = simpleValues()
	(signal,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,rectParams,numberOfSamples,samplingFrequency,noiseRatio)

	# (gaborParams , sinusParams , asymetricParams , rectParams , noiseRatio , samplingFrequency , numberOfSamples) = masterValues()
	# (signal,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,rectParams,numberOfSamples,samplingFrequency,noiseRatio)

# quick saving to matlab
	# tmp = {}
	# tmp['signal'] = signal
	# tmp['czas']   = time
	# savemat('../syg_asym.mat' , tmp)

# config for a dictionary and MP
	flags = {}
	flags['useAsymA'] = 1
	flags['useRectA'] = 1
	
	config = {}
	config['flags']                            = flags
	config['minS']                             = 32
	config['maxS']                             = numberOfSamples
	config['density']                          = 0.01
	config['maxNumberOfIterations']            = 4
	config['minEnergyExplained']               = 0.99
	config['samplingFrequency']                = samplingFrequency
	config['minNFFT']                          = 256 # 2*samplingFrequency
	config['flags']['useGradientOptimization'] = 1

# optional config for t-f map drawing
	# config['mapFreqRange']    = [0.0 , samplingFrequency/2]
	# config['mapStructFreqs']  = [0.0 , samplingFrequency/2]
	# config['mapStructSigmas'] = [0.0 , 4.0]
	
	dictionary = generateDictionary(time , config)
	book       = calculateMP(dictionary , signal , config)

# plot resulting functions
	plt.figure()
	plt.subplot(4,1,1)
	plt.plot(time,signal,'k')
	plt.plot(time,sum(book['reconstruction']).real , 'r')

	plt.subplot(4,1,2)
	plt.plot(time,book['reconstruction'][0].real , 'r')

	plt.subplot(4,1,3)
	plt.plot(time,book['reconstruction'][1].real , 'r')

	plt.subplot(4,1,4)
	plt.plot(time,book['reconstruction'][2].real , 'r')
	
	plt.show()

# draw standard t-f map
	(T,F,TFmap) = calculateTFMap(book,time,config['samplingFrequency'],0)

	gs = gridspec.GridSpec(3,1,height_ratios=[3,1,1])
		
	fig = plt.figure()

	ax0 = plt.subplot(gs[0])
	m   = ax0.imshow(np.abs(TFmap) , aspect='auto' , origin='lower' , extent=[0.0,numberOfSamples/samplingFrequency , 0.0,samplingFrequency/2])
	ax0.set_xlabel(r'Time [s]')
	ax0.set_ylabel(r'Frequency [Hz]')
	# ax0.set_ylim(config['mapFreqRange'])
	
	ax1 = plt.subplot(gs[1])
	ax1.plot(time,signal)
	ax1.set_xlabel(r'Time [s]')
	ax1.set_ylabel(r'Amplitude [uV]')

	ax2 = plt.subplot(gs[2])
	ax2.plot(time,book['reconstruction'].sum().real)
	ax2.set_xlabel(r'Time [s]')
	ax2.set_ylabel(r'Amplitude [uV]')

	fig.subplots_adjust(left=0.1, right=0.9)
	cbar_ax = fig.add_axes([0.92, 0.5, 0.02, 0.4])
	fig.colorbar(m, cax=cbar_ax)

	plt.show()

# draw complex t-f map
	(T,F,TFmap) = calculateTFMap(book,time,config['samplingFrequency'],1)

	fig = plt.figure()

	plt.subplot(3,1,1)
	m = plt.imshow(np.abs(TFmap) , aspect='auto' , origin='lower' , extent=[0.0,numberOfSamples/samplingFrequency , 0.0,samplingFrequency/2])
	
	plt.subplot(3,1,2)
	m_r = plt.imshow(TFmap.real , aspect='auto' , origin='lower' , extent=[0.0,numberOfSamples/samplingFrequency , 0.0,samplingFrequency/2])
	
	plt.subplot(3,1,3)
	m_i = plt.imshow(TFmap.imag , aspect='auto' , origin='lower' , extent=[0.0,numberOfSamples/samplingFrequency , 0.0,samplingFrequency/2])
	
	fig.subplots_adjust(left=0.1, right=0.9)
	cbar_ax = fig.add_axes([0.92, 0.5, 0.02, 0.35])
	fig.colorbar(m, cax=cbar_ax)
	cbar_ax = fig.add_axes([0.92, 0.1, 0.02, 0.35])
	fig.colorbar(m_r, cax=cbar_ax)

	plt.show()