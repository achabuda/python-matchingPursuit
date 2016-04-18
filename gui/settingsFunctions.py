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

# libraries imports #
import os
import time
import numpy as np
from platform  import system
from functools import partial
from os.path   import expanduser
from PyQt4     import QtCore, QtGui

# gui imports #
from settingsGraphics import mainWindowUI

# modules imports #
import data.dataLoader as dl
from src.utils      import determineAlgorithmConfig , determineDictionaryConfig , generateRangeFromString
from src.dictionary import generateDictionary

class mainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        
        print '#################'
        print 'Application starting'
        
        print 'Window creation...'
        QtGui.QWidget.__init__(self, parent)
        self.ui = mainWindowUI()
        self.ui.setupUi(self)
        print '- done'

        print 'Variables initialization...'
        self.initializeFlags()
        self.setVariablesState(0)
        print '- done'

        print 'Setting widgets initial states...'
        self.setWidgetsInitialState()
        print '- done'
        
        print 'Signals and slots connecting...'
        self.setConnections()
        print '- done'
        
        print 'Application started'
        print '###################'

# WIDGETS STATE
###############
    def setConnections(self):
        self.ui.lst_data.currentItemChanged.connect(self.selectData)

        self.ui.btn_settingsData.clicked.connect(self.resizeWindow)
        self.ui.btn_addData.clicked.connect(self.chooseDataFiles)
        self.ui.btn_removeData.clicked.connect(self.removeData)
        self.ui.btn_dictionarySave.clicked.connect(self.createDictionary)

        self.ui.led_samplingFrequency.textChanged.connect(self.samplingFrequencyChanged)
        self.ui.led_iterationsLimit.textChanged.connect(self.iterationsLimitChanged)
        self.ui.led_energyLimit.textChanged.connect(self.energyLimitChanged)
        self.ui.led_nfft.textChanged.connect(self.nfftChanged)
        self.ui.led_channels2calc.textChanged.connect(self.channelsRangeChanged)
        self.ui.led_trials2calc.textChanged.connect(self.trialsRangeChanged)
        self.ui.led_dictonaryDensity.textChanged.connect(self.dictionaryDensityChanged)
        self.ui.led_minS.textChanged.connect(self.minSValueChanged)
        self.ui.led_maxS.textChanged.connect(self.maxSValueChanged)

        self.ui.cmb_maxS.currentIndexChanged.connect(self.maxSUnitChanged)
        self.ui.cmb_minS.currentIndexChanged.connect(self.minSUnitChanged)

    def initializeFlags(self):
        self.flags = {}
        self.flags['groupBoxDataResized'] = 0

    def setVariablesState(self , flag):

        if flag == 0:
            if system() == 'Windows':
                # self.configFileName = os.path.expanduser("~") + '/_config/wordViewer_ng/configFile.txt'
                self.lineEnding     = '\n'
            else:
                # self.configFileName = os.path.expanduser("~") + '/.config/wordViewer_ng/configFile.txt'
                self.lineEnding     = '\r\n'

            self.informationTextColor = QtCore.Qt.green
            self.warrningTextColor    = QtCore.Qt.red
            self.standardTextColor    = QtCore.Qt.black

            self.warnings = {}
            self.warnings['wrongType']      = 'Wrong file type, in '
            self.warnings['openData_err_0'] = 'Wrong file type, in '
            self.warnings['openData_err_1'] = 'Field "data" was not found in the file '
            self.warnings['openData_err_2'] = 'Either "channels" or "trials" did not match the shape of "data", in '
            self.warnings['openData_err_3'] = 'Data matrix has more than three dimensions, in '
            self.warnings['openData_err_4'] = 'Duplicated input file - '

            self.warrningDisplayTime = 5000     # in [ms]

            self.filePath         = ''
            self.dataMatrixes     = {}
            self.dictionaryConfig = {}

    def setWidgetsInitialState(self):
        self.ui.groupBoxErrors.setHidden(True)

        algorithmTypes = {'smp':0 , 'mmp':1}
        keys = algorithmTypes.keys()
        for position in keys:
            self.ui.cmb_algorithmType.addItem(position)
        self.ui.cmb_algorithmType.setCurrentIndex(1)

        unitTypes = {'[samples]':0 , '[sec]':1}
        keys = unitTypes.keys()
        for position in keys:
            self.ui.cmb_minS.addItem(position)
            self.ui.cmb_maxS.addItem(position)
        self.ui.cmb_minS.setCurrentIndex(1)
        self.ui.cmb_maxS.setCurrentIndex(1)

        self.changeButtonsAvailability()

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerEvent)

    def setDataInfoControlls(self , config=[]):
        if config != []:
            self.ui.led_trials.setText(str(config['numberOfTrials']))
            self.ui.led_channels.setText(str(config['numberOfChannels']))
            self.ui.led_samples.setText(str(config['numberOfSamples']))
            self.ui.led_samplingFrequency.setText(str(config['samplingFreq']))
        else:
            self.ui.led_trials.setText('')
            self.ui.led_channels.setText('')
            self.ui.led_samples.setText('')
            self.ui.led_samplingFrequency.setText('')
    
    def setDataInfoConfig(self):
        config = {}
        config['numberOfTrials']   = int(self.ui.led_trials.text())
        config['numberOfChannels'] = int(self.ui.led_channels.text())
        config['numberOfSamples']  = int(self.ui.led_samples.text())
        config['samplingFreq']     = float(self.ui.led_samplingFrequency.text())
        return config

    def setAlgorithmControlls(self , config=[]):
        if config != []:
            self.ui.led_iterationsLimit.setText(str(config['iterationsLimit']))
            self.ui.led_energyLimit.setText(str(config['energyLimit']))
            self.ui.led_nfft.setText(str(config['nfft']))
            ind = self.ui.cmb_algorithmType.findText(config['algorithmType'])
            self.ui.cmb_algorithmType.setCurrentIndex(ind)
            self.ui.led_trials2calc.setText(config['trials2calc'])
            self.ui.led_channels2calc.setText(config['channels2calc'])
            self.ui.chb_displayInfo.setChecked(config['displayInfo'])
            self.ui.chb_useGradient.setChecked(config['useGradient'])
        else:
            self.ui.led_iterationsLimit.setText('')
            self.ui.led_energyLimit.setText('')
            self.ui.led_nfft.setText('')
            ind = self.ui.cmb_algorithmType.findText('smp')
            self.ui.cmb_algorithmType.setCurrentIndex(ind)
            self.ui.led_trials2calc.setText('')
            self.ui.led_channels2calc.setText('')
            self.ui.chb_displayInfo.setChecked(0)
            self.ui.chb_useGradient.setChecked(0)

    def setAlgorithmConfig(self):
        config = {}
        config['iterationsLimit'] = int(str(self.ui.led_iterationsLimit.text()))
        config['energyLimit']     = float(str(self.ui.led_energyLimit.text()))
        config['nfft']            = int(str(self.ui.led_nfft.text()))
        if self.ui.chb_displayInfo.isChecked():
            config['displayInfo'] = 1
        else:
            config['displayInfo'] = 0
        if self.ui.chb_useGradient.isChecked():
            config['useGradient'] = 1
        else:
            config['useGradient'] = 0
        config['algorithmType']   = str(self.ui.cmb_algorithmType.currentText())
        config['channels2calc']   = str(self.ui.led_channels2calc.text())
        config['channelsRange']   = generateRangeFromString(config['channels2calc'])
        config['trials2calc']     = str(self.ui.led_trials2calc.text())
        config['trialsRange']     = generateRangeFromString(config['trials2calc'])
        return config

    def setDictionaryControlls(self):
        self.ui.led_dictonaryDensity.setText(str(self.dictionaryConfig['dictionaryDensity']))
        self.ui.chb_useRect.setChecked(self.dictionaryConfig['useRect'])
        self.ui.chb_useAsym.setChecked(self.dictionaryConfig['useAsym'])
        
        ind = self.ui.cmb_maxS.findText('[samples]')
        self.ui.cmb_maxS.setCurrentIndex(ind)
        self.ui.led_maxS.setText(str(self.dictionaryConfig['maxS_samples']))

        ind = self.ui.cmb_minS.findText('[samples]')
        self.ui.cmb_minS.setCurrentIndex(ind)
        self.ui.led_minS.setText(str(self.dictionaryConfig['minS_samples']))

    def setDictionaryConfig(self):
        self.dictionaryConfig['dictionaryDensity'] = float(self.ui.led_dictonaryDensity.text())
        self.dictionaryConfig['useRect']           = int(self.ui.chb_useAsym.checkStateSet())
        self.dictionaryConfig['useAsym']           = int(self.ui.chb_useRect.checkStateSet())
        
        if str(self.ui.cmb_maxS.currentText()) == '[samples]':
            self.dictionaryConfig['maxS_samples']      = int(self.ui.led_maxS.text())
            self.dictionaryConfig['maxS_seconds']      = float(self.dictionaryConfig['maxS_samples'] / float(self.ui.led_samplingFrequency.text()))
        else:
            self.dictionaryConfig['maxS_seconds']      = float(self.ui.led_maxS.text())
            self.dictionaryConfig['maxS_samples']      = int(self.dictionaryConfig['maxS_seconds'] * float(self.ui.led_samplingFrequency.text()))

        if str(self.ui.cmb_minS.currentText()) == '[samples]':
            self.dictionaryConfig['minS_samples']      = int(self.ui.led_minS.text()) 
            self.dictionaryConfig['minS_seconds']      = float(self.dictionaryConfig['minS_samples'] / float(self.ui.led_samplingFrequency.text()))
        else:
            self.dictionaryConfig['minS_seconds']      = float(self.ui.led_minS.text())
            self.dictionaryConfig['minS_samples']      = int(self.dictionaryConfig['minS_seconds'] * float(self.ui.led_samplingFrequency.text()))

    def samplingFrequencyChanged(self):
        text = self.ui.led_samplingFrequency.text()
        try:
            sf = float(text)
            if sf > 0.0:
                freqs   = []
                for ind in range(self.ui.lst_data.count()):
                    path = str(self.ui.lst_data.item(ind).text())
                    freqs.append(self.dataMatrixes[path][1]['samplingFreq'])
                freqs = np.array(freqs)
                freqs = np.unique(freqs)
                if freqs.shape == (1L,) and freqs[0] == sf:
                    self.ui.led_samplingFrequency.setStyleSheet("color: rgb(0, 0, 0);")
                else:
                    self.ui.led_samplingFrequency.setStyleSheet("color: rgb(255, 0, 0);")
                    msg = 'Sampling Frequencies are not uniform!'
                    self.warrning('on' , msg , 3000)
            elif sf == 0.0:
                self.ui.led_samplingFrequency.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'Sampling Frequency can not be equal to 0[Hz]!'
                self.warrning('on' , msg , 3000)
            elif sf < 0.0:
                self.ui.led_samplingFrequency.setText(str(abs(sf)))
            self.changeButtonsAvailability()
        except ValueError:
            self.ui.led_samplingFrequency.setText(text[0:-1])

    def energyLimitChanged(self):
        text = self.ui.led_energyLimit.text()
        try:
            energy = float(text)
            if energy < 1.0 and energy > 0.0:
                self.ui.led_energyLimit.setStyleSheet("color: rgb(0, 0, 0);")
            elif energy >= 1.0:
                self.ui.led_energyLimit.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'It is impossible to explain more than 100 percent of a signal energy!'
                self.warrning('on' , msg , 3000)
            elif energy < 0.0:
                self.ui.led_energyLimit.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.led_energyLimit.setText(str(abs(energy)))
            elif energy == 0.0:
                self.ui.led_energyLimit.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'Explained signal energy should be greater than 0!'
                self.warrning('on' , msg , 3000)
            self.changeButtonsAvailability()
        except ValueError:
            self.ui.led_energyLimit.setText(text[0:-1])

    def iterationsLimitChanged(self):
        text = self.ui.led_iterationsLimit.text()
        try:
            iterations = int(text)
            if iterations > 0:
                self.ui.led_iterationsLimit.setStyleSheet("color: rgb(0, 0, 0);")
            elif iterations < 0:
                self.ui.led_iterationsLimit.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.led_iterationsLimit.setText(str(abs(iterations)))
            elif iterations == 0:
                self.ui.led_iterationsLimit.setStyleSheet("color: rgb(255, 0, 0);")
                msg = '# of iterations should be greater than 0!'
                self.warrning('on' , msg , 3000)
            self.changeButtonsAvailability()
        except ValueError:
            self.ui.led_iterationsLimit.setText(text[0:-1])

    def nfftChanged(self):
        text      = self.ui.led_nfft.text()
        nfftThres = 1<<(int(float(self.ui.led_samplingFrequency.text()))-1).bit_length()
        try:
            nfft = int(text)
            if nfft < 0:
                self.ui.led_nfft.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.led_nfft.setText(str(abs(nfft)))
            elif nfft == 0:
                self.ui.led_nfft.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'NFFT parameter should be greater than 0!'
                self.warrning('on' , msg , 3000)
            elif nfft > 0 and nfft < nfftThres:
                self.ui.led_nfft.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'NFFT parameter should be at least the next power of 2, greater than sampling frequency!'
                self.warrning('on' , msg , 3000)
            else:
                self.ui.led_nfft.setStyleSheet("color: rgb(0, 0, 0);")
            self.changeButtonsAvailability()
        except ValueError:
            self.ui.led_nfft.setText(text[0:-1])

    def channelsRangeChanged(self):
        text     = self.ui.led_channels2calc.text()
        possible = ['1','2','3','4','5','6','7','8','9','0',':',';','-',' ',',']
        if any(x not in possible for x in text):
            self.ui.led_channels2calc.setStyleSheet("color: rgb(255, 0, 0);")
            msg = 'Channels range contains incorrect characters!'
            self.warrning('on' , msg , 3000)
        else:
            self.ui.led_channels2calc.setStyleSheet("color: rgb(0, 0, 0);")
        self.changeButtonsAvailability()
            
    def trialsRangeChanged(self):
        text = self.ui.led_trials2calc.text()
        possible = ['1','2','3','4','5','6','7','8','9','0',':',';','-',' ']
        if any(x not in possible for x in text):
            self.ui.led_trials2calc.setStyleSheet("color: rgb(255, 0, 0);")
            msg = 'Trials range contains incorrect characters!'
            self.warrning('on' , msg , 3000)
        else:
            self.ui.led_trials2calc.setStyleSheet("color: rgb(0, 0, 0);")
        self.changeButtonsAvailability()

    def dictionaryDensityChanged(self):
        text = self.ui.led_dictonaryDensity.text()
        try:
            density = float(text)
            if density >= 1.0:
                self.ui.led_dictonaryDensity.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'Density of the dictionary should be less than 1.0!'
                self.warrning('on' , msg , 3000)
            elif density <= -1.0 or density == 0.0:
                self.ui.led_dictonaryDensity.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'Density of the dictionary should be greater than 0.0!'
                self.warrning('on' , msg , 3000)
            elif density < 0.0 and density > -1.0:
                self.ui.led_dictonaryDensity.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.led_dictonaryDensity.setText(str(abs(density)))
            else:
                self.ui.led_dictonaryDensity.setStyleSheet("color: rgb(0, 0, 0);")
            self.changeButtonsAvailability()
        except ValueError:
            self.ui.led_dictonaryDensity.setText(text[0:-1])

    def maxSValueChanged(self):
        text = self.ui.led_maxS.text()

        if str(self.ui.cmb_maxS.currentText()) == '[samples]':
            try:
                maxS = int(text)
            except ValueError:
                self.ui.led_maxS.setText(text[0:-1])
                return

            if str(self.ui.cmb_minS.currentText()) == '[samples]':
                minS = int(self.ui.led_minS.text())
            elif str(self.ui.cmb_maxS.currentText()) == '[sec]':
                minS = int(self.ui.led_minS.text()) * float(self.ui.led_samplingFrequency.text())
            else:
                return

        elif str(self.ui.cmb_maxS.currentText()) == '[sec]':
            try:
                maxS = float(text)
            except ValueError:
                self.ui.led_maxS.setText(text[0:-1])
                return

            if str(self.ui.cmb_minS.currentText()) == '[samples]':
                minS = int(self.ui.led_minS.text()) / float(self.ui.led_samplingFrequency.text())
            elif str(self.ui.cmb_maxS.currentText()) == '[sec]':
                minS = float(self.ui.led_minS.text())
            else:
                return

        if maxS > minS:
            if minS > 0:
                self.ui.led_minS.setStyleSheet("color: rgb(0, 0, 0);")

            if maxS > 0:
                self.ui.led_maxS.setStyleSheet("color: rgb(0, 0, 0);")
            elif maxS < 0:
                self.ui.led_maxS.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.led_maxS.setText(str(abs(maxS)))
            elif maxS == 0:
                self.ui.led_maxS.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'Width of structures in the dictionary should be greater than 0 [samples]!'
                self.warrning('on' , msg , 3000)
            self.changeButtonsAvailability()
        else:
            self.ui.led_maxS.setStyleSheet("color: rgb(255, 0, 0);")
            msg = 'Width of the widest structure in the dictionary should be greater than width of the most narrow one!'
            self.warrning('on' , msg , 3000)

    def minSValueChanged(self):
        text = self.ui.led_minS.text()

        if str(self.ui.cmb_minS.currentText()) == '[samples]':
            try:
                minS = int(text)
            except ValueError:
                self.ui.led_minS.setText(text[0:-1])
                return

            if str(self.ui.cmb_maxS.currentText()) == '[samples]':
                maxS = int(self.ui.led_maxS.text())
            elif str(self.ui.cmb_maxS.currentText()) == '[sec]':
                maxS = int(self.ui.led_maxS.text()) * float(self.ui.led_samplingFrequency.text())
            else:
                return

        elif str(self.ui.cmb_minS.currentText()) == '[sec]':
            try:
                minS = float(text)
            except ValueError:
                self.ui.led_minS.setText(text[0:-1])
                return

            if str(self.ui.cmb_maxS.currentText()) == '[samples]':
                maxS = int(self.ui.led_maxS.text()) / float(self.ui.led_samplingFrequency.text())
            elif str(self.ui.cmb_maxS.currentText()) == '[sec]':
                maxS = float(self.ui.led_maxS.text())
            else:
                return

        if minS < maxS:
            if maxS > 0:
                self.ui.led_maxS.setStyleSheet("color: rgb(0, 0, 0);")

            if minS > 0:
                self.ui.led_minS.setStyleSheet("color: rgb(0, 0, 0);")
            elif minS < 0:
                self.ui.led_minS.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.led_minS.setText(str(abs(minS)))
            elif minS == 0:
                self.ui.led_minS.setStyleSheet("color: rgb(255, 0, 0);")
                msg = 'Width of structures in the dictionary should be greater than 0 [samples]!'
                self.warrning('on' , msg , 3000)
            self.changeButtonsAvailability()
        else:
            self.ui.led_minS.setStyleSheet("color: rgb(255, 0, 0);")
            msg = 'Width of the widest structure in the dictionary should be greater than width of the most narrow one!'
            self.warrning('on' , msg , 3000)

    def maxSUnitChanged(self):
        if str(self.ui.cmb_maxS.currentText()) == '[samples]':
            try:
                tmp = float(str(self.ui.led_maxS.text()))
                tmp = tmp * float(str(self.ui.led_samplingFrequency.text()))
                tmp = int(tmp)
                self.ui.led_maxS.setText( str(tmp) )
            except ValueError:
                pass

        elif str(self.ui.cmb_maxS.currentText()) == '[sec]':
            try:
                tmp = int(str(self.ui.led_maxS.text())) / float(str(self.ui.led_samplingFrequency.text()))
                tmp = float(tmp)
                self.ui.led_maxS.setText( str(tmp) )
            except ValueError:
                pass


    def minSUnitChanged(self):
        if str(self.ui.cmb_minS.currentText()) == '[samples]':
            try:
                tmp = float(str(self.ui.led_minS.text()))
                tmp = tmp * float(str(self.ui.led_samplingFrequency.text()))
                tmp = int(tmp)
                self.ui.led_minS.setText( str(tmp) )
            except ValueError:
                pass

        elif str(self.ui.cmb_minS.currentText()) == '[sec]':
            try:
                tmp = int(str(self.ui.led_minS.text())) / float(str(self.ui.led_samplingFrequency.text()))
                tmp = float(tmp)
                self.ui.led_minS.setText( str(tmp) )
            except ValueError:
                pass

