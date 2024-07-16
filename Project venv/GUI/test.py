import sys 
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import numpy as np
import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore  import Qt
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure 

class MlpCanvas(FigureCanvasQTAgg):
    def __init__(self , parent=None , width=5 , height=4 , dpi=100):
        fig = Figure(figsize=(width , height),dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MlpCanvas, self).__init__(fig)
class MainWindow(QMainWindow):
    
    def __init__(self): 
        super(MainWindow ,self).__init__()
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(963, 629)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_4.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_4.addWidget(self.pushButton)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.MplWidget = MplWidget(self.centralwidget)
        self.MplWidget.setObjectName("MplWidget")
        self.verticalLayout_5.addWidget(self.MplWidget)
        self.verticalLayout_4.addLayout(self.verticalLayout_5)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_3.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_3.addWidget(self.checkBox_3)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_3.addWidget(self.checkBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4.addWidget(self.widget)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.MplWidget_2 = MplWidget(self.centralwidget)
        self.MplWidget_2.setObjectName("MplWidget_2")
        self.verticalLayout_6.addWidget(self.MplWidget_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.MplWidget_3 = MplWidget(self.centralwidget)
        self.MplWidget_3.setObjectName("MplWidget_3")
        self.verticalLayout_7.addWidget(self.MplWidget_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_7)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 963, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton, self.checkBox_2)
        MainWindow.setTabOrder(self.checkBox_2, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.checkBox_3)
        MainWindow.setTabOrder(self.checkBox_3, self.pushButton_2)
        #dividing time axes based on state
        
        
    def web(self): #returns numpy  BE , BC , BPIx , BPIz
        data = np.random.randint(0,100 , size=(14400,114))
        array = np.arange(0, 14400).reshape(-1,1)
        concat_data =  np.hstack((array , data))
        self.BE = concat_data[:,1]
        self.BC = concat_data[:,2]
        self.TI = concat_data[:,0]
        self.BPIx = concat_data[:,3:59]
        # print(self.TI)
        # print(array)
        print(self.BPIx.shape)
        self.BPIz = concat_data[:,59:115]
        print(self.BPIz.shape)
        print("data loaded")
       
    def plotter(self):
        
        #matplotlib
        # Plotting energy and current
        self.p = self.canvas.axes
        self.p.clear()
        self.p.plot(self.TI , self.BE , label = 'Beam Energy' , color = 'r' , marker='o' )
        self.p.plot(self.TI , self.BC , label = 'Beam Current' , color = 'b' , marker='x' )
        
        self.p.set_xlabel('Time(in units)')
        self.p.set_ylabel('Beam parameters')
        self.p.set_title('beam parameters v/s time')        
        
        self.p.legend()
        self.p.grid(True)
        self.canvas.draw()
        
        x = self.TI
        y = self.BE
        a = 20
        b = 2500
        list = x[(y>=a)&(y<=b)] 
        self.ramp_start = list[0]
        self.ramp_stop  = list[-1]
        
        
        #plotting BPIx BPIz
        
           
   
    def beam_state_selector(self): # it return new_TI based on beam_state value 
        selected_parts = []
        
        self.part1 = self.TI[:self.ramp_start]
        self.part2 = self.TI[self.ramp_start:self.ramp_stop]
        self.part3 = self.TI[self.ramp_stop:]
        # Collect the parts in order based on checkbox state
        if self.checkbox1.checkState() == Qt.Checked:
            selected_parts.append(self.part1)
        if self.checkbox2.checkState() == Qt.Checked:
            selected_parts.append(self.part2)
        if self.checkbox3.checkState() == Qt.Checked:
            selected_parts.append(self.part3)

        # Concatenate the selected parts
        new_TI = [item for sublist in selected_parts for item in sublist]
        new_TI_arr = np.array(list(set(new_TI)))
        return new_TI_arr
    def plot_i_th_BPI(self , i,state):
        if state == 2 :
            print(f"{i} checked")     
            self.i_func(i,1)
        else:
            print(f"{i} unchecked")
            self.i_func(i,0)
    def i_func( self,i ,state):      #plotting the ith bpi and getting time index from beam_state_selector func

        # color_ = self.random_color()
        if state:
           self.BPIx_canvas.axes.clear() 
           self.BPIz_canvas.axes.clear()
           print(f"new_TI : {self.beam_state_selector().shape}")
           x_= self.BPIx
           x = x_[self.beam_state_selector()]
           z_= self.BPIz
           z = z_[self.beam_state_selector()]
           print(f"BPIx : {x.shape}")
           print(f"BPIz : {z.shape}")
           self.BPIx_canvas.axes.plot(self.beam_state_selector() , x[:,i] , label = f"{i+1}", color = 'r')
           self.BPIz_canvas.axes.plot(self.beam_state_selector() , z[:,i] , label = f"{i+1}", color = 'r')
        # # pass
                        
    def toggle_collapse(self ,checked):
        if checked:
            self.scroll_area.hide()
            self.toggle_button.setText("Expand")
        else:
            self.scroll_area.show()
            self.toggle_button.setText("Collapse")
            
        
app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()        