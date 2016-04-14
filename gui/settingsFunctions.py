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
from platform  import system
from functools import partial
from os.path   import expanduser
from PyQt4     import QtCore, QtGui

# gui imports #
from settingsGraphics import mainWindowUI

# modules imports #
import data.dataLoader as dl
from src.utils import determineAlgorithmConfig , determineDictionaryConfig , generateRangeFromString

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

        # self.ui.led_samplingFrequency.textChanged.connect(self.samplingFrequencyChanged)
        # self.ui.led_iterationsLimit.textChanged.connect(self.iterationsLimitChanged)
        # self.ui.led_energyLimit.textChanged.connect(self.energyLimitChanged)
        # self.ui.led_nfft.textChanged.connect(self.nfftChanged)

        # GroupboxDictionary
        # self.led_dictonaryDensity
        # self.led_minS
        # self.led_maxS
        # self.cmb_minS
        # self.cmb_maxS
        # self.cmb_maxS
        # self.cmb_minS

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

            self.warnings = {}
            self.warnings['wrongType']      = 'Wrong file type, in '
            self.warnings['openData_err_0'] = 'Wrong file type, in '
            self.warnings['openData_err_1'] = 'Field "data" was not found in the file '
            self.warnings['openData_err_2'] = 'Either "channels" or "trials" did not match the shape of "data", in '
            self.warnings['openData_err_3'] = 'Data matrix has more than three dimensions, in '

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
        config['iterationsLimit'] = int(self.ui.led_iterationsLimit.text())
        config['energyLimit']     = float(self.ui.led_energyLimit.text())
        config['nfft']            = int(self.ui.led_nfft.text())
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
        
        if str(self.ui.cmb_maxS.currentText) == 'samples':
            self.dictionaryConfig['maxS_samples']      = int(self.ui.led_maxS.text())
            self.dictionaryConfig['maxS_seconds']      = float(self.dictionaryConfig['maxS_samples'] / float(self.ui.led_samplingFrequency.text()))
            # self.dataMatrixes[self.filePath][1]['samplingFreq']
        else:
            self.dictionaryConfig['maxS_seconds']      = float(self.ui.led_maxS.text())
            self.dictionaryConfig['maxS_samples']      = int(self.dictionaryConfig['maxS_seconds'] * float(self.ui.led_samplingFrequency.text()))

        if str(self.ui.cmb_minS.currentText) == 'samples':
            self.dictionaryConfig['minS_samples']      = int(self.ui.led_minS.text()) 
            self.dictionaryConfig['minS_seconds']      = float(self.dictionaryConfig['minS_samples'] / float(self.ui.led_samplingFrequency.text()))
        else:
            self.dictionaryConfig['minS_seconds']      = float(self.ui.led_minS.text())
            self.dictionaryConfig['minS_samples']      = int(self.dictionaryConfig['minS_seconds'] * float(self.ui.led_samplingFrequency.text()))


    # def samplingFrequencyChanged(self):
    #     text = self.ui.led_samplingFrequency.text()
    #     try:
    #         sf = float(text)
    #         dataId = str(self.ui.lst_data.currentItem().text())
    #         if sf > 0.0:
    #             pass
    #             self.dataMatrixes[dataId][1]['samplingFreq'] = sf
    #         elif sf == 0.0:
    #             self.ui.led_samplingFrequency.setText(str(self.dataMatrixes[dataId][1]['samplingFreq']))
    #             msg = 'Sampling Frequency can not be equal to 0[Hz]!'
    #             self.warrning('on' , msg , 3000)
    #         else:
    #             self.dataMatrixes[dataId][1]['samplingFreq'] = abs(sf)
    #             self.ui.led_samplingFrequency.setText(str(abs(sf)))
    #     except ValueError:
    #         self.ui.led_samplingFrequency.setText(text[0:-1])
    #         if len(text[0:-1]) > 0:
    #             msg = '"Sampling Frequency" field contained incorrect characters!'
    #             self.warrning('on' , msg , 3000)

    # def energyLimitChanged(self):
    #     text = self.ui.led_energyLimit.text()
    #     try:
    #         energy = float(text)
    #         dataId = str(self.ui.lst_data.currentItem().text())
    #         if energy < 1 and energy > 0:
    #             self.dataMatrixes[dataId][2]['energyLimit'] = str(energy)
    #         elif energy >= 1:
    #             self.dataMatrixes[dataId][2]['energyLimit'] = str(0.99)
    #             self.ui.led_energyLimit.setText(str(0.99))
    #             msg = 'It is impossible to explain more than 100 percent of a signal energy!'
    #             self.warrning('on' , msg , 3000)
    #         elif energy < 0:
    #             self.dataMatrixes[dataId][2]['energyLimit'] = str(abs(energy))
    #             self.ui.led_energyLimit.setText(str(abs(energy)))
    #         else:
    #             self.ui.led_energyLimit.setText(str(self.dataMatrixes[dataId][2]['energyLimit']))
    #             msg = 'Explained signal energy should be greater than 0!'
    #             self.warrning('on' , msg , 3000)
    #     except ValueError:
    #         self.ui.led_energyLimit.setText(text[0:-1])
    #         if len(text[0:-1]) > 0:
    #             msg = '"Energy percentage" field contained incorrect characters!'
    #             self.warrning('on' , msg , 3000)

    # def iterationsLimitChanged(self):
    #     text = self.ui.led_iterationsLimit.text()
    #     try:
    #         iterations = int(text)
    #         dataId = str(self.ui.lst_data.currentItem().text())
    #         if iterations > 0:
    #             self.dataMatrixes[dataId][2]['iterationsLimit'] = str(iterations)
    #         elif iterations == 0:
    #             self.ui.led_iterationsLimit.setText(str(self.dataMatrixes[dataId][2]['iterationsLimit']))
    #             msg = '# of iterations should be greater than 0!'
    #             self.warrning('on' , msg , 3000)
    #         else:
    #             self.dataMatrixes[dataId][2]['iterationsLimit'] = abs(iterations)
    #             self.ui.led_iterationsLimit.setText(str(abs(iterations)))
    #     except ValueError:
    #         self.ui.led_iterationsLimit.setText(text[0:-1])
    #         if len(text[0:-1]) > 0:
    #             msg = '"# of iterations" has to be integer!'
    #             self.warrning('on' , msg , 3000)

    # def nfftChanged(self):
    #     text = self.ui.led_nfft.text()
    #     try:
    #         iterations = int(text)
    #     except ValueError:
    #         self.ui.led_nfft.setText(text[0:-1])

    #     # str(1 << (int(dataInfo['samplingFreq'])-1).bit_length())