# WIDGETS BEHAVIOUR
##################
    def chooseDataFiles(self):
        # if self.ui.lst_data.count() > 0:
        #     self.dataMatrixes[self.filePath][2] = self.setAlgorithmConfig()
        #     self.dataMatrixes[self.filePath][1] = self.setDataInfoConfig()

        dialog = QtGui.QFileDialog.getOpenFileNames(self , 'Open data files' , expanduser('~') , 'All Files (*);;Matlab files (*.mat);;Python pickles (*.p)')
        if len(dialog) == 0:
            return
            
        warningCollector = ''
        for filePath in dialog:
            print filePath
            if filePath != '':

                if self.ui.lst_data.findItems(str(filePath) , QtCore.Qt.MatchExactly) != []:
                    warningCollector = warningCollector + self.warnings['openData_err_4'] + filePath + '\n'
                    continue
                
                self.displayInformation('Opening file '+ filePath + '. Please wait...' , 'new')
                if filePath[-4:] == '.mat' or filePath[-2:] == '.p':
                    (dataMatrix , dataInfo , message) = dl.loadSigmalFromFile(filePath)
                else:
                    warningCollector += self.warnings['wrongType'] + filePath + '\n'

                if message == 'ok':
                    self.addData(filePath , dataMatrix , dataInfo)
                else:
                    warningCollector += self.warnings['openData_'+message] + filePath + '\n'
            else:
                return

        if self.refreshSamplingFrequency() == 1:
            warningCollector += 'Sampling frequency is not uniform across all files!' + '\n'

        self.displayInformation('' , 'new')
        if warningCollector != '':
            self.warrning('on' , warningCollector)

        self.changeButtonsAvailability()

    def removeData(self):
        path = self.filePath

        item = self.ui.lst_data.currentItem()
        item = self.ui.lst_data.takeItem(self.ui.lst_data.currentRow())
        item = None
        del self.dataMatrixes[path]

        if self.ui.lst_data.count() < 1:
            if self.flags['groupBoxDataResized'] == 1:
                self.resizeWindow()
            self.filePath = ''
        else:
            self.filePath = str(self.ui.lst_data.currentItem().text())
            self.refreshSamplingFrequency()

        self.changeButtonsAvailability()

    def selectData(self):
        try:
            if self.ui.led_iterationsLimit.text() != '':
                # means in fact, that there are fields loaded into gui
                # print self.ui.led_nfft.text()

                self.dataMatrixes[self.filePath][2] = self.setAlgorithmConfig()
                self.dataMatrixes[self.filePath][1] = self.setDataInfoConfig()

            self.filePath = str(self.ui.lst_data.currentItem().text())
            self.setDataInfoControlls(self.dataMatrixes[self.filePath][1])
            self.setAlgorithmControlls(self.dataMatrixes[self.filePath][2])

            self.refreshSamplingFrequency()

        except AttributeError:
            # means that list is empty, or nothing is selected
            self.setDataInfoControlls()
            self.setAlgorithmControlls()
            self.filePath = ''
        
    def changeButtonsAvailability(self):
        if len(self.dataMatrixes) > 0:
            self.ui.btn_settingsData.setEnabled(True)
            self.ui.btn_removeData.setEnabled(True)
            self.ui.btn_calculate.setEnabled(True)
            self.ui.btn_dictionarySave.setEnabled(True)
        else:
            self.ui.btn_calculate.setEnabled(False)
            self.ui.btn_settingsData.setEnabled(False)
            self.ui.btn_saveSelectedBooks.setEnabled(False)
            self.ui.btn_openVisualisationTool.setEnabled(False)
            self.ui.btn_dictionarySave.setEnabled(False)
            self.ui.btn_removeData.setEnabled(False)

    def refreshSamplingFrequency(self):
        freqs   = []
        for ind in range(0 , self.ui.lst_data.count()):
            path = str(self.ui.lst_data.item(ind).text())
            freqs.append(self.dataMatrixes[path][1]['samplingFreq'])
        freqs = np.array(freqs)
        freqs = np.unique(freqs)
        if freqs.shape == (1L,):
            self.ui.led_samplingFrequency.setStyleSheet("color: rgb(0, 0, 0);")
            self.warrning('off')
            return 0
        else:
            self.ui.led_samplingFrequency.setStyleSheet("color: rgb(255, 0, 0);")
            msg = 'Sampling Frequencies are still not uniform!'
            self.warrning('on' , msg , 3000)
            return 1

    def displayInformation(self , text , flag='new'):
        # possible flags: new, add, remove_last
        palette = QtGui.QPalette()
        if text == '':
            self.ui.lbl_errors.setText('')
            palette.setColor(QtGui.QPalette.Foreground, self.warrningTextColor)
            self.ui.lbl_errors.setPalette(palette)
            self.ui.groupBoxErrors.hide()
        else:
            palette.setColor(QtGui.QPalette.Foreground, self.informationTextColor)
            self.ui.lbl_errors.setPalette(palette)
            if flag == 'new':
                self.ui.lbl_errors.setText(text)
                self.ui.groupBoxErrors.show()
            elif flag == 'add':
                newtext = self.ui.lbl_errors.text() + ' ' + text
                self.ui.lbl_errors.setText(newtext)
            elif flag == 'remove_last':
                t1 = self.ui.lbl_errors.text().find(' ')
                newtext = self.ui.lbl_errors.text()[0:t1]
                self.ui.lbl_errors.setText(newtext)
        QtGui.QApplication.instance().processEvents()   # Important!

    def warrning(self , flag='off' , errorMsg='' , time=0):
        if time == 0:
            time = self.warrningDisplayTime

        if flag == 'on':
            if self.timer.isActive():
                self.timer.stop()
            palette = QtGui.QPalette()
            self.ui.lbl_errors.setText(errorMsg)
            palette.setColor(QtGui.QPalette.Foreground, self.warrningTextColor)
            self.ui.lbl_errors.setPalette(palette)
            self.ui.groupBoxErrors.show()
            self.timer.start(time)
        elif flag == 'off':
            self.timer.stop()
            self.ui.lbl_errors.setText('')
            self.ui.groupBoxErrors.hide()
        QtGui.QApplication.instance().processEvents()   # Important!

