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
from scipy.io   import savemat, loadmat


if __name__ == '__main__':
	
	############################################################################
	######################## JENA ##############################################
	# data              = loadmat('../Jena-burstSupression/BSM_trials.mat')
	# subject           = 'bsm_gj_4s'
	# data              = data[subject]
	# samplingFrequency = 128.0
	# time              = np.arange(0,4,1./samplingFrequency)

	# config for a dictionary
	# flags = {}
	# flags['useAsymA'] = 1
	# flags['useRectA'] = 0
	# config = {}
	# config['flags']   = flags
	# config['minS']    = 32
	# config['maxS']    = 128
	# config['density'] = 0.001
	# # config for Matching Pursuit calculations
	# config['maxNumberOfIterations']            = 20
	# config['minEnergyExplained']               = 0.9999
	# config['samplingFrequency']                = samplingFrequency
	# config['minNFFT']                          = 256 # 2*samplingFrequency
	# config['flags']['useGradientOptimization'] = 1
	# # config for display
	# config['flags']['drawMeanMap']    = 1
	# config['flags']['saveMeanMap']    = 0

	# config['flags']['drawSingleMaps'] = 1
	# config['flags']['saveSingleMaps'] = 0
	
	# config['mapFreqRange']    = [0.0 , 16.0]
	# config['mapStructFreqs']  = [0.0 , 64.0]
	# config['mapStructSigmas'] = [0.0 , 4.0]

	# dictionary = generateDictionary(time , config)
	
	##########################################################
	##########################################################
	# results  = {}
	# arr      = np.arange(0,data.shape[1])
	# mask     = np.ones(arr.shape , dtype=bool)
	# # mask[80] = 0

	# ind2 = 0
	# for ind1 in arr[mask]:
	# 	ind2 += 1
	# 	print 'Calculation for {} trial:'.format(ind1)
	#  	signal      = data[:,ind1]
	#  	book        = calculateMP(dictionary , signal , config)
		
	#  	nameOfStruct     = 'trial_' + str(ind1)
	#  	results[nameOfStruct] = {col_name : book[col_name].values for col_name in book.columns.values}

	#  	(T,F,TFmap) = calculateTFMap(book,time,config['samplingFrequency'],config['mapStructFreqs'],config['mapStructSigmas'])
	#  	if ind2 == 1:
	#  		maps = np.zeros(TFmap.shape)
	#  	maps += TFmap
	 	
	#  	results[nameOfStruct]['mapM'] = TFmap
	#  	results[nameOfStruct]['mapT'] = time
	#  	results[nameOfStruct]['mapF'] = F


	#  	if config['flags']['drawSingleMaps'] == 1:
	#  		gs = gridspec.GridSpec(3,1,height_ratios=[3,1,1])
		
	# 		fig = plt.figure()

	# 		ax0 = plt.subplot(gs[0])
	# 		m   = ax0.imshow(TFmap,aspect='auto' , origin='lower' , extent=[0.0,4.0 , 0.0,64.0])
	# 		ax0.set_xlabel(r'Time [s]')
	# 		ax0.set_ylabel(r'Frequency [Hz]')
	# 		ax0.set_ylim(config['mapFreqRange'])
			
	# 		ax1 = plt.subplot(gs[1])
	# 		ax1.plot(time,signal)
	# 		ax1.set_xlabel(r'Time [s]')
	# 		ax1.set_ylabel(r'Amplitude [uV]')

	# 		ax2 = plt.subplot(gs[2])
	# 		ax2.plot(time,book['reconstruction'].sum().real)
	# 		ax2.set_xlabel(r'Time [s]')
	# 		ax2.set_ylabel(r'Amplitude [uV]')

	# 		fig.subplots_adjust(left=0.1, right=0.9)
	# 		cbar_ax = fig.add_axes([0.92, 0.5, 0.02, 0.4])
	# 		fig.colorbar(m, cax=cbar_ax)

	# 		if config['flags']['saveSingleMaps'] == 1:
	# 			nameOfOutputFile = '../Jena-burstSupression/' + subject + '_' + str(ind1) + '.png'
	# 			plt.savefig(nameOfOutputFile , bbox_inches = 'tight')
	# 			nameOfOutputFile = '../Jena-burstSupression/' + subject + '_' + str(ind1) + '.pdf'
	# 			plt.savefig(nameOfOutputFile , bbox_inches = 'tight')
	# 			plt.close()
	# 		else:
	# 			plt.show()

	# maps = maps / ind2

	# nameOfOutputFile = '../Jena-burstSupression/' + subject + '.mat'
	# savemat(nameOfOutputFile , results)

	# if config['flags']['drawMeanMap'] == 1:
	# 	gs = gridspec.GridSpec(2,1,height_ratios=[3,1])
	# 	fig = plt.figure()

	# 	ax0 = plt.subplot(gs[0])
	# 	m   = ax0.imshow(maps,aspect='auto' , origin='lower' , extent=[0.0,4.0 , 0.0,64.0])
	# 	ax0.set_xlabel(r'Time [s]')
	# 	ax0.set_ylabel(r'Frequency [Hz]')
	# 	ax0.set_ylim(config['mapFreqRange'])
			
	# 	ax1 = plt.subplot(gs[1])
	# 	for ind1 in arr[mask]:
	# 		signal = data[:,ind1]
	# 		ax1.plot(time,signal,'k')
	# 	ax1.plot(time,np.mean(data,1),'r')
	# 	ax1.set_xlabel(r'Time [s]')
	# 	ax1.set_ylabel(r'Amplitude [uV]')

	# 	fig.subplots_adjust(left=0.1, right=0.9)
	# 	cbar_ax = fig.add_axes([0.92, 0.5, 0.02, 0.4])
	# 	fig.colorbar(m, cax=cbar_ax)

	# 	if config['flags']['saveMeanMap'] == 1:
	# 		nameOfOutputFile = '../Jena-burstSupression/' + subject + '.png'
	# 		plt.savefig(nameOfOutputFile , bbox_inches = 'tight')
	# 		nameOfOutputFile = '../Jena-burstSupression/' + subject + '.pdf'
	# 		plt.savefig(nameOfOutputFile , bbox_inches = 'tight')
	# 		plt.close()
	# 	else:
	# 		plt.show()
	####################################################
	####################################################
	############# END OF JENA ##########################

	#####################################################################
	###### SIMULATIONS ##################################################
	
	# create a synthetic signal
	
	# (gaborParams , sinusParams , asymetricParams , noiseRatio , samplingFrequency , numberOfSamples) = simpleValues()
	# (signal1,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,numberOfSamples,samplingFrequency,noiseRatio)

	(gaborParams , sinusParams , asymetricParams , rectParams , noiseRatio , samplingFrequency , numberOfSamples) = masterValues()
	(signal,time) = generateTestSignal(gaborParams,sinusParams,asymetricParams,rectParams,numberOfSamples,samplingFrequency,noiseRatio)

	# quick saving to matlab
	#tmp = {}
	#tmp['signal'] = signal
	#tmp['czas']   = time
	#savemat('../syg_asym.mat' , tmp)

	# config for a dictionary
	flags = {}
	flags['useAsymA'] = 1
	flags['useRectA'] = 1
	
	config = {}
	config['flags']                            = flags
	config['minS']                             = 32
	config['maxS']                             = 1000
	config['density']                          = 0.01
	config['maxNumberOfIterations']            = 4
	config['minEnergyExplained']               = 0.99
	config['samplingFrequency']                = samplingFrequency
	config['minNFFT']                          = 256 # 2*samplingFrequency
	config['flags']['useGradientOptimization'] = 1
	
	dictionary = generateDictionary(time , config)
	book       = calculateMP(dictionary , signal , config)

	plt.figure()
	plt.subplot(5,1,1)
	plt.plot(time,signal,'k')
	plt.plot(time,sum(book['reconstruction']).real , 'r')

	plt.subplot(5,1,2)
	plt.plot(time,book['reconstruction'][0].real , 'r')

	plt.subplot(5,1,3)
	plt.plot(time,book['reconstruction'][1].real , 'r')

	plt.subplot(5,1,4)
	plt.plot(time,book['reconstruction'][2].real , 'r')

	plt.subplot(5,1,5)
	plt.plot(time,book['reconstruction'][3].real , 'r')
	
	plt.show()


	#plt.figure()
	#plt.imshow(maps,extent=[0, 1, 0, 1])

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

