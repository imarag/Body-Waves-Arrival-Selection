from PyQt5.QtWidgets import QPushButton, QPlainTextEdit, QMainWindow, QAction, QComboBox,QLabel, QFormLayout, QScrollArea, QColorDialog, QLineEdit, QApplication, QWidget, QVBoxLayout, QRadioButton, QButtonGroup, QHBoxLayout, QFileDialog, QMessageBox,QToolBar, QCheckBox 
from PyQt5.Qt import Qt
from PyQt5 import QtGui


import pyqtgraph as pg
from pyqtgraph import GraphicsLayoutWidget


import numpy as np
import pandas as pd

import re
import sys
import glob
import os
import pathlib
import shutil

from obspy.core import read, UTCDateTime
from obspy.core.stream import Stream
from obspy.core.trace import Trace



class ShowWaveformInfo(QScrollArea):
    def __init__(self, dpi, stream):
        super().__init__()
        self.dpi = dpi
        self.inches_text = 0.14

        self.setWidgetResizable(True)

        self.main_widget = QWidget()
        self.verBoxLayout = QVBoxLayout()

        self.setStyleSheet('''
            *{color: white; background-color: #3a3a3a; font-size:''' +  str(int(self.inches_text * self.dpi)) + 'px' + '''}
            QLabel#title {margin-bottom: 50px;}
            QLabel{font-family: consolas}
            ''') 

        self.lb_title = QLabel("<h1>Information about the record</h1>")
        self.lb_title.setObjectName('title')
        self.lb_title.setWordWrap(True)

        self.setWidget(self.main_widget)
        self.main_widget.setLayout(self.verBoxLayout)
        
        self.verBoxLayout.addWidget(self.lb_title)

        for tr in stream:
            lb_wave = str(tr.stats)
            lb = QLabel(lb_wave)
            print(lb)
            lb.setWordWrap(True)
            self.verBoxLayout.addWidget(lb)
            
        

class ShortcutsClass(QScrollArea):
    def __init__(self, dpi):
        super().__init__()
        self.dpi = dpi
        self.inches_text = 0.14

        self.setWidgetResizable(True)

        self.main_widget = QWidget()
        self.verBoxLayout = QVBoxLayout()

        self.setStyleSheet('''
            *{color: white; background-color: #3a3a3a; font-size:''' +  str(int(self.inches_text * self.dpi)) + 'px' + '''}
            QLabel#title {margin-bottom: 50px;}
            QLabel#ending {margin-top: 80px; margin-bottom: 100px; font-family: consolas}
            ''')

        
        self.setWidget(self.main_widget)
        self.main_widget.setLayout(self.verBoxLayout)

        self.lb_title = QLabel('<h1>Shortcuts</h1>')
        self.lb_title.setObjectName('title')
        self.lb_title.setWordWrap(True)

        dct = {
            'Save waveform': 'N',
            'Next waveform file' : 'M',
            'Move to NOTSURE folder' : 'K',
            'Move to NOTGOOD folder' : 'J',
            'Move the waveform to the right' : 'D',
            'Move the waveform to the left' : 'A',
            'Zoom in the Y axis' : 'W',
            'Zoom out in the Y axis' : 'S',
            'Pan the waveform' : 'left-click pressed',
            'Zoom in/out in the X axis' : 'right-click pressed',
            'Zoom in/out in both axis' : 'scroll-wheel',
            'Insert a P|S arrival' : 'double-click',
        }
       
        self.formlayout = QFormLayout()

        for lb in dct:
            key = QLabel(dct[lb])
            label = QLabel(':    ' + lb)
            self.formlayout.addRow(key, label)

        self.verBoxLayout.addWidget(self.lb_title)
        self.verBoxLayout.addLayout(self.formlayout)







class ProgramInfoClass(QScrollArea):
    def __init__(self, dpi):
        super().__init__()
        self.dpi = dpi
        self.inches_text = 0.14

        self.setWidgetResizable(True)

        self.main_widget = QWidget()
        self.verBoxLayout = QVBoxLayout()

        self.setStyleSheet('''
            *{color: white; background-color: #3a3a3a; font-size:''' +  str(int(self.inches_text * self.dpi)) + 'px' + '''}
            QLabel#title {margin-bottom: 50px;}
            QLabel#ending {margin-top: 80px; margin-bottom: 100px; font-family: consolas}
            ''')

        
        self.setWidget(self.main_widget)
        self.main_widget.setLayout(self.verBoxLayout)

        self.lb_title = QLabel('<h1>Information about the program</h1>')
        self.lb_title.setObjectName('title')
        self.lb_title.setWordWrap(True)

        self.lb_body = QLabel('''
            <p>This program is written by Ioannis Maragkakis using the library PyQt5 and pyqtgraph of the Python programming language. Feel free to use it and share it. This program was written throughout my master of applied Geophysics and Seismology of the Aristotle university of Thessaloniki (2019-2022). It is remade after my master. The Python libraries used, are: <ul><li><b><i>PyQt5</i></b> for the graphical user interface (GUI)</li> <li><b><i>pyqtgraph</i></b> for the visualizations (waveforms, arrival lines etc.) </li> <li><b><i>Obspy</i></b> to read and edit the seismic records</li> <li>Other libraries to process the files (e.g. <i><b>os</i></b>, <i><b>re</i></b>, <i><b>glob</i></b>, <i><b>pathlib</i></b>) In case any problem is encountered, feel free to contact me using the following details:</p>
            '''
        )
        self.lb_body.setObjectName('body')
        self.lb_body.setWordWrap(True)


        self.lb_ending = QLabel('''
            <pre>
                email: <a style="color:#517ffc" href="#"><u>giannis.marar@hotmail.com<u></a>
                linkedin:  <a style="color:#517ffc" href="#"><u>www.linkedin.com/in/ioannis-maragkakis-1ba2851a9</u></a>
            </pre>
        ''')
        self.lb_ending.setObjectName('ending')
        self.lb_ending.setWordWrap(True)
        self.lb_ending.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.verBoxLayout.addWidget(self.lb_title)
        self.verBoxLayout.addWidget(self.lb_body)
        self.verBoxLayout.addWidget(self.lb_ending)





