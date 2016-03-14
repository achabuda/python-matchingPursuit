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
from data.signalGenerator import loadSyntheticSigmalFromEEGLABFile
from src.processing       import calculateMP
from src.drawing          import calculateTFMap

import matplotlib.pyplot as plt
import numpy             as np

from matplotlib import gridspec, ticker
# from scipy.io   import savemat, loadmat


if __name__ == '__main__':
# load a synthetic signal
	nameOfFile    = '../matlab-fieldtripSimulations/simulationDataStruct.mat'
	(data , time , info) = loadSyntheticSigmalFromEEGLABFile(nameOfFile)
	
# config for a dictionary and MP
	flags = {}
	flags['useAsymA'] = 0
	flags['useRectA'] = 0
	flags['useGradientOptimization']  = 1
	
	config = {}
	config['flags']                            = flags
	config['algorithm']                        = 'mmp'
	config['trials2calculate']                 = range(info['numberOfTrials'])
	# config['channels2calculate']               = range(info['numberOfChannels'])
	config['channels2calculate']               = range(5)
	config['minS']                             = 100
	config['maxS']                             = info['numberOfSamples']
	config['density']                          = 0.01
	config['maxNumberOfIterations']            = 1
	config['minEnergyExplained']               = 0.99
	config['samplingFrequency']                = info['samplingFreq']
	config['minNFFT']                          = 1024

# optional config for t-f map drawing
	# config['mapFreqRange']    = [0.0 , samplingFrequency/2]
	# config['mapStructFreqs']  = [0.0 , samplingFrequency/2]
	# config['mapStructSigmas'] = [0.0 , 4.0]
	
	dictionary = generateDictionary(time , config)

	book       = calculateMP(dictionary , data , config)

