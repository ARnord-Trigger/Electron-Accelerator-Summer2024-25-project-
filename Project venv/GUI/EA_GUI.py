import sys 
import matplotlib 
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5.QtCore  import Qt
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure 

class MlpCanvas(FigureCanvasQTAgg):
    def __init__(self , parent=None , width=5 , height=4 , dpi=100):
        fig = Figure(figsize=(width , height),dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MlpCanvas, self).__init__(fig)
class MainWin(QMainWindow):
    
    def __init__(self): 
        super(MainWin ,self).__init__()
        
        self.setWindowTitle("EA_GUI")
        
        # self.BE = np.array([])
        # self.BC = np.array([])
        # self.TI = np.array([])
        # self.BPIx = np.array([[],[]])
        # self.BPIz = np.array([[],[]])
        # self.ramp_start = 0
        # self.ramp_stop = 0
        # self.part1 = np.array([])
        # self.part2 = np.array([])
        # self.part3 = np.array([])
        self.new_TI = np.array([])
        
        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        #create a matplotlib canvas
        self.canvas = MlpCanvas(self , width = 5, height=  4 , dpi=100)
        self.BPIx_canvas = MlpCanvas(self , width =4 , height=4 , dpi = 100)
        self.BPIz_canvas = MlpCanvas(self , width =4 , height=4 , dpi = 100)
        
        
        
        # creating layout
        main_layout = QVBoxLayout()
        CBlayout = QVBoxLayout()#for checkbox
        BBC_layout = QHBoxLayout() # button button checkbox
        BPI_plots_layout= QHBoxLayout() #BPIx BPIz are added to this layout
        BPI_list_layout = QVBoxLayout()     
        BPI_layout = QVBoxLayout()# contains BPI list and BPIPLots layout
        plots_layout  = QHBoxLayout()
        
        #BPI list
        #collapsible box
        self.BPI_list_box = QGroupBox("BPI NO.")
        BPI_layout.addWidget(self.BPI_list_box)
        self.BPI_list_box.setLayout(BPI_list_layout)
        # create a button to toggle the collapse
        self.toggle_button = QPushButton("Collapse")
        self.toggle_button.setCheckable(True)
        self.toggle_button.clicked.connect(self.toggle_collapse)
        BPI_list_layout.addWidget(self.toggle_button)
        #create a scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        BPI_list_layout.addWidget(self.scroll_area)
        #create a widget for the scroll aree content
        scroll_content = QWidget()
        self.scroll_area.setWidget(scroll_content)
        #create a layout for the scroll area content 
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)
        #create 56 CBs
        for i in range(56):
            self.checkbox=QCheckBox(f"{i+1}")
            scroll_layout.addWidget(self.checkbox)
            self.checkbox.stateChanged.connect(lambda state, i=i :self.plot_i_th_BPI(i,state))
        
        #Buttons
        #creating buttons
        button1 = QPushButton("Get data")
        button1.setCheckable(True)
        button1.clicked.connect(self.web)
        
        button2 = QPushButton("Plot Data")
        button2.setCheckable(True)
        button2.clicked.connect(self.plotter)  
        
        button3 = QPushButton("Train Model")
        button3.setCheckable(True)
        # button3.clicked.connect(self.train_model)        
        
        #adding button to layout
        BBC_layout.addWidget(button1)
        BBC_layout.addWidget(button2)
        BBC_layout.addWidget(button3)
        
        # state checkboxes
        # creating checkboxes
        self.checkbox1 = QCheckBox("Injection")
        self.checkbox2 = QCheckBox("Ramping")
        self.checkbox3 = QCheckBox("storage ")
        
        #connect statechange signal to a slot method
        self.checkbox1.stateChanged.connect(self.beam_state_selector)
        self.checkbox2.stateChanged.connect(self.beam_state_selector)
        self.checkbox3.stateChanged.connect(self.beam_state_selector)
        
        #adding Checkbox to layout
        CBlayout.addWidget(self.checkbox1)
        CBlayout.addWidget(self.checkbox2)
        CBlayout.addWidget(self.checkbox3)
        
        #BPIs_Canvas to BPI_plots_layout
        BPI_plots_layout.addWidget(self.BPIx_canvas)
        BPI_plots_layout.addWidget(self.BPIz_canvas)
        
        # add BPI_plots_layout to BPILayout
        BPI_layout.addLayout(BPI_plots_layout)
        
        #adding CBlayout to BBClayout
        BBC_layout.addLayout(CBlayout)
        
        #adding BBC_layout & plots_layout to main_layout
        main_layout.addLayout(BBC_layout)
        main_layout.addLayout(plots_layout)
        
        #adding canvas and BPI layout to plots_layout
        plots_layout.addWidget(self.canvas)
        plots_layout.addLayout(BPI_layout)
        
        
        central_widget.setLayout(main_layout) 
        
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
            
    def train_model(self):
        # call the header file having cnn 
        pass
            
        
app = QApplication(sys.argv)
win = MainWin()
win.show()
app.exec_()        