class txtToMseedClass(QScrollArea):
    abs_path_to_parent_of_file = pathlib.Path(__file__).resolve().parent 
    
    def __init__(self, dpi):
        super().__init__()
        self.dpi = dpi
        self.inches_text = 0.14

        self.setWidgetResizable(True)
        self.main_widget = QWidget()
        self.verBoxLayout = QVBoxLayout()


        self.main_widget.setStyleSheet('''
            *{color: white; background-color: #3a3a3a; font-size:''' +  str(int(self.inches_text * self.dpi)) + 'px' + '''}
            QLabel#title {margin-bottom: 50px;}
            QLabel#sample {margin-top: 80px; margin-bottom: 100px; font-family: consolas}
            QPushButton {background-color: #ccf7b7; color: black; font-weight: bold}
            ''')


        self.setWidget(self.main_widget)
        self.main_widget.setLayout(self.verBoxLayout)
        
        
        self.bt_load = QPushButton('Load folder')
        self.bt_load.clicked.connect(self.load_folder_data)

   
        self.label_title = QLabel('<h1>Convert ASCII files to MSEED</h1>')
        self.label_title.setObjectName('title')
        self.label_title.setWordWrap(True)

        self.label_body = QLabel(
            '<p>Below there is a sample header of a file, showing the information that each file needs to have, so the program can convert the <code>TXT</code> files to <code>MSEED</code> files. It is important to provide (the order is not important):</p>' + 
            '<ul> \
                <li>the <b>station name</b> (the program is looking for the word "station" in the header)</li>  \
                <li>The <b>components</b> (the program is searching for the word "components" in the header)</li> \
                <li>The <b>start date</b> of the record (the file is looking for the word "starttime" in the header)</li>\
                <li>One of <b>sampling frequency</b> (the program is looking for the word "frequency") or <b>delta</b> (the program is looking for the word "delta" in the header)</li> \
            </ul> ' +
            '<p>The number of sampling points (<b>npts</b>) is not necessary to be provided. It will be calculated from the length of the acceleration values. All properties must be in the form "property: value" <b>Be careful, you need to provide the colon (:) after each attribute.</b> Lastly, a folder name called "mseed_converted_files" is going to be created with the converted mseed files in it.</p>' 
        )
        self.label_body.setObjectName('body')
        self.label_body.setWordWrap(True)

        self.label_sample = QLabel(
            '''
            <pre>
                *******************************************
                                                            
                station: PRF0 
                sampling frequency (fs): 200.0   
                delta: 0.005     
                components: E N Z 
                starttime: 2015-07-24 09:58:34 
                                                    
                0.02758933  0.00252933  0.00758933 
                0.00758935  0.00758983  0.01658931 
                0.00728f53  0.00758933  0.00758933 
                0.00758931  0.01728933  0.00778937 
                                                        
                ******************************************** 
  
            </pre> 
            '''
        )
        self.label_sample.setObjectName('sample')
        self.label_sample.setWordWrap(True)


        self.verBoxLayout.addWidget(self.label_title)
        self.verBoxLayout.addWidget(self.label_body)
        self.verBoxLayout.addWidget(self.label_sample)
        self.verBoxLayout.addWidget(self.bt_load)


         
    
    def load_folder_data(self):
        self.folder_data = str(QFileDialog().getExistingDirectory(self, 'Select a directory'))
          
        if not self.folder_data:
            return
   
        txtfiles = list(glob.glob(self.folder_data + "/*.txt"))
        datfiles = list(glob.glob(self.folder_data + "/*.dat"))
        self.asciifiles = txtfiles + datfiles
        
        if not self.asciifiles:
           QMessageBox.critical(self, 'Empty folder', 'The folder you selected is empty')
           return
   
        QMessageBox.information(self, 'Files read', f'Found {len(txtfiles)} .txt files and {len(datfiles)} .dat files.')
        
        self.edit_loaded_data()
        
    
    def edit_loaded_data(self):
        
        
    
        if not os.path.exists(self.folder_data + "/mseed_converted_files"):
             os.mkdir(self.folder_data + "/mseed_converted_files")
    
        
    
    
        for arx in self.asciifiles:
             name = pathlib.Path(arx).stem
   
             with open(arx, 'r') as f:
                  ff = f.readlines()
                  ind_num = None
                  params_provided = []

             header = {}
             
             for line in ff:

                  if 'station' in line.lower():
                       station = line.split(":")[1].strip()
                       header["station"] = station
                       params_provided.append('station')
                       
                  elif 'delta' in line.lower():
                       delta = line.split(":")[1].strip()
                       patt = re.search("[0-9]+", delta)
                       delta = delta[patt.start(): patt.end()]
                       if not re.search('^[0-9]+\.?[0-8]*$', delta):
                            QMessageBox.critical(self, 'Information invalid', f'The parameter "delta" in the header ({delta}) is not valid number ({name})')
                            return
   
                       header["delta"] = float(delta)
                       params_provided.append('delta')
                       
                 
                        
                  elif 'frequency' in line.lower():
                       sampling_rate = line.split(":")[1].strip()
              
                       if not re.search('^[0-9]+\.?[0-8]*$', sampling_rate):
                            QMessageBox.critical(self, 'Information invalid', f'The frequency in the header ({sampling_rate}) is not a valid number ({name})')
                            return
                       header["sampling_rate"] = float(sampling_rate)
                       params_provided.append('frequency')
                       

                  elif 'components' in line.lower():
                      compo = line.split(":")[1].split()
                      params_provided.append('components')
                       
                  elif 'starttime' in line.lower():
                      try:
                          utcdt = UTCDateTime(line.split(":", 1)[1])
                      except:
                          QMessageBox.critical(self, 'Invalid information', f'Cannot convert the starttime provided ({line.split(":", 1)[1]}). Check your input ({name})')
                          return
                      header['starttime'] = utcdt
                      params_provided.append('starttime')
                      
                  elif line.strip() and line.strip().lstrip("-")[0].isnumeric():
                      
                      ind_num = ff.index(line)
                      break
                  
             if not ind_num:
                 QMessageBox.critical(self, 'Invalid input', 'Cannot find the rows where the data (numbers) start. Check the sample file!')
                 return

              
             if 'station' not in params_provided:
                 QMessageBox.critical(self, 'Invalid input', 'You didnt insert any station name. The program is looking for the word "station" on the file header. Check the sample header provided when clicking the option "ASCII to MSEED" and try again!')
                 return
             
             if 'components' not in params_provided:
                 QMessageBox.critical(self, 'Invalid input', 'You didnt insert any components. The program is looking for the word "components" on the file header. Check the sample header provided when clicking the option "ASCII to MSEED" and try again!')
                 return
             
             if 'starttime' not in params_provided:
                 QMessageBox.critical(self, 'Invalid input', 'You didnt insert any start datetime of the record. The program is looking for the word "starttime" on the file header. Check the sample header provided when clicking the option "ASCII to MSEED" and try again!')
                 return
             
             if 'delta' not in params_provided and 'frequency' not in params_provided:
                 QMessageBox.critical(self, 'Invalid input', 'You didnt insert the "delta" or the "sampling frequency". You need to provide one of them. The program is looking for the word "delta" for the delta and the word "frequency" for the sampling frequency on the file header. Check the sample header provided when clicking the option "ASCII to MSEED" and try again!')
                 return
              
    
             data = ff[ind_num:]
             data = np.array([dt.split() for dt in data])
             data_dict = {}
             length = data.shape[1]
             for i in range(length):
                 data_dict[compo[i]] = data[:, i].astype(float)
                
  
             traces = []
             for cp in data_dict:
                 header["channel"] = cp
                 tr = Trace(data=data_dict[cp], header=header) 
                 traces.append(tr)
               
             try:
                 stream = Stream(traces)
             except Exception as e:
                 QMessageBox.critical(self, 'Something went wrong', str(e))
                 
             stream.write(self.folder_data + "/mseed_converted_files/" + name + ".mseed")
        
        QMessageBox.information(self, 'mseed_converted_files folder created', 'Succesfully converted the files. Check the folder "mseed_converted_files" in the current path, for the .mseed files')


class ProgramTutorial(QWidget):


    def __init__(self, dpi):

        super().__init__()
        self.dpi = dpi
        self.inches_text = 0.14

        self.dct = {
        'Read-me-first': 
        'Below you will find some important things to remember before you start selecting the arrival times of the P and S waves:\n\n'
        'I) The position of the Python file that you run, is important. When you select the arrivals of a record, the program saves the arrivals in a folder called "picked", located in the same folder where this python file is located\n'
        'II) The program reads MSEED files that you need to have in order to select the arrivals. If you just have the acceleration values in a TXT or DAT file, there is an option in the program that you can transform TXT files into MSEED files. Please try to format the TXT files as close as possible to the sample file that i provide when you click this option.\n'
        'III) Check the keyboard shortcuts that you can use while selecting the arrivals. It will help trust me! I used them all the time\n'
        'IV) The program is not perfect. I am sure there will be some bugs in it but it does its job. If there is any bug just close the program and re-open it. And if it is really annoying just let me know. I have my details in the "information" tab.\n'
        'V) Change the template selecting a them on the bottom to help you select the arrivals easier.\n'
        'VI) Dont do anything stupid and rename the files that the program creates. It is only gonna make your life more difficult. Just let the program do its own things and you just select the arrivals.\n'
        'VII) Please have all of your mseed files in one place (folder) and dont use different paths. Again it is not gonna help if you do otherwise\n'
        'VIII) Please put all of your mseed files in a folder (it doent matter where, as long as it is not in the "picked" folder) and then use this folder you select the arrivals'
        ,
        "Browse": 'Use this option to search for a record and more specifically a file with ".mseed" extension. As soon as you select one, the folder where this file is located, becomes the "NEXT" folder. That means that you have to use the <Browse> option initially when you start the program, to define the "NEXT" folder and be able to use the <Next> option. EVERY time you use the <Browse> option, the "NEXT" folder is re-defined, if it is different from the previous one.',
        "Load": 'Load a folder that you have already selected the arrivals. This folder must contain one MSEED file with the record and one TXT file with the arrivals (ending in "_arrivals.txt") that were created from the program when you selected the arrivals. If not, the option will throw an error.',
        "Save": 'Save the selected arrivals. The program automatically creates a folder in the "picked" folder with name, the name of the record. Then the program moves the MSEED file into this folder and at the same time it creates a TXT file ending in "_arrivals.txt", with the selected arrivals in this folder too. ',
        "Next": 'This option is created to facilitate the picking. Instead of browsing for a file over and over again by searching for and clicking on a different file every time, this option help you to load immidiately the first file found in the "NEXT" folder whose path is defined ONLY when using the <Browse> option. Every time you press the <Next> button, the first file from the "NEXT" folder is loaded automatically. You need to use the <Browse> option initially, to define the "NEXT" folder. Every time you select a file using the <Browse> option, you re-define the "NEXT" folder, if it is different than the previous one.',
        "NotGood": 'This folder is used to move the current loaded MSEED file to the "mypicker_notgood_files" folder. You can use this folder to move the records that it is impossible to select the arrivals, due to the low signal to noise ratio. This folder is created the first time you select the option <NotGood>, and it is located in the same path where the "picked" folder exists.',
        "NotSure": 'This folder is used to move the current loaded MSEED file to the "mypicker_for_later" folder. You can use this folder to move the records that you are not sure about how to select the arrivals at that time and you want to save the file so you can select the arrivals another time. This folder is created the first time you select the option <NotSure> and it is located in the same path where the "picked" folder exists.',
        "Zoom Y-Axis": 'When you apply a filter (ex. 1-5Hz) the amplitude of the waveforms changes (decreases). This option helps to change the y-axis limits from the minimum to the maximum value of the waveforms amplitudes every time, when a filter is applied',
        "Toggle y-axis": 'Using this option, the waveforms cannot be moved in the Y direction (up and down). Try to move one waveform in the Y direction when this option is activated to see the result.',
        'TXTtoMSEED': 'Helps to transform TXT and DAT files, to MSEED files. These files are read by the program. Just select the folder that contains the TXT or DAT files. Please try to format your TXT files as close as possible to the sample file that i provide when you click this option. The program is only searching for TXT files in the folder you selected, NOT in folders existing in the folder you selected.',
        'Reset': "Resets the X and Y axis limits from the minimum to the maximum values.",
        'left-right filter': "Apply manually a filter on the waveforms of the current record instead of selecting a predefined option from the radiobuttons on the upper right part of the window. If both entries (right and left) are filled with a number, then a bandpass filter is applied. If just the left filter is filled with a number, a highpass filter is applied. If only the right filter is filled with a number, a lowpass filter is applied",
        'Trim waveforms' : 'Trim (cut) the waveforms at an area between two vertical lines which you can move to manage that area. These lines are apparent only in the first waveform but dont worry about it. It will trim all of them.',
        'Arrivals to excel': 'Use this option to select a folder with the selected arrivals (files ending in "_arrivals.txt") to extract them to an excel file. It is useful if you want to collect all of them in one place and use them at a later stage. Take into account that the program searches for ALL the arrival files (files ending in _arrivals.txt) everywhere in the folder specified. That is it searches in the folder you selected, in the folders inside the folder you selected and so on.',
        'Extr. acc. values': 'Extract the y values (acceleration) of the waveforms at an excel file. This option is useful if you want to edit the waveforms (e.g. apply some filter or trim the waveforms) and then just save the values without selecting any arrival.',
        'Detrend waveforms': 'Remove a trend from the waveforms. That means, move the start of your waveforms to the zero Y value (check here for more instructions https://docs.obspy.org/packages/autogen/obspy.core.trace.Trace.detrend.html'
        }

        
        self.layoutH = QHBoxLayout()
        self.layoutV = QVBoxLayout()
        self.main_widget = QWidget()
        self.scroll_widget = QScrollArea()
        self.entry_plaintext = QPlainTextEdit("Select the buttons on the left to learn about the functionality of each element!")
        
        self.setLayout(self.layoutH)
        self.layoutH.addWidget(self.scroll_widget, 1)   
        self.layoutH.addWidget(self.entry_plaintext, 3) 
        self.scroll_widget.setWidgetResizable(True)
        self.scroll_widget.setWidget(self.main_widget)
        self.main_widget.setLayout(self.layoutV)
          

       
        self.setStyleSheet('''
            *{color: white; background-color: #3a3a3a; font-size:''' +  str(int(self.inches_text * self.dpi)) + 'px' + '''}
            QPushButton {background-color: #3a3a3a; color: white; font-weight: bold}
            QPushButton::hover {background-color: white; color:#3a3a3a}
            QPlainTextEdit {font-weight: light; background-color: white; color: black;}
            ''')


        for lb in self.dct:
            
            bt = QPushButton(lb)

            self.layoutV.addWidget(bt)
            bt.clicked.connect(self.show_info)

    def show_info(self):
        bt_label = self.sender().text()
        text = self.dct[bt_label]
        self.entry_plaintext.setPlainText(text)








