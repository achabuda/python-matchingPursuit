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

import numpy as np
import scipy.stats as scp


def generateTestSignal(gaborParams , sinusParams , asymetricWaveformsAParams , numberOfSamples , samplingFrequency , noiseRatio , silenceFlag = 1):
	'''
	gaborParams         - numpy array (as for gaborFunction) or None
	sinusParams         - numpy array of amplitude-frequency-phase trios or None
	asymetricWaveformsA - numpy array of  None
	noiseRatio  - float (0-1)
	'''
	time            = np.arange(0,1000)
	signal          = np.squeeze(np.zeros((numberOfSamples,1)))

	ind1 = 0
	if gaborParams is not None:
		for gabor in gaborParams:
			(tmp,time)  = gaborFunction(gabor)
			signal     += tmp
			ind1       += 1
	if silenceFlag == 0:
		print '{} gabors generated'.format(ind1)

	ind1 = 0
	if sinusParams is not None:
		for param in sinusParams:
			freq    = (param[1] / (0.5*samplingFrequency) ) * np.pi
			signal += np.array(param[0] * np.sin(freq * time + param[2]))
			ind1   += 1
	if silenceFlag == 0:
		print '{} sinusoids generated'.format(ind1)

	ind1 = 0
	if asymetricWaveformsAParams is not None:
		for asym in asymetricWaveformsAParams:
			amplitude = asym[0]
			freq      = asym[1] * 2 * np.pi
			pos       = asym[2]
			sigma     = asym[3]
			asymetry  = asym[4]
			x         = np.linspace(scp.lognorm.ppf(0.0001, asymetry),scp.lognorm.ppf(0.9999, asymetry), sigma)
			envelope  = scp.lognorm.pdf(x, asymetry)
			tmp       = np.squeeze(np.zeros((numberOfSamples,1)))
			tmp[pos:pos+sigma] = amplitude * envelope * np.cos(freq * x)
			
			signal += tmp
			ind1   += 1
	if silenceFlag == 0:
		print '{} asymmetrical waveforms generated'.format(ind1)

	return (signal , time)

def gaborFunction(params):
	'''
	params:numpy Array containing:
	numberOfSamples in [samples]
	samplingFreq    in [Hz]
	samplingFreq    in [Hz]
	width           in [s]
	position        in [s]
	amplitude       in [au]
	phase           in [rad]
	'''
	numberOfSamples = params[0]
	samplingFreq    = params[1]
	amplitude       = params[2]
	position        = params[3] * samplingFreq
	width           = params[4] * samplingFreq
	frequency       = (params[5] / (0.5*samplingFreq) ) * np.pi
	phase           = params[6]
	time            = np.arange(0,numberOfSamples)
	signal          = np.array(amplitude * np.exp(-np.pi*((time-position)/width)**2) * np.cos(frequency*(time-position)+phase))
	return (signal , time)

def defaultValues():
	numberOfSamples = 1000
	samplingFreq    = 250.0
	amplitude       = 12.0
	position1       = 3.0
	position2       = 1.0
	width           = 0.5
	frequency1      = 10.0
	frequency2      = 15.0
	phase           = 0.0

	gaborParams = np.array([[numberOfSamples,samplingFreq,amplitude,position1,width,frequency1,phase],[numberOfSamples,samplingFreq,amplitude,position2,width,frequency2,phase]])
	sinusParams = np.array([[5.0,5.0,0.0]])
	noiseRatio  = 0.0
	return (gaborParams , sinusParams , None , noiseRatio , samplingFreq , numberOfSamples)

def advancedValues():
	numberOfSamples = 1000
	samplingFreq    = 250.0
	amplitude1      = 12
	amplitude2      = 20
	freq1           = 5.0
	freq2           = 10.0
	pos1            = 250
	pos2            = 500
	sigma           = 500
	asymetry        = 0.45

	asymetricParams = np.array([[amplitude1,freq1,pos1,sigma,asymetry],[amplitude2,freq2,pos2,sigma,asymetry]])
	#asymetricParams = np.array([[amplitude1,freq1,pos1,sigma,asymetry]])
	sinusParams     = np.array([[2.0,5.0,0.0]])
	#sinusParams = None
	noiseRatio      = 0.0
	return(None , sinusParams , asymetricParams , noiseRatio , samplingFreq , numberOfSamples)