# WIDGETS BEHAVIOUR
##################
    def chooseDataFiles(self):

        dialog = QtGui.QFileDialog.getOpenFileNames(self , 'Open data files' , expanduser('~') , 'All Files (*);;Matlab files (*.mat);;Python pickles (*.p)')

        warningCollector = ''
        for filePath in dialog:
            if filePath != '':
                self.displayInformation('Opening file '+ filePath + '. Please wait...' , 'new')
                if filePath[-4:] == '.mat' or filePath[-2:] == '.p':
                    (dataMatrix , dataInfo , message) = dl.loadSigmalFromFile(filePath)
                else:
                    warningCollector = warningCollector + self.warnings['wrongType'] + filePath + '\n'

                if message == 'ok':
                    self.addData(filePath , dataMatrix , dataInfo)
                else:
                    warningCollector = warningCollector + self.warnings['openData_'+message] + filePath + '\n'

        self.displayInformation('' , 'new')
        if warningCollector != '':
            self.warrning('on' , warningCollector)

        self.changeButtonsAvailability()

    def removeData(self):
        item = self.ui.lst_data.currentItem()
        del self.dataMatrixes[str(item.text())]
        self.ui.lst_data.takeItem(self.ui.lst_data.currentRow())

        if self.ui.lst_data.count() < 1:
            if self.flags['groupBoxDataResized'] == 1:
                self.resizeWindow()

        self.changeButtonsAvailability()

    def selectData(self):
        try:
            try:
                config = self.setAlgorithmConfig()
                self.dataMatrixes[self.filePath][2] = config
                config = self.setDataInfoConfig()
                self.dataMatrixes[self.filePath][1] = config
            except ValueError:
                # means, there is nothing to store
                pass

            self.filePath = str(self.ui.lst_data.currentItem().text())
            self.setDataInfoControlls(self.dataMatrixes[self.filePath][1])
            self.setAlgorithmControlls(self.dataMatrixes[self.filePath][2])
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
            palette = QtGui.QPalette()
            self.ui.lbl_errors.setText(errorMsg)
            palette.setColor(QtGui.QPalette.Foreground, self.warrningTextColor)
            self.ui.lbl_errors.setPalette(palette)
            self.ui.groupBoxErrors.show()
            self.timer.singleShot(time , self.timerEvent)
        elif flag == 'off':
            self.ui.lbl_errors.setText('')
            self.ui.groupBoxErrors.hide()
        QtGui.QApplication.instance().processEvents()   # Important!

### PROCESSING EVENTS:
######################
    def addData(self , filePath , dataMatrix , dataInfo):
        filePath = str(filePath)

        algorithmConfig       = determineAlgorithmConfig(dataInfo)
        self.dictionaryConfig = determineDictionaryConfig(self.dictionaryConfig , algorithmConfig['energyLimit'] , dataInfo)

        self.dataMatrixes[filePath] = [dataMatrix , dataInfo , algorithmConfig]
        
        self.setDictionaryControlls()

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