class MyPickerClass(QMainWindow):
    
    
    abs_path_to_parent_of_file = pathlib.Path(__file__).resolve().parent # auto einai to absolute path tou parent file toy mypicker.py

    

       
    def __init__(self, dpi):
        
        super().__init__()
        self.dpi = dpi
        self.pixel_size_in = 1 / self.dpi
        self.inches_selected = 0.14
        self.inches_selected_pg_vert_ln = 0.02
        self.inches_selected_pg_sym = 0.3
        self.inches_windows=5

        self.setWindowTitle('P&S wave arrivals')
        
        self.mainlayout = QWidget()
        
        self.verBoxMain = QVBoxLayout()
        self.horBoxUpper = QHBoxLayout()
        self.verBoxMiddle = QVBoxLayout()
        self.horBoxLower = QHBoxLayout()
   
      
        
        self.verBoxMain.addLayout(self.horBoxUpper)
        self.verBoxMain.addLayout(self.verBoxMiddle)
        self.verBoxMain.addLayout(self.horBoxLower)
       
        
        self.graphlayout = GraphicsLayoutWidget()
       
        self.p1 = self.graphlayout.addPlot(row=0, col=0)
        self.p2 = self.graphlayout.addPlot(row=1, col=0)
        self.p3 = self.graphlayout.addPlot(row=2, col=0)
        
        
        self.plotwidgets_list = [self.p1, self.p2, self.p3]
        self.legend = []
        self.gridlist = [pg.GridItem(textPen=None), pg.GridItem(textPen=None), pg.GridItem(textPen=None)]
        self.plotdataitems_list = []
        self.PSvert_lines_dictionary = {'P':[] , 'S':[]}
        self.PSsymbols_dictionary = {'P':[] , 'S':[]}
        self.nextfolder = None
        
    
        
        for n,pt in enumerate(self.plotwidgets_list):
            
            font = QtGui.QFont()
            font.setPixelSize(int(self.dpi * self.inches_selected))
            left = pt.getAxis('left')
            bottom = pt.getAxis('bottom')
            bottom.setStyle(tickFont=font, tickTextOffset=int(self.dpi * self.inches_selected))
            left.setStyle(tickFont=font, )
            left.setLabel('      ')
            

            # this is to be able to move the axis both in x and y
            pt.getViewBox().setMouseEnabled(x=True,y=True)
            # # this is to disable the menu when right clicking
            pt.setMenuEnabled(False)
            # # create a legend item and anchor it over the internal ViewBox
            # # Plots added after this will be automatically displayed in the legend if they are created with a ‘name’ argument.
           
            leg = pt.addLegend(pen='b', brush='k', labelTextColor='w', offset=(0, .5))
            
            self.legend.append(leg)
        
        # self.p3.getAxis('bottom').setWidth(2)
        self.verBoxMiddle.addWidget(self.graphlayout)
       
        
        self.mainlayout.setLayout(self.verBoxMain)
        
        self.setCentralWidget(self.mainlayout)
        
        self.allActions()
        self.createToolBar()
        self.createwidgets()
        self.createMenu()
        self.createstatusbar()
        self.initialstate()

        self.pen_plotdataitem= pg.mkPen(color='#f7ff58')
        self.pen_vert_lines = pg.mkPen(color='#abc4ff', style=Qt.DashLine, width=4)
        self.pen_symbol = pg.mkPen(color='#ffffff', width=40)

        # click event
        self.graphlayout.scene().sigMouseClicked.connect(self.clicked_event_on_graph)  
        
        # #auto einai gia na breis se poio axes mesa einai to pontiki sou
        self.proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved, rateLimit=60, slot=self.findinaxes)
        

        self.menu.setStyleSheet('font-size:' + str(int(self.inches_selected * self.dpi)) + 'px')
        self.btSrem.setStyleSheet('font-size:' + str(int(self.inches_selected * self.dpi)) + 'px; background-color: #ff264a; color: black')
        self.btPrem.setStyleSheet('font-size:' + str(int(self.inches_selected * self.dpi)) + 'px; background-color: #ff264a; color: black')
        self.set_theme('default')
        
       
    
    def set_pens(self, property_name, property_value):
        
        if property_name == 'plotdataitems':
            self.pen_plotdataitem= pg.mkPen(color=property_value)
            
            if self.plotdataitems_list:
                for pdi in self.plotdataitems_list:
                    pdi.setPen(self.pen_plotdataitem)
                
            
        
        elif property_name == 'verticallines':
            self.pen_vert_lines = pg.mkPen(color=property_value[0], style=Qt.DashLine, width=property_value[1])
            if self.PSvert_lines_dictionary['S']:
                
                for vl in self.PSvert_lines_dictionary['S']:
                    vl.setPen(self.pen_vert_lines)
                    
            if self.PSvert_lines_dictionary['P']:
                if self.PSvert_lines_dictionary['P']:
                    for vl in self.PSvert_lines_dictionary['P']:
                        vl.setPen(self.pen_vert_lines)
                    
            
        else:
            self.pen_symbol = pg.mkPen(color=property_value[0], width=property_value[1])

            if self.PSsymbols_dictionary['P']:

                for sym in self.PSsymbols_dictionary['P']:
                    sym.setHtml('<b style="color: ' + self.pen_symbol.color().name() + '; font-size:' + str(self.pen_symbol.width()) +'px"> P </b>')
                    
  
            if self.PSsymbols_dictionary['S']:
                for sym in self.PSsymbols_dictionary['S']:
                    sym.setHtml('<b style="color: ' + self.pen_symbol.color().name() + '; font-size:' + str(self.pen_symbol.width()) +'px"> S </b>')
    

    def initialstate(self):
        
        
        self.p1.setTitle(" ")
        
        if self.plotdataitems_list:
            for i in range(len(self.plotdataitems_list)):
                 self.plotwidgets_list[i].removeItem(self.plotdataitems_list[i])
             
        self.plotdataitems_list = []
  
        if self.PSsymbols_dictionary['P']:
            for n,sym in enumerate(self.PSsymbols_dictionary['P']):
                 self.plotwidgets_list[n].removeItem(sym)
             
        if self.PSsymbols_dictionary['S']:
            for n,sym in enumerate(self.PSsymbols_dictionary['S']):
                 self.plotwidgets_list[n].removeItem(sym)
              
        if self.PSvert_lines_dictionary['P']:
            for n,vert in enumerate(self.PSvert_lines_dictionary['P']):
                 self.plotwidgets_list[n].removeItem(vert)
              
        if self.PSvert_lines_dictionary['S']:
            for n,vert in enumerate(self.PSvert_lines_dictionary['S']):
                 self.plotwidgets_list[n].removeItem(vert)
                  
        self.PSvert_lines_dictionary = {'P':[] , 'S':[]}
        self.PSsymbols_dictionary = {'P':[] , 'S':[]}
        self.PSarrivals_values = {'P':"" , 'S':""}

        for ax in self.plotwidgets_list:
            ax.setXRange(0,1)
            ax.setYRange(0,1)
          
        for lg in self.legend:
            lg.clear()
          
        for rb in self.filtersGroup.buttons():
            rb.setDisabled(True)
        
        self.filtleft.setDisabled(True)
        self.filtright.setDisabled(True)
          
        # set as filter selected the 'initial' waveform (i have initialized this variable in the create_widgets function)
        self.filterselected = self.initial_filter
        self.initial_filter.setChecked(True)
                      

        self.dt = None
        self.xx = None
        self.inaxes = None
        
        self.btPrem.hide()
        self.btSrem.hide()
        self.rbP.setChecked(True)
        self.rbP.setDisabled(True)
        self.rbS.setDisabled(True)
    
    
    
    def createstatusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready", 0)
        
    def createwidgets(self):
    
        

    
      #--------------------------------------ENTRIES-------------------------------------------
    
      
    
        # left entry handfilter    
        self.filtleft = QLineEdit()
        self.filtleft.setPlaceholderText("Left-filter")
        self.filtleft.returnPressed.connect(self.filterhandenterpressed)

        # right entry handfilter
        self.filtright = QLineEdit()
        self.filtright.setPlaceholderText("Right-filter")
        self.filtright.returnPressed.connect(self.filterhandenterpressed)

   
        

    
      #--------------------------------------QPUSHBUTTONS-------------------------------------------

        # button remove P arrival
        self.btPrem = QPushButton('Del. P')
        self.btPrem.clicked.connect(self.removepicks)
        
      
        # button remove S arrival
        self.btSrem = QPushButton('Del. S') 
        self.btSrem.clicked.connect(self.removepicks)
        

      #--------------------------------------CHECKBOXES-------------------------------------------
      
        # checkbox toggle axis movement
        self.chkbxmoveyaxis = QCheckBox('Toggle y-axis')
        self.chkbxmoveyaxis.stateChanged.connect(self.toogle_y_axis)
        self.chkbxmoveyaxis.setToolTip("Lock the padding on the y-axis")
      
      
        # checkbox addgrid
        self.chkbxgrid = QCheckBox('Add-Grid')
        self.chkbxgrid.stateChanged.connect(self.add_grid)
        self.chkbxgrid.setToolTip("Add grid to facilitate the picking")
      
      
        # checkbox zoom y axis when filtering
        self.chkbxzoomfilter= QCheckBox('Zoom Y-Axis')
        # i do this state changed in this checkbox just to add something to the status bar when checked or unchecked, nothing more
        self.chkbxzoomfilter.stateChanged.connect(self.zoom_filter_checked)
        self.chkbxzoomfilter.setToolTip("Set y-axis from minimum to maximum value when a filter is applied")
      
    

      #--------------------------------------RADIOBUTTONS-------------------------------------------
    
        #radiobutton to select P wave arrivals
        self.rbP = QRadioButton("P")
       
        #radiobutton to select S wave arrivals
        self.rbS = QRadioButton("S")

      #--------------------------------------LAYOUTS-------------------------------------------
    
        self.horBoxUpper.addStretch(stretch=1) 
        self.horBoxLower.addWidget(self.chkbxmoveyaxis)
        self.horBoxLower.addWidget(self.chkbxgrid)          
        self.horBoxLower.addWidget(self.chkbxzoomfilter)
        self.horBoxLower.addStretch(stretch=4) 
        #--------------------------------------QLabels-------------------------------------------
            
        #$$$
        self.combo_themes = QComboBox()
        templates = list(glob.glob(str(MyPickerClass.abs_path_to_parent_of_file) + '/templates/*.qss'))
        templates = [pathlib.Path(tp).stem for tp in templates]
        templates.sort(key=lambda x: int(x[5:]) if 'theme' in x else -1)
        self.combo_themes.addItems(templates)
        self.combo_themes.currentTextChanged.connect(self.set_theme)
        
        # self.bt = QPushButton('random')
        # self.horBoxLower.addWidget(self.bt)
        # self.bt.clicked.connect(self.randomm)
        self.horBoxLower.addWidget(self.combo_themes)
                
        # layout QHBoxLayout for filterhand left and right
        self.horBoxLower.addWidget(self.filtleft)
        self.horBoxLower.addWidget(self.filtright)
        

        self.horBoxUpper.addStretch(stretch=1)        

        # layout for P and S radiobuttons
        self.horBoxUpper.addWidget(self.rbP)
        self.horBoxUpper.addWidget(self.btPrem)
        self.horBoxUpper.addWidget(self.rbS)
        self.horBoxUpper.addWidget(self.btSrem)
        
        self.horBoxUpper.addStretch(stretch=3)
      
    
     
     #--------------------------------------GROUPBUTTONS-------------------------------------------
    
        self.PSGroup = QButtonGroup() 
        self.filtersGroup = QButtonGroup() 
        
    
    #--------------------------------------COMBOBOXES-------------------------------------------
    
        
        self.filters = [ '<10', '0.7-10', '0.7-5', '1-10', '1-5', '1-3', '>0.5', 'initial']
    

        for i in range(len(self.filters)):
            filt = self.filters[i]
    
            rb = QRadioButton(filt)
            self.filtersGroup.addButton(rb)
            rb.clicked.connect(self.setfilters)
            
            if filt == 'initial':
                self.initial_filter = rb
    
            self.horBoxUpper.addWidget(rb)

    
        self.horBoxUpper.addStretch(stretch=1)  
    

        self.PSGroup.addButton(self.rbP)
        self.PSGroup.addButton(self.rbS)
      
        
      

    

    def createMenu(self):


        self.menu = self.menuBar()
        
        self.file_menu = self.menu.addMenu("&File")
        self.edit_menu = self.menu.addMenu("&Edit")
        self.move_menu = self.menu.addMenu("&MoveTo") 
        self.extract_menu = self.menu.addMenu("&extract") 
        self.info_menu = self.menu.addMenu("&Information")
    
        
        self.file_menu.addAction(self.browse_action)
        self.file_menu.addAction(self.load_action)
        self.file_menu.addAction(self.next_action)
        self.file_menu.addAction(self.txttomseed_action)
        self.file_menu.addAction(self.save_action)
        # self.file_menu.addAction(self.set_theme_action)
    
        # self.edit_menu.addAction(self.waveform_action)
        # self.edit_menu.addAction(self.linepick_action)
        # self.edit_menu.addAction(self.textpick_action)
        # self.edit_menu.addAction(self.background_action)
        self.edit_menu.addAction(self.reset_action)
        self.edit_menu.addAction(self.trim_action)
        self.edit_menu.addAction(self.detrend_action)
        
      

        self.move_menu.addAction(self.notgood_action)
        self.move_menu.addAction(self.notsure_action)
        
        self.extract_menu.addAction(self.arrivals_to_excel)
        self.extract_menu.addAction(self.extract_acc_values_action)
        
        self.info_menu.addAction(self.manual)
        self.info_menu.addAction(self.shortcuts_action)
        self.info_menu.addAction(self.myprogram_action)
        self.info_menu.addAction(self.waveform_info)

    def createToolBar(self):

        self.tbtop = QToolBar("righttoolbar", self)
        self.addToolBar(Qt.TopToolBarArea, self.tbtop)    
    
        self.tbtop.addAction(self.browse_action)
        self.tbtop.addAction(self.load_action)
        self.tbtop.addAction(self.next_action)
        self.tbtop.addAction(self.notgood_action)
        self.tbtop.addAction(self.notsure_action)
        self.tbtop.addAction(self.save_action)


          


    def createAction(self, text, info_text, func):
        widget = QAction(text, self)
        widget.setStatusTip(info_text)
        widget.setToolTip(info_text)
        widget.triggered.connect(func)
        return widget

    def allActions(self):

        self.browse_action = self.createAction("Browse", "Browse a new file", self.browse_file)
        self.load_action = self.createAction("Load", "Load a file where the arrival time is already selected", self.load_folder)
        self.next_action = self.createAction("Next", 'Get the next MSEED file from the "NEXT" folder', self.get_next_file)
        self.notgood_action = self.createAction("NotGood", 'Move the file of the record to the "NOTGOOD" folder', self.send_file_to_notgood_folder)
        self.notsure_action = self.createAction("NotSure", 'Move the file of the record to the "NOTSURE" folder', self.send_file_to_notsure_folder)
        self.save_action = self.createAction("Save arrivals", "Save the P & S wave arrival time", self.save_file)
    
        # self.waveform_action = self.createAction("Waveform Color", "Change the waveform color", self.setcolorfunction)
        # self.linepick_action = self.createAction("Line-Pick Color", "Change the color of the pick line", self.setcolorfunction)
        # self.textpick_action = self.createAction("Text-Pick Color", "Change the color of the P/S symbol next to the pick line", self.setcolorfunction)
        # self.background_action = self.createAction("Background Color", "Change the background color of the graphs", self.setcolorfunction)
    
        self.reset_action = self.createAction("Reset", "Reset the window axis limits from the minimum to the maximum value", self.resetlimits)
        self.shortcuts_action = self.createAction("Shortcuts", "Open the keyboard shortcuts window", self.defshortcuts)
        self.txttomseed_action = self.createAction("ASCII to MSEED", "Convert ASCII files to MSEED", self.txttomseed)
    
        self.manual = self.createAction("Manual", "A small tutorial about how to use this program", self.manual_function)
        self.waveform_info = self.createAction("Information about the record", "Information about the traces of the record", self.show_waveform_info)

        
        self.arrivals_to_excel = self.createAction("Arrivals to excel", "Select the folder containing the P and/or S arrival times and extract them to an excel file in the current path.", self.arrivals_to_excel)
        self.myprogram_action = self.createAction("About this program", "Information about the program", self.myprogram_info)
        
        self.trim_action = self.createAction("Trim waveforms", "Trim the waveform", self.trim_waveforms)
        
        self.extract_acc_values_action = self.createAction("Exract acceleration values", "Extract the acceleration values", self.extract_acc_values)

        self.detrend_action = self.createAction("Detrend waveforms", "Move the start of the waveform to the zero Y value", self.detrend_waveforms)

        
        
    def browse_file(self):
        
        
        
        # select the file
        self.file = QFileDialog.getOpenFileName(self, 'Select file', '', 'MSEED files (*.mseed)')[0]
        
        # if no file selected return
        if not self.file:
            return
        
        if 'picked' in  self.file:
            QMessageBox.critical(self, 'Invalid path', 'You cannot browse for an MSEED file in the "picked" folder. Please move your MSEED file outside of the "picked" folder and try again. If the MSEED file is not in the "picked" folder and you still get this error then that means that the program finds the word "picked" in the path of this MSEED file somewhere. Wherever you have the "picked" name in the path, change it.') 
            return
        # every time you browse a file, the folder that this file is in, becomes the "nextfolder"
         
        if pathlib.Path(self.file).parent  != self.nextfolder:
            text = f'The <i>"NEXT"</i> folder is initialized and set to the folder where the selected file is located ({os.path.dirname(pathlib.Path(self.file).parent )}). If you need to re-define it, use the <b><u>Browse</u></b> option again to select a file located to a different folder.'
            QMessageBox.information(self, 'The "NEXT" folder is initialized', text)
            self.nextfolder = pathlib.Path(self.file).parent
        
        # every time you select a file you need to do some initial state before you upload it
        self.initialstate()
        
        # then you can use the following function that reads the mseedf file
        self.readmseed()
        

        

    def get_next_file(self):
        if self.nextfolder:
            
             self.statusbar.showMessage('Getting the next file from the "NEXT" folder...', 3000)
             # the nextfolder is defined in the browse option
             # get all the mseed files in the next folder
             lista = glob.glob( str(self.nextfolder) + '/*mseed' )

              # if the next folder is not empty get the first mseed file and put it equal to self.file
             if  lista:
                  self.file = lista[0]
              
             else:
                  text = f'The "NEXT" folder you have set ({self.nextfolder}) is empty (there are not MSEED files)'
                  QMessageBox.critical(self, '"NEXT" folder empty', text)
                  return

             # every time you select a file you need to do some initial state before you upload it
             self.initialstate()
             
             # then you can use the following function that reads the mseedf ile
             self.readmseed()
             

             
        else:
           
            text = 'the <i>"NEXT"</i> folder is not set. Use the <u><b>Browse</b></u> option to initialize it.'
            QMessageBox.critical(self, 'Folder not initialized', text)
            return
        
        
        
    def send_file_to_notgood_folder(self):
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return
     
        self.statusbar.showMessage("Moving the file to the notgood_folder...", 3000)
        
        text = 'Are you sure you want to move this file to the "mypicker_notgood_files" folder?'
        returnValue = QMessageBox.question(self, 'Confirmation to proceed!', text)
     
        if returnValue == QMessageBox.Yes:
            notgoodfolderpath = MyPickerClass.abs_path_to_parent_of_file / 'mypicker_notgood_files'

            if not os.path.exists(notgoodfolderpath):
                 os.mkdir(notgoodfolderpath) # create the mypicker_notgood_files folder
            

            try:
                 shutil.move(self.file, notgoodfolderpath)
            except Exception as e:
                 QMessageBox.critical(self, 'Cannot move the file to the mypicker_notgood_files folder', str(e))

            pickedpath = MyPickerClass.abs_path_to_parent_of_file / 'picked' / os.path.basename(self.file).split('.')[0]
            picked_record = False # set a variable to check if the file already exists in the picked folder
            if os.path.exists(pickedpath):
                picked_record = True
                # if there is already a file with this record in the picked folder , delete it
                shutil.rmtree(pickedpath)
            
            self.initialstate()
            if picked_record:
                QMessageBox.information(self, 'success!', f'Succesfully moved the file to the "{notgoodfolderpath}" folder and \n deleted the folder {pickedpath} in the "picked" folder')
            else:
                QMessageBox.information(self, 'success!', f'Succesfully moved the file to the "{notgoodfolderpath}" folder.')
                
                
    def send_file_to_notsure_folder(self):
        
        
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return
        
        self.statusbar.showMessage("Moving the file to the notsure_folder...", 3000)
     
        text = 'Are you sure you want to move this file to the "mypicker_for_later" folder?'
        returnValue = QMessageBox.question(self, 'Confirmation to proceed!', text)
     
        if returnValue == QMessageBox.Yes:
            notsurefolderpath = MyPickerClass.abs_path_to_parent_of_file / 'mypicker_for_later'
            
            if not os.path.exists(notsurefolderpath):
                 os.mkdir(notsurefolderpath)
           
            try:
                 shutil.move(self.file, notsurefolderpath)

            except Exception as e:
                 print(e)

            pickedpath = MyPickerClass.abs_path_to_parent_of_file / 'picked' / os.path.basename(self.file).split('.')[0]
            picked_record = False
            if os.path.exists(pickedpath):
                picked_record = True
                shutil.rmtree(pickedpath)
            
            self.initialstate()
            if picked_record:
                QMessageBox.information(self, 'success!', f'Succesfully moved the file to the "{notsurefolderpath}" folder and \n deleted the folder {pickedpath} in the "picked" folder')
            else:
                QMessageBox.information(self, 'success!', f'Succesfully moved the file to the "{notsurefolderpath}" folder.')
                
     
    def save_file(self):
        
        
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return

        if not self.PSarrivals_values['P'] and not self.PSarrivals_values['S']:
             text = "you have not selected any P or S arrival time. You need to select at least one of them to able to use this option!"
             QMessageBox.critical(self, 'No arrivals selected', text)
             return
        
        namefolder = pathlib.Path(self.file).stem

        if not os.path.exists(MyPickerClass.abs_path_to_parent_of_file / 'picked'): # check if the picked folder exists
            os.mkdir(MyPickerClass.abs_path_to_parent_of_file / 'picked')

        if not os.path.exists(MyPickerClass.abs_path_to_parent_of_file / 'picked' / namefolder): # check if the record folder exists in the picked folder
            os.mkdir(MyPickerClass.abs_path_to_parent_of_file / 'picked' / namefolder)


        arrpath = MyPickerClass.abs_path_to_parent_of_file / 'picked' / namefolder / f"{namefolder}_arrivals.txt"
 
        with open(arrpath,"w") as f:          
            if self.PSarrivals_values['P'] and self.PSarrivals_values['S']:
                 f.write("P-arrival S-arrival\n")
                 f.write( f"{self.PSarrivals_values['P']:.3f} {self.PSarrivals_values['S']:.3f}\n" )
            elif self.PSarrivals_values['P']:
                 f.write("P-arrival\n")
                 f.write( f"{self.PSarrivals_values['P']:.3f}\n"  )
            elif self.PSarrivals_values['S']:
                 f.write("S-arrival\n")
                 f.write( f"{self.PSarrivals_values['S']:.3f}\n" )
             
            f.write("\n\n")
            f.write(f"filter-selected : {self.filterselected.text()}\n")
            


        # if you used the browse option then also move the file to the corresponding folder in the picked folder
        if not os.path.exists(MyPickerClass.abs_path_to_parent_of_file / 'picked' / namefolder / os.path.basename(self.file)):
        
            try:
                shutil.move(self.file, MyPickerClass.abs_path_to_parent_of_file / 'picked' / namefolder )
            except Exception as e:
                text = str(e)
                QMessageBox.critical(self, 'Cannot move the MSEED file to the respective folder', text)
                return

        self.initialstate()
        self.statusbar.showMessage("Arrivals saved", 5)
        
        
    
    
    def load_folder(self):
        # select the folder that is created
        self.folder = QFileDialog().getExistingDirectory(self, 'Select a directory')
        
        # if the use hits cancel then return
        if not self.folder:
             return
        
        # the file must have the _arrivals file in it (the arrivals). If it does not then error
        get_arrivals_file = glob.glob(self.folder + "/*_arrivals.txt")
        get_mseed_file = glob.glob(self.folder + "/*mseed")
        
        if len(get_arrivals_file) !=1 or len(get_mseed_file) !=1:
            QMessageBox.critical(self, 'Invalid files in the folder', 'Since you want to load a folder with already picked arrivals, it must have one file with the arrivals (file ending with _arrivals) and one with ".mseed" extension file. Please re-pick the arrivals to the mseed file and delete this folder.')
            return
     
        
 
  
        self.initialstate()

        try:
        # open the arrivals file to get the arrivals
            with open(get_arrivals_file[0],'r') as f:
                ff = f.readlines()
                if len(ff[1].split()) == 2:
                    self.PSarrivals_values = {'P':float(ff[1].split()[0]) , 'S':float(ff[1].split()[1])}
                    self.btPrem.show()
                    self.btSrem.show()
                    self.rbP.setDisabled(True)
                    self.rbS.setDisabled(True)
               
                elif len(ff[1].split()) == 1 and 'S-arrival' in ff[0]:
                    self.PSarrivals_values = {'P':None , 'S':float(ff[0].split()[0])}
                    self.rbP.setDisabled(False)
                    self.rbS.setDisabled(True)
                    self.btPrem.hide()
                    self.btSrem.show()
                    self.rbP.setChecked(True)
                    self.rbS.setChecked(False)
                    
                elif len(ff[1].split()) == 1 and 'P-arrival' in ff[0]:
                     self.PSarrivals_values = {'P':float(ff[1].split()[0]) , 'S':None}
                     self.rbP.setDisabled(True)
                     self.rbS.setDisabled(False)
                     self.btPrem.show()
                     self.btSrem.hide()
                     self.rbP.setChecked(False)
                     self.rbS.setChecked(True)
                       

        except Exception as e:
            text = str(e)
            QMessageBox.critical(self, 'Cannot read the arrivals file', text)
            return
          
  
        
        # addign the mseed file to the self.file variable
        self.file = get_mseed_file[0]
        
        self.p1.setTitle(self.file)

        self.dt = read(self.file)
        
        try:
            self.dt = self.dt.detrend("linear")
        except:
            pass

        
        self.dt_initial = self.dt.copy()
        self.min_times_value = self.dt[0].times().min()
        self.max_times_value = self.dt[0].times().max()
        self.start_dt = self.dt[0].stats.starttime
        self.compos = [tr.stats.channel for tr in self.dt]
        self.rec_name = pathlib.Path(self.file).stem
 
   
        # if the self.plotdataitems_list list (contains the PlotDataItems) is empty (this happends when you run the program) then create the PlotDataItems else change just he x and y data
        if not self.plotdataitems_list:
        
            for n,mseed in enumerate(self.dt):
                z=self.plotwidgets_list[n].plot(x=mseed.times(), y=mseed.data,  name=f'Channel : {mseed.stats.channel}')
                self.plotdataitems_list.append(z) # insert the PlotDataItems return (z) in the self.plotdataitems_list list
                self.plotwidgets_list[n].setXRange(np.nanmin(mseed.times()),np.nanmax(mseed.times())) # set x limit
                self.plotwidgets_list[n].setYRange(np.nanmin(mseed.data),np.nanmax(mseed.data)) # set y limit
                z.setPen(self.pen_plotdataitem)
                

        else:
          
            for n,mseed in enumerate(self.dt):
                self.plotdataitems_list[n].setData(mseed.times(),mseed.data) 
                self.plotwidgets_list[n].setXRange(np.nanmin(mseed.times()),np.nanmax(mseed.times()))
                self.plotwidgets_list[n].setYRange(np.nanmin(mseed.data),np.nanmax(mseed.data))
                
        self.p1.setTitle(self.file)
        
        
        for rb in self.filtersGroup.buttons():
            rb.setDisabled(False)
            
        self.initial_filter.setChecked(True)
        
        self.filtleft.setDisabled(False)
        self.filtright.setDisabled(False)
        

        text_waves = []

        if self.PSarrivals_values['P']:
              text_waves.append('P')

        if self.PSarrivals_values['S']:
              text_waves.append('S')
             

        for wv in text_waves:

             for i in range(len(self.dt)):
          

                  pick = self.plotwidgets_list[i].addLine(x=self.PSarrivals_values[wv])
                  
                  pick.setMovable(True)
                  pick.sigPositionChanged.connect(self.inflinemoved)

                  self.symbol_text = pg.TextItem(wv)

                  self.plotwidgets_list[i].addItem(self.symbol_text)

                  self.symbol_text.setPos(self.PSarrivals_values[wv],0)
                  self.PSvert_lines_dictionary[wv].append(pick)
                  self.PSsymbols_dictionary[wv].append(self.symbol_text)
                  
                  pick.setPen(self.pen_vert_lines)
                  self.symbol_text.setHtml('<b style="color: ' + self.pen_symbol.color().name() + '; font-size:' + str(self.pen_symbol.width()) +'px>' + wv + '</b>')
               
                  
                  
                  
                  

    def readmseed(self):
       
        try:
            self.dt = read(self.file)
        except Exception as e:
            QMessageBox.critical(self, "Can't read the mseed file", str(e))
            self.dt = None
            return

        
        self.statusbar.showMessage(f"Read the MSEED file {self.file}", 0)
        

        # here i just save the initial self.dt in a variable because maybe the user will change it in the trim section
        self.dt_initial = self.dt.copy()
        self.min_times_value = self.dt[0].times().min()
        self.max_times_value = self.dt[0].times().max()
        self.start_dt = self.dt[0].stats.starttime
        self.compos = [tr.stats.channel for tr in self.dt]
        self.rec_name = pathlib.Path(self.file).stem

        
        # if the self.plotdataitems_list list (contains the PlotDataItems) is empty (this happends when you run the program) then create the PlotDataItems else change just he x and y data
        if not self.plotdataitems_list:
        
            for n,mseed in enumerate(self.dt):
                z=self.plotwidgets_list[n].plot(x=mseed.times(), y=mseed.data,  name=f'Channel : {mseed.stats.channel}')
                self.plotdataitems_list.append(z) # insert the PlotDataItems return (z) in the self.plotdataitems_list list
                self.plotwidgets_list[n].setXRange(np.nanmin(mseed.times()),np.nanmax(mseed.times())) # set x limit
                self.plotwidgets_list[n].setYRange(np.nanmin(mseed.data),np.nanmax(mseed.data)) # set y limit
                z.setPen(self.pen_plotdataitem)
                
                

        else:
          
            for n,mseed in enumerate(self.dt):
                self.plotdataitems_list[n].setData(mseed.times(),mseed.data) 
                self.plotwidgets_list[n].setXRange(np.nanmin(mseed.times()),np.nanmax(mseed.times()))
                self.plotwidgets_list[n].setYRange(np.nanmin(mseed.data),np.nanmax(mseed.data))
                
        self.p1.setTitle(self.file)
       
        self.rbP.setDisabled(False)
        self.rbS.setDisabled(False)
        

        for rb in self.filtersGroup.buttons():
            rb.setDisabled(False)
            
        
        self.filtleft.setDisabled(False)
        self.filtright.setDisabled(False)
        
        self.rbP.setChecked(True)
        self.initial_filter.setChecked(True)
        
        
        
    
    def clicked_event_on_graph(self,event):
        


        if not self.dt or not self.xx:
            return
        
        xdata = self.xx



        if event.double() and int(event.button()) == 1:
            
            if self.PSvert_lines_dictionary['P'] and self.PSvert_lines_dictionary['S']:
                return
              
            if self.rbP.isChecked() :
                radiochecked = 'P'     
                self.rbS.setChecked(True)
                self.rbP.setDisabled(True)
                self.btPrem.show()
                self.statusbar.showMessage("Inserted the P arrival", 0)

            else:
                radiochecked = 'S'
                self.rbP.setChecked(True)
                self.rbS.setDisabled(True)
                self.btSrem.show()
                self.statusbar.showMessage("Inserted the S arrival", 0)
   
            self.PSarrivals_values[radiochecked] = xdata
         
            for i in range(len(self.dt)):
        
                pick = self.plotwidgets_list[i].addLine(x=xdata)
                pick.setMovable(True)
                pick.sigPositionChanged.connect(self.inflinemoved)
       
                self.symbol_text = pg.TextItem(radiochecked)
                self.plotwidgets_list[i].addItem(self.symbol_text)
                self.symbol_text.setPos(self.xx,0)
                self.PSvert_lines_dictionary[radiochecked].append(pick)
                self.PSsymbols_dictionary[radiochecked].append(self.symbol_text)
                
                pick.setPen(self.pen_vert_lines)
                print(self.pen_symbol.width())
                self.symbol_text.setHtml('<b style="color: ' + self.pen_symbol.color().name() + '; font-size:' + str(self.pen_symbol.width()) +'px">' + radiochecked + '</b>')
             
    
                 
                 

    def findinaxes(self, evt):
        if not self.dt:
            return

        height = self.graphlayout.geometry().height()
        limit = (height-30)/3
        mousepos = evt[0].y()


        if mousepos <= limit :
            self.inaxes = self.p1
            
        elif mousepos <= 2*limit:
            self.inaxes = self.p2
          
        elif mousepos <= 3*limit+50:
            self.inaxes = self.p3
          
        else:
             return

        self.xx = self.inaxes.vb.mapSceneToView(evt[0]).x()

   
    def removepicks(self):
        btclicked = self.sender().text()
        PORS = btclicked.split()[1] #apla epeidh to koumpoi ekei px Del. P gia text, to kanw split gia na parw to P h to S
        for n in range(len(self.dt)):
            self.plotwidgets_list[n].getViewBox().removeItem(self.PSvert_lines_dictionary[PORS][n])
            self.plotwidgets_list[n].getViewBox().removeItem(self.PSsymbols_dictionary[PORS][n])
          
        self.PSvert_lines_dictionary[PORS] = []
        self.PSsymbols_dictionary[PORS] = []
        if btclicked == 'Del. P':
            self.rbP.setChecked(True)
            self.btPrem.hide()
            self.PSarrivals_values['P'] = ""
            self.rbP.setDisabled(False)
            self.statusbar.showMessage("Deleted the P arrival", 0)
           
          
        elif btclicked == 'Del. S':
            self.rbS.setChecked(True)
            self.btSrem.hide()
            self.PSarrivals_values['S'] = ""
            self.rbS.setDisabled(False)
            self.statusbar.showMessage("Deleted the S arrival", 0)
              

    def inflinemoved(self, evt):

        indfoundP = 'notfound' # arxikopoiw to index gia th lista dictPSpicks twn P arrival
        indfoundS = 'notfound' # arxikopoiw to index gia th lista dictPSpicks twn S arrival
        self.statusbar.showMessage(f"Setting the X value of the vertical line to: {evt.x():.2f}", 0)
        
        if self.PSvert_lines_dictionary['P']:
            for i in range(len(self.PSvert_lines_dictionary['P'])): 
                if self.PSvert_lines_dictionary['P'][i] == evt:
                    indfoundP = i
                    break

            if indfoundP != 'notfound': 
                self.PSarrivals_values['P'] = evt.x()
              
                for ptext in self.PSsymbols_dictionary['P']:
                    ptext.setPos(self.PSarrivals_values['P'], 0)
                
                for k in range(len(self.PSvert_lines_dictionary['P'])):
                    if k != indfoundP:
                        self.PSvert_lines_dictionary['P'][k].setValue(self.PSarrivals_values['P'])
                      

        if self.PSvert_lines_dictionary['S']:
             for i in range(len(self.PSvert_lines_dictionary['S'])):
                  if self.PSvert_lines_dictionary['S'][i] == evt:
                       indfoundS = i
                       break

             if indfoundS != 'notfound':

                  self.PSarrivals_values['S'] = evt.x()
              
                  for stext in self.PSsymbols_dictionary['S']:
                       stext.setPos(self.PSarrivals_values['S'], 0)
                  
              
                  for k in range(len(self.PSvert_lines_dictionary['S'])):
                       if k != indfoundS:
                            self.PSvert_lines_dictionary['S'][k].setValue(self.PSarrivals_values['S'])
                            
                            
                            
                            
    
    def setfilters(self):
        
        
        radioBtn = self.sender()
        radioselected = radioBtn.text()

        self.filterselected = radioBtn

        if radioselected== '<10':
             dtfiltered = [dt_10.copy().filter('lowpass',freq=10) for dt_10 in self.dt]
        elif radioselected == '0.7-10':
             dtfiltered = [dt07_10.copy().filter('bandpass',freqmin=0.7,freqmax=10) for dt07_10 in self.dt]
        elif radioselected == '0.7-5':
             dtfiltered = [dt07_5.copy().filter('bandpass',freqmin=0.7,freqmax=5) for dt07_5 in self.dt]
        elif radioselected == '1-3':
             dtfiltered = [dt1_3.copy().filter('bandpass',freqmin=1,freqmax=3) for dt1_3 in self.dt]
        elif radioselected == '1-10':
             dtfiltered = [dt1_10.copy().filter('bandpass',freqmin=1,freqmax=10) for dt1_10 in self.dt]
        elif radioselected == '1-5':
             dtfiltered = [dt1_5.copy().filter('bandpass',freqmin=1,freqmax=5) for dt1_5 in self.dt]
        elif radioselected == '>0.5':
             dtfiltered = [dt_05.copy().filter('highpass',freq=0.5) for dt_05 in self.dt]
        elif radioselected == 'initial':
             dtfiltered = [tr for tr in self.dt]
             
        for n,i in enumerate(self.dt):
            self.plotdataitems_list[n].setData(np.array(dtfiltered[n].times()), np.array(dtfiltered[n].data))
            if self.chkbxzoomfilter.isChecked():
                 self.plotwidgets_list[n].setXRange(np.nanmin(dtfiltered[n].times()),np.nanmax(dtfiltered[n].times()), padding=0)
                 self.plotwidgets_list[n].setYRange(np.nanmin(dtfiltered[n].data),np.nanmax(dtfiltered[n].data), padding=0)
        self.statusbar.showMessage(f"Applied filter: {radioselected} Hz", 0)
        
        
 

    def keyPressEvent(self, event):

        ax = self.inaxes
    
        if ax == self.p1:
             axno = 0
        elif ax == self.p2:
             axno = 1
        elif ax == self.p3:
             axno = 2

        if event.key() == Qt.Key_N:
            self.save_file()


        elif event.key() == Qt.Key_M:
            self.get_next_file()


        elif event.key() == Qt.Key_J:
            self.send_file_to_notgood_folder()

        elif event.key() == Qt.Key_W:
            movey = np.nanmax(np.absolute(self.dt[axno].data))/10
            ax.setYRange(ax.getAxis('left').range[0]+movey, ax.getAxis('left').range[1]-movey, padding=0)
            
        elif event.key() == Qt.Key_S:
            movey = np.nanmax(np.absolute(self.dt[axno].data))/10
            ax.setYRange(ax.getAxis('left').range[0]-movey, ax.getAxis('left').range[1]+movey, padding=0)
            
        elif event.key() == Qt.Key_D:
            movex = np.nanmax(self.dt[axno].times())/20
            ax.setXRange(ax.getAxis('bottom').range[0]+movex, ax.getAxis('bottom').range[1]+movex, padding=0)
            
        elif event.key() == Qt.Key_A:
            movex = np.nanmax(self.dt[axno].times())/20
            ax.setXRange(ax.getAxis('bottom').range[0]-movex, ax.getAxis('bottom').range[1]-movex, padding=0)
            
            
            
    def filterhandenterpressed(self):
        

        leftvalue = self.filtleft.text()
        rightvalue = self.filtright.text()
        
        if leftvalue and rightvalue:
            try:
                leftvalue = float(leftvalue)
                rightvalue = float(rightvalue)
            except:
                QMessageBox.critical(self, 'Invalid Input', "The values that you inserted are not numerical.")
                return
        elif leftvalue and not rightvalue: 
            try:
                leftvalue = float(leftvalue)
            except:
                QMessageBox.critical(self, 'Invalid Input', "The low corner frequency on the left entry is not numerical!")
                return
        elif rightvalue and not leftvalue:
            try:
                rightvalue = float(rightvalue)
            except:
                QMessageBox.critical(self, 'Invalid Input', "The high corner frequency on the right entry is not numerical!")
                return
        else:
            QMessageBox.critical(self, 'Invalid Input', "You must insert values for the low and/or the high corner frequency!!")
            return
        
        if leftvalue:
            if leftvalue<0.01 or leftvalue > 100:
                QMessageBox.critical(self, 'Invalid frecuenty value', 'The frequency range values that you can insert is from 0.01 to 100 Hz !')
                return
        
        if rightvalue:
            if rightvalue<0.01 or rightvalue > 100:
                QMessageBox.critical(self, 'Invalid frecuenty value', 'The frequency range values that you can insert is from 0.01 to 100 Hz !')
                return
        

        try:
          
            if leftvalue and rightvalue:
                 dtfiltered = [dtband.copy().filter('bandpass',freqmin=float(leftvalue),freqmax=float(rightvalue)) for dtband in self.dt]
                 self.statusbar.showMessage(f"Applied bandpass filter: {leftvalue}-{rightvalue} Hz", 0)
            elif leftvalue:
                 dtfiltered = [dthigh.copy().filter('highpass',freq=float(leftvalue)) for dthigh in self.dt]
                 self.statusbar.showMessage(f"Applied highpass filter: {leftvalue} Hz", 0)
            elif rightvalue:
                 dtfiltered = [dtlow.copy().filter('lowpass',freq=float(rightvalue)) for dtlow in self.dt]
                 self.statusbar.showMessage(f"Applied lowpass filter: {rightvalue} Hz", 0)
               
            for n,i in enumerate(self.dt):
                 self.plotdataitems_list[n].setData(np.array(dtfiltered[n].times()), np.array(dtfiltered[n].data))
                 
        except Exception as e:

            QMessageBox.critical(self, 'Invalid input', str(e))
            return
        
        
        
        
          
           
    def resetlimits(self):
      
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return

        for i in range(len(self.dt)):
             time_values = self.dt[i].times()
             data_values = self.dt[i].data
             self.plotwidgets_list[i].setXRange(np.nanmin(time_values), np.nanmax(time_values))
             self.plotwidgets_list[i].setYRange(np.nanmin(data_values), np.nanmax(data_values))
        
        self.statusbar.showMessage("The X and Y axis have been reset from the minimum to the maximum values", 0)
        
        
    def add_grid(self):
        
        if not self.chkbxgrid.isChecked():
            self.statusbar.showMessage("The grid has been removed", 0)
            for n,i in enumerate(self.plotwidgets_list):
                i.removeItem(self.gridlist[n])
        else:
            self.statusbar.showMessage("The grid is inserted", 0)
            for n,i in enumerate(self.plotwidgets_list):
                i.addItem(self.gridlist[n])
        
        
        
    def toogle_y_axis(self):
        if self.chkbxmoveyaxis.isChecked():
            self.statusbar.showMessage("The Y axis pad is locked", 0)
            for n,i in enumerate(self.plotwidgets_list):
                i.getViewBox().setMouseEnabled(x=True,y=False)
        else:
            self.statusbar.showMessage("The Y axis pad is unlocked", 0)
            for n,i in enumerate(self.plotwidgets_list):
                i.getViewBox().setMouseEnabled(x=True,y=True)
        

    
 
    
    def manual_function(self):
        self.manual_object = ProgramTutorial(self.dpi)
                
        self.manual_object.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.manual_object.resize(int(self.dpi * self.inches_windows*2), int(self.dpi * self.inches_windows/1.4))
        self.manual_object.show()
    
   
    def txttomseed(self):
        self.txttomseed_object = txtToMseedClass(self.dpi)
                
        self.txttomseed_object.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.txttomseed_object.resize(1100, 900)
        self.txttomseed_object.show()
    

    def defshortcuts(self):
        
        self.shortcuts_object = ShortcutsClass(self.dpi)
        self.shortcuts_object.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.shortcuts_object.resize(int(self.dpi * self.inches_windows/1.5), int(self.dpi * self.inches_windows/1.4))
        self.shortcuts_object.show()



    def arrivals_to_excel(self):
        
        QMessageBox.information(self, 'Select folder', 'Select a folder that contains the program generated, arrival files (the ones ending with <code>"_arrivals.txt"</code>) and extract them to an excel file. The files can be anywhere in the folder, that means in folders inside another folders etc.')
        
        
        self.folder_data = str(QFileDialog().getExistingDirectory(self, 'Select a directory'))
        
        if not self.folder_data:
            return
        
        self.statusbar.showMessage("Loading the folder...", 3000)
                         
        arrival_files = glob.glob(self.folder_data + '/**/*arrivals.txt', recursive=True)
        
        if not arrival_files:
            QMessageBox.critical(self, 'Empty folder', 'The folder you selected is empty')
            return
        
        df_arr = pd.DataFrame
        
        for arx in arrival_files:
            rec_name = pathlib.Path(arx).stem.rsplit('_', 1)[0]
            
            f = open(arx, 'r')
            arrival_symbols = f.readline()
            arrivals = f.readline()
            arrivals = [float(arr) for arr in arrivals.split()]
            
            if len(arrivals) == 2:
                ser = pd.Series([rec_name, arrivals[0], arrivals[1]], index=['record', 'P_arrival', 's_arrival']).to_frame().T
            elif len(arrivals) == 1 and 'P-arrival' in arrival_symbols:
                ser = pd.Series([rec_name, arrivals[0], '-'], index=['record', 'P_arrival', 's_arrival']).to_frame().T
            elif len(arrivals) == 1 and 'S-arrival' in arrival_symbols:
                ser = pd.Series([rec_name, '-', arrivals[0]], index=['record', 'P_arrival', 's_arrival']).to_frame().T
                
                
            if df_arr.empty:
                df_arr = ser
            else:
                df_arr = pd.concat([df_arr, ser])
                
        df_arr.to_excel(MyPickerClass.abs_path_to_parent_of_file / 'arrivals.xlsx', index=None)
        QMessageBox.information(self, 'Extracted to excel', f'Found {len(df_arr)} file(s). The arrivals are extracted to a file called "arrivals.xlsx" in the folder: {MyPickerClass.abs_path_to_parent_of_file}')
        self.statusbar.showMessage(f'Extracted the arrivals to the path: {MyPickerClass.abs_path_to_parent_of_file / "arrivals.xlsx"}', 0)
                         
              
          
    def myprogram_info(self):

        self.program_info_object = ProgramInfoClass(self.dpi)
        print(int(self.dpi * self.inches_windows))
        self.program_info_object.resize(int(self.dpi * self.inches_windows * 1.5), int(self.dpi * self.inches_windows/1.2))
        self.program_info_object.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.program_info_object.show()
        
        
    def trim_waveforms(self):
        
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return
        
        # devide the max value by 4 to split it into 4 equal parts ans place the initial region
        part = self.max_times_value/4
        left_initial_region_pos = self.min_times_value + part
        right_initial_region_pos = self.max_times_value - part
        
        self.widget_trim = QWidget()
        self.widget_trim.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.verLayoutTrim = QVBoxLayout()
        self.horLayoutTrim_lb = QHBoxLayout()
        self.horLayoutTrim_en = QHBoxLayout()
        self.horLayoutTrim_bt = QHBoxLayout()
        
        QMessageBox.information(self, 'Trimming the waveforms', '<h2>Select the left and right limits to trim the waveforms using the two vertical lines</h2><b><p>Dont worry that the lines are just on the first window. The trimming will be applied on all the windows!!</p></p>')

        self.lb_not_x = QLabel('<b>IF YOU JUST WANT TO CLOSE THIS WINDOW <br>PRESS THE <u><b style="color:red">CANCEL</b></u> BUTTON, NOT THE <b style="color:red">X</b>>')
        
        self.lb_title = QLabel('<h1>Use the lines on the <br>graph to trim</h1')


        self.bt_done_trim = QPushButton('done')
        self.bt_done_trim.clicked.connect(self.apply_trim)
        
        self.bt_cancel_trim = QPushButton('Cancel')
        self.bt_cancel_trim.clicked.connect(self.cancel_trim_func)
        
        
        self.left_label_trim = QLabel("left limit")
        self.right_label_trim = QLabel("right limit")
        

        self.left_entry_trim = QLineEdit(f"{left_initial_region_pos:.2f}")
        self.right_entry_trim = QLineEdit(f"{right_initial_region_pos:.2f}")
        self.left_entry_trim.setReadOnly(True)
        self.right_entry_trim.setReadOnly(True)

        
        self.horLayoutTrim_lb.addWidget(self.left_label_trim)
        self.horLayoutTrim_lb.addWidget(self.right_label_trim)
        
        self.horLayoutTrim_bt.addWidget(self.bt_done_trim)
        self.horLayoutTrim_bt.addWidget(self.bt_cancel_trim)
        
        self.horLayoutTrim_en.addWidget(self.left_entry_trim)
        self.horLayoutTrim_en.addWidget(self.right_entry_trim)
        
        self.verLayoutTrim.addWidget(self.lb_title)
        self.verLayoutTrim.addLayout(self.horLayoutTrim_lb)
        self.verLayoutTrim.addLayout(self.horLayoutTrim_en)
        self.verLayoutTrim.addWidget(self.lb_not_x)
        self.verLayoutTrim.addStretch(1)
        self.verLayoutTrim.addLayout(self.horLayoutTrim_bt)
        
        self.widget_trim.setLayout(self.verLayoutTrim)
        
      
        
        
        self.regionItem = pg.LinearRegionItem(
            values=(left_initial_region_pos, right_initial_region_pos), 
            orientation='vertical', 
            movable=True, 
            bounds=(self.min_times_value, self.max_times_value), span=(0, 1), 
            swapMode='block')
        self.regionItem.sigRegionChanged.connect(self.region_moved)
        
        self.plotwidgets_list[0].addItem(self.regionItem)
        
      
        if pathlib.Path(self.sshFile).exists():
            
            with open(self.sshFile,"r") as fh:
                styles = fh.read()
                styles = styles.replace('40px' , f'{int(self.inches_selected * self.dpi)}px')
                self.widget_trim.setStyleSheet(styles)
       
        
        
        self.widget_trim.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.widget_trim.show()
        
    def region_moved(self, evt):
        left_lim, right_lim = self.regionItem.getRegion()
        self.left_entry_trim.setText(f"{left_lim:.2f}")
        self.right_entry_trim.setText(f"{right_lim:.2f}")
        
        
    def cancel_trim_func(self):
        self.plotwidgets_list[0].removeItem(self.regionItem)
        self.widget_trim.deleteLater()
        self.widget_trim = None
        
          
    def apply_trim(self):
        self.statusbar.showMessage("Applying trim...", 5000)
        left_lim, right_lim = float(self.left_entry_trim.text()),  float(self.right_entry_trim.text())
        self.dt = [tr.trim(starttime=self.start_dt+left_lim, endtime=self.start_dt+right_lim) for tr in self.dt]
        
        
        for n,i in enumerate(self.dt):
            self.plotdataitems_list[n].setData(np.array(self.dt[n].times()), np.array(self.dt[n].data))

        
        self.plotwidgets_list[0].removeItem(self.regionItem)
        self.widget_trim.deleteLater()
        self.widget_trim = None
        
        
    def extract_acc_values(self):
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return
        
        # get the values of the acceleration (if you applied filter or trim, it does count!)
        df_acc = pd.DataFrame({"Channel " + tr.stats.channel : tr.data for tr in self.dt})
        
        
        QMessageBox.information(self, 'Extracting values', 'The acceleration values are extracted to a file in the current path (where this python file is located) with a prefix of "acc_values" and ending with the name of the record file.')
       
        df_acc.to_excel(MyPickerClass.abs_path_to_parent_of_file / f'acc_values_{self.rec_name}.xlsx', index=None)
            
        
    def show_waveform_info(self):
        
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return
        
        
      
        self.widget_waveform_info = ShowWaveformInfo(self.dpi, self.dt)
        self.widget_waveform_info.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.widget_waveform_info.resize(int(self.dpi * self.inches_windows * 1.5), int(self.dpi * self.inches_windows/1.2))
        self.widget_waveform_info.show()

        
        
    def zoom_filter_checked(self, checked):
        if checked:
            self.statusbar.showMessage('Y-axis now fluctuates from the minimum to the maximum value when a filter is applied')
        else:
            self.statusbar.showMessage('Y-axis now is no changing when a filter is applied')


    def detrend_waveforms(self):
        if not self.dt:
            text = "You haven't loaded any waveform to use this option."
            QMessageBox.critical(self, 'No file found', text)
            return
        
        self.dt.detrend("linear")
        
        for n,tr in enumerate(self.dt):
            self.plotdataitems_list[n].setData(np.array(tr.times()), np.array(tr.data))
            self.plotwidgets_list[n].setYRange(np.nanmin(tr.data),np.nanmax(tr.data), padding=0)
        self.statusbar.showMessage("A simple detrend function is applied", 0)
        QMessageBox.information(self, 'Detrend applied', 'Detrend method was applied succesfully')
        
    
    def set_theme(self, option):


        randomfile = str(MyPickerClass.abs_path_to_parent_of_file) + f'/templates/{option}.qss'
        with open(randomfile, 'r') as fr:
            ff = fr.readlines()[1:8]
            print(ff[0])
            wavecolor = ff[0].split(':')[1].strip()
            graphcolor = ff[1].split(':')[1].strip()
            # figurecolor = ff[2].split(':')[1].strip()
            linecolor = ff[4].split(':')[1].strip()
            symbolcolor = ff[5].split(':')[1].strip()
            
           
        
        # for pw in self.plotwidgets_list:
        #     pw.getViewBox().setBackgroundColor(graphcolor)
        self.graphlayout.setBackground(graphcolor)
        self.set_pens('plotdataitems', wavecolor)
        self.set_pens('verticallines', [linecolor, int(self.inches_selected_pg_vert_ln * self.dpi)])
        self.set_pens('symbols', [symbolcolor, int(self.inches_selected_pg_sym * self.dpi)])
        
        self.sshFile = str(MyPickerClass.abs_path_to_parent_of_file) + f'/templates/{option}.qss'
        print(self.sshFile)
        if pathlib.Path(self.sshFile).exists():
            
            with open(self.sshFile,"r") as fh:
                styles = fh.read()

                styles = styles.replace('40px' , f'{int(self.inches_selected * self.dpi)}px')
         
                self.setStyleSheet(styles)
            

        

        




if __name__ == '__main__':

    
    app = QApplication(sys.argv)
    from screeninfo import get_monitors

    for mon in get_monitors():
        if mon.is_primary:
            screen_width_length_mm = mon.width_mm
            screen_width_length_cm = screen_width_length_mm / 10
            screen_width_length_in = screen_width_length_cm  * 0.393701
            width_number_of_pixels = mon.width
            dpi = width_number_of_pixels / screen_width_length_in
          


    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    #     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    #     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    picker_obj = MyPickerClass(dpi)
    # picker_obj.resize(1200, 800)
    
    

    picker_obj.show()
    app.exec_()
    
   