### PROCESSING EVENTS:
######################
    def createDictionary(self):
        pass
        # dictionary = generateDictionary(time , config)

    def addData(self , filePath , dataMatrix , dataInfo):
        filePath = str(filePath)

        algorithmConfig       = determineAlgorithmConfig(dataInfo)
        self.dictionaryConfig = determineDictionaryConfig(self.dictionaryConfig , algorithmConfig['energyLimit'] , dataInfo)

        self.dataMatrixes[filePath] = [dataMatrix , dataInfo , algorithmConfig]
        
        self.setDictionaryControlls()
        # self.setAlgorithmControlls(algorithmConfig)
        # self.setDataInfoControlls(dataInfo)

        item = QtGui.QListWidgetItem(filePath)
        self.ui.lst_data.addItem(item)
        self.ui.lst_data.setCurrentItem(item)
        self.filePath = filePath

    def timerEvent(self):
        self.warrning('off')


# ANIMATIONS AND WINDOW RESIZING
################################
    def resizeWindow(self):

        animationDuration = 750     # in [ms]

    	self.animation = QtCore.QParallelAnimationGroup(self)
    	self.animation.finished.connect(self.setProperWindowSize)

    	self.animationWindow = QtCore.QPropertyAnimation(self, "size")
        self.animationWindow.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationWindow.setDuration(animationDuration)

        self.animationGroupBoxBooks = QtCore.QPropertyAnimation(self.ui.groupBoxBooks, "geometry")
        self.animationGroupBoxBooks.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxBooks.setDuration(animationDuration)        

        self.animationGroupBoxDataInfo = QtCore.QPropertyAnimation(self.ui.groupBoxDataInfo, "size")
        self.animationGroupBoxDataInfo.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxDataInfo.setDuration(animationDuration)

        self.animationGroupBoxAlgorithm = QtCore.QPropertyAnimation(self.ui.groupBoxAlgorithm, "size")
        self.animationGroupBoxAlgorithm.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxAlgorithm.setDuration(animationDuration)

        self.animationGroupBoxDictionary = QtCore.QPropertyAnimation(self.ui.groupBoxDictionary, "geometry")
        self.animationGroupBoxDictionary.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxDictionary.setDuration(animationDuration)

        self.animationGroupBoxErrors = QtCore.QPropertyAnimation(self.ui.groupBoxErrors, "size")
        self.animationGroupBoxErrors.setEasingCurve(QtCore.QEasingCurve.OutExpo)
        self.animationGroupBoxErrors.setDuration(animationDuration)

        if self.flags['groupBoxDataResized'] == 0:
            self.animationWindow.setEndValue(QtCore.QSize(1000,self.ui.basicWindowSize[1]))
            self.animationGroupBoxBooks.setEndValue(QtCore.QRect(710,10,280,370))
            self.animationGroupBoxDataInfo.setEndValue(QtCore.QSize(180,140))
            self.animationGroupBoxAlgorithm.setEndValue(QtCore.QSize(180,220))
            self.animationGroupBoxErrors.setEndValue(QtCore.QSize(980,160))
            self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(495,10,200,370))
            self.setMaximumSize(QtCore.QSize(1000, self.ui.basicWindowSize[1]))
            self.flags['groupBoxDataResized'] = 1
        else:
            self.animationWindow.setEndValue(QtCore.QSize(self.ui.basicWindowSize[0],self.ui.basicWindowSize[1]))
            self.animationGroupBoxBooks.setEndValue(QtCore.QRect(310,10,280,370))
            self.animationGroupBoxDataInfo.setEndValue(QtCore.QSize(0,140))
            self.animationGroupBoxAlgorithm.setEndValue(QtCore.QSize(0,220))
            self.animationGroupBoxErrors.setEndValue(QtCore.QSize(580,160))
            self.animationGroupBoxDictionary.setEndValue(QtCore.QRect(305,10,0,370))
            self.setMinimumSize(QtCore.QSize(self.ui.basicWindowSize[0], self.ui.basicWindowSize[1]))
            self.flags['groupBoxDataResized'] = 0

        self.animation.addAnimation(self.animationWindow)
        self.animation.addAnimation(self.animationGroupBoxBooks)
        self.animation.addAnimation(self.animationGroupBoxDataInfo)
        self.animation.addAnimation(self.animationGroupBoxAlgorithm)
        self.animation.addAnimation(self.animationGroupBoxDictionary)
        self.animation.addAnimation(self.animationGroupBoxErrors)

        self.animation.start()

    def setProperWindowSize(self):
    	if self.flags['groupBoxDataResized'] == 0:
    		self.setMaximumSize(QtCore.QSize(self.ui.basicWindowSize[0], self.ui.basicWindowSize[1]))
    	else:
    		self.setMinimumSize(QtCore.QSize(1000, self.ui.basicWindowSize[1]))


