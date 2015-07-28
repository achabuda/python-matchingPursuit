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
from data.signalGenerator import generateTestSignal , defaultValues , advancedValues
from src.processing       import calculateMP
from src.drawing          import calculateTFMap

import matplotlib.pyplot as plt
import numpy             as np

from matplotlib import gridspec, ticker
from scipy.io   import savemat, loadmat


if __name__ == '__main__':
	# create a synthetic signal
	# (gaborParams , sinusParams , asymetricParams , noiseRatio , samplingFrequency , numberOfSamples) = defaultValues()
	# (signal1,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,numberOfSamples,samplingFrequency,noiseRatio)

	# (gaborParams , sinusParams , asymetricParams , noiseRatio , samplingFrequency , numberOfSamples) = advancedValues()
	# (signal,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,numberOfSamples,samplingFrequency,noiseRatio)

	#tmp = {}
	#tmp['signal'] = signal
	#tmp['czas']   = time
	#savemat('../syg_asym.mat' , tmp)

	data              = loadmat('../Jena-burstSupression/BSM_trials.mat')
	data              = data['bsm_gj_4s']
	samplingFrequency = 128.0
	time              = np.arange(0,4,1./samplingFrequency)

	# config for a dictionary
	flags = {}
	flags['useAsymA'] = 1
	flags['useRectA'] = 0
	config = {}
	config['flags']   = flags
	config['minS']    = 32
	config['maxS']    = 128
	config['density'] = 0.001
	# config for Matching Pursuit calculations
	config['maxNumberOfIterations']            = 20
	config['minEnergyExplained']               = 0.9999
	config['samplingFrequency']                = samplingFrequency
	config['minNFFT']                          = 256 # 2*samplingFrequency
	config['flags']['useGradientOptimization'] = 1
	
	dictionary = generateDictionary(time , config)

	#for ind1 in np.arange(0,data.shape[1]):
	for ind1 in [1,2,4]:#np.arange(0,10):
		signal      = data[:,ind1]
		book        = calculateMP(dictionary , signal , config)
		(T,F,TFmap) = calculateTFMap(book,time,config['samplingFrequency'])
		if ind1 == 1:
			maps = np.zeros(TFmap.shape)
		maps += TFmap

	maps = maps / ind1

	gs = gridspec.GridSpec(3,1,height_ratios=[3,1,1])#,width_ratios=[1,1,1]) 

	fig = plt.figure()#figsize=(8, 6))

	ax0 = plt.subplot(gs[0])
	ax0.imshow(maps,aspect='auto' , origin='lower' , extent=[0.0,4.0 , 0.0,64.0])
	ax0.set_xlabel(r'Time [s]')
	ax0.set_ylabel(r'Frequency [Hz]')
	#ax0.get_axes().xaxis.set_visible(False)
	#dupa = ticker.FuncFormatter(lambda x,pos: "{}".format(x/samplingFrequency))
	#ax0.get_axes().xaxis.set_major_formatter(dupa)

	ax1 = plt.subplot(gs[1])
	ax1.plot(time,signal)

	ax2 = plt.subplot(gs[2])
	ax2.plot(time,book['reconstruction'].sum().real)

	plt.tight_layout()


	#plt.figure()
	#plt.imshow(maps,extent=[0, 1, 0, 1])

	# plt.subplot(2,1,2)
	# plt.plot(signal,'k')
	# plt.plot(book['reconstruction'].real.sum() , 'r')

	plt.show()

	# plt.figure()
	# plt.subplot(2,1,1)
	# plt.plot(time,signal)
	
	# plt.subplot(2,1,2)
	# plt.plot(time , book['reconstruction'][13].real)
	# plt.show()

	# plt.subplot(5,1,3)
	# try:
	# 	plt.plot(time , book['reconstruction'][1].real)
	# except KeyError:
	# 	pass

	# plt.subplot(5,1,4)
	# try:
	# 	plt.plot(time , book['reconstruction'][2].real)
	# except KeyError:
	# 	pass

	# plt.subplot(5,1,5)
	# try:
	# 	plt.plot(time , book['reconstruction'][3].real)
	# except KeyError:
	# 	pass
	
	# plt.show()

