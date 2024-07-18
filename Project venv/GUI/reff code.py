import sys
import os
import cv2
from PyQt5 import QtGui, QtCore, uic, QtWidgets
import pyqtgraph as pg
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
import pyqtgraph.exporters
import numpy as np
from scipy.optimize import curve_fit, leastsq

qtMainFile= 'D:/Work/work/new_interferometry/Test_final/test_label/label_gui.ui'

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtMainFile)

##x = 20 # 300
##y = 0
##w = 1280 # 1000
##h = 830 # 800

x = 0 # 300
y = 0
w = 205 # 1000
h = 205 # 800
lineThickness = 2

##roi_pixel_h = 200
##roi_pixel_v = 600

lemda = 0.0005

roi_pixel_h = 200
roi_pixel_v = 200

##===================================================
## function to compute rms
##==================================================
def rms (arr1, arr2):
    mse = np.square(np.subtract(arr1, arr2)).mean()
    rmse = np.sqrt(mse)
    return rmse
##===================================================
## function to rotate image
##==================================================
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

##===================================================
## function to compute beam sizes
##==================================================
def beamsize(lemda, slit_sep, const_k, a4):
    size_comp = (float(lemda) * 6600 * (np.sqrt(0.5 * (np.log( 1/ (float(a4)*float(const_k))))))) /( np.pi * float(slit_sep))
    return size_comp


##==================================================    
# function to fit and ROI selection
##==================================================
def func( y, a1, a2, a3, a4, a5, a6):
    I = a1*(((np.sin((a2*y) -a3))/((a2*y)-a3))**2) * (1 + (a4 * np.cos((a5 * y) - a6)))
    return I

##================================================================
##GUI front Panel
##================================================================
class InterFerro(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    ## QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.image_view1 = pg.ImageView()
        self.image_view2 = pg.ImageView()
        self.img_plt.addWidget(self.image_view1)
        self.image_view1.ui.histogram.hide()
        self.image_view1.ui.roiBtn.hide()
        self.image_view1.ui.menuBtn.hide()
        self.rot_img_plt.addWidget(self.image_view2)
        self.image_view2.ui.histogram.hide()
        self.image_view2.ui.roiBtn.hide()
        self.image_view2.ui.menuBtn.hide()
        

##        self.h_plt.axes.hold(False) #clear on plot()
##        self.v_plt.axes.hold(False) #clear on plot()
##        self.img_plt.axes.hold(False) #clear on plot()
##        self.rot_img_plt.axes.hold(False) #clear on plot()
        self.load.clicked.connect(self.load_img)
        self.ang.valueChanged.connect(self.rot_img)
        self.proc.clicked.connect(self.proc_img)
        self.act.clicked.connect(self.print_msg)
        
        self.sld_a1_h.valueChanged.connect(self.update_a1_h)
        self.sld_a2_h.valueChanged.connect(self.update_a2_h)
        self.sld_a3_h.valueChanged.connect(self.update_a3_h)
        self.sld_a4_h.valueChanged.connect(self.update_a4_h)
        self.sld_a5_h.valueChanged.connect(self.update_a5_h)
        self.sld_a6_h.valueChanged.connect(self.update_a6_h)

        self.sld_a1_v.valueChanged.connect(self.update_a1_v)
        self.sld_a2_v.valueChanged.connect(self.update_a2_v)
        self.sld_a3_v.valueChanged.connect(self.update_a3_v)
        self.sld_a4_v.valueChanged.connect(self.update_a4_v)
        self.sld_a5_v.valueChanged.connect(self.update_a5_v)
        self.sld_a6_v.valueChanged.connect(self.update_a6_v)
        self.graph_plot.clicked.connect(self.plot_graph)

    def print_msg(self):
        self.res1.setText('hello world')

    def update_a1_h(self, value):
        self.sld_val_a1_h.setText(str(float(value/10000)))
        self.plot_graph()
        
    def update_a2_h(self, value):
        self.sld_val_a2_h.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a3_h(self, value):
        self.sld_val_a3_h.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a4_h(self, value):
        self.sld_val_a4_h.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a5_h(self, value):
        self.sld_val_a5_h.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a6_h(self, value):
        self.sld_val_a6_h.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a1_v(self, value):
        self.sld_val_a1_v.setText(str(float(value/10000)))
        self.plot_graph()
        
    def update_a2_v(self, value):
        self.sld_val_a2_v.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a3_v(self, value):
        self.sld_val_a3_v.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a4_v(self, value):
        self.sld_val_a4_v.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a5_v(self, value):
        self.sld_val_a5_v.setText(str(float(value/10000)))
        self.plot_graph()

    def update_a6_v(self, value):
        self.sld_val_a6_v.setText(str(float(value/10000)))
        self.plot_graph()

    def plot_graph(self):

        noptx = [float(self.sld_val_a1_h.text()), float(self.sld_val_a2_h.text()), float(self.sld_val_a3_h.text()), float(self.sld_val_a4_h.text()), float(self.sld_val_a5_h.text()), float(self.sld_val_a6_h.text())]
        nopty = [float(self.sld_val_a1_v.text()), float(self.sld_val_a2_v.text()), float(self.sld_val_a3_v.text()), float(self.sld_val_a4_v.text()), float(self.sld_val_a5_v.text()), float(self.sld_val_a6_v.text())]

        print(noptx, nopty)

        self.v_plt.clear()
        self.h_plt.clear()
        
        l_x = func(self.new_x_data, *noptx)
        l_y = func(self.new_y_data, *nopty)
        self.v_plt.plot(self.new_y_data, self.new_y_func, pen= 'r',symbol='o', symbolPen='r', symbolBrush='r', width=0.1)
##        self.v_plt.plot(self.new_y_data, func(self.new_y_data, *nopty), pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.1)
        self.v_plt.plot(self.new_y_data, l_y, pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.1)
        self.h_plt.plot(self.new_x_data, self.new_x_func, pen= 'r',symbol='o', symbolPen='r', symbolBrush='r', width=0.1)
##        self.h_plt.plot(self.new_x_data, func(self.new_x_data, *noptx), pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.1)
        self.h_plt.plot(self.new_x_data, l_x, pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.1)
        rms_x = rms(self.new_x_data, l_x)
        rms_y = rms(self.new_y_data, l_y)
        self.rms_h.setText(str(rms_x))
        self.rms_v.setText(str(rms_y))


    def load_img(self):
        
        fpath = (QtWidgets.QFileDialog.getOpenFileName(None, 'Open file'))
        self.image = cv2.imread(fpath[0], cv2.IMREAD_GRAYSCALE)
        self.image_view1.clear()
        self.image_view1.setImage(self.image.T)
        self.image_view2.clear()
        self.image_view2.setImage(self.image.T)

    def rot_img(self, value):
        angle = float(value)/10
        self.sld_ang.setText(str(float(value/10)))
        self.img_rot = rotate_image(self.image, angle)
        self.image_view2.clear()
        self.image_view2.setImage(self.img_rot.T)

    def proc_img(self):
        img_crop = self.image[y:y+h, x:x+w]
        img_blur = img_crop # cv2.GuassianBlurr(img_crop, (5,5), 0)
        (minVal, maxVal_disp, minLoc, maxLoc) = cv2.minMaxLoc(img_blur)
        norm_image = cv2.normalize(img_blur, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(norm_image)
        y_data = np.linspace(-int(roi_pixel_v/2), int(roi_pixel_v/2), roi_pixel_v)
        x_data = np.linspace(-int(roi_pixel_h/2), int(roi_pixel_h/2), roi_pixel_h)
        y_func = norm_image[(maxLoc[1]- int(roi_pixel_v/2)) : (maxLoc[1]+ int(roi_pixel_v/2)), maxLoc[0]]
        x_func = norm_image[maxLoc[1], (maxLoc[0]-int(roi_pixel_h/2)): (maxLoc[0]+int(roi_pixel_h/2)) ]
        y_ind = np.where(y_func < 0.01)
        x_ind = np.where(x_func < 0.01)
        self.new_y_data = np.delete(y_data, y_ind)
        self.new_x_data = np.delete(x_data, x_ind)
        self.new_y_func = np.delete(y_func, y_ind)
        self.new_x_func = np.delete(x_func, x_ind)
        bounds_relax = ([-1, -1, -1, -1, -1, -1], [1, 1, 1, 1, 1, 1])
        bounds_h = ([0.1,0.028,-0.1, 0.05,0.1,-1], [0.5, 0.036, 0.01, 0.3, 0.125, 0.001]) 
        bounds_v =([0.2,-0.1, 0.1, 0.05,0.25,-0.5], [0.2575,-0.01, 0.18, 0.5, 0.289, 0.9293])
        p0_h = [1,0.039,0.1, 1, 0.15, 1]
        p0_v = [0.21, 0.1,0.25, 1,0.32, 1]

        popty, pcovy = curve_fit(func, self.new_y_data, self.new_y_func) #, p0 = p0_v, bounds=bounds_relax, check_finite=True, method= 'trf' )
        poptx, pcovx = curve_fit(func, self.new_x_data, self.new_x_func) #, p0 = p0_h, bounds=bounds_relax, check_finite=True, method= 'trf' )

        self.v_plt.clear()
        self.h_plt.clear()
        
        
        self.v_plt.plot(self.new_y_data, self.new_y_func, pen= 'r',symbol='o', symbolPen='r', symbolBrush='r', width=0.3)
        self.v_plt.plot(self.new_y_data, func(self.new_y_data, *popty), pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.1)
        self.h_plt.plot(self.new_x_data, self.new_x_func, pen= 'r',symbol='o', symbolPen='r', symbolBrush='r', width=0.3)
        self.h_plt.plot(self.new_x_data, func(self.new_x_data, *poptx), pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.3)

        self.sld_a1_h.setValue(int(10000* round(poptx[0], 4)))
        self.sld_a2_h.setValue(int(10000* round(poptx[1], 4)))
        self.sld_a3_h.setValue(int(10000* round(poptx[2], 4)))
        self.sld_a4_h.setValue(int(10000* round(poptx[3], 4)))
        self.sld_a5_h.setValue(int(10000* round(poptx[4], 4)))
        self.sld_a6_h.setValue(int(10000* round(poptx[5], 4)))

        self.sld_a1_v.setValue(int(10000* round(popty[0], 4)))
        self.sld_a2_v.setValue(int(10000* round(popty[1], 4)))
        self.sld_a3_v.setValue(int(10000* round(popty[2], 4)))
        self.sld_a4_v.setValue(int(10000* round(popty[3], 4)))
        self.sld_a5_v.setValue(int(10000* round(popty[4], 4)))
        self.sld_a6_v.setValue(int(10000* round(popty[5], 4)))

        print(poptx, popty)
        print(round(poptx[0], 4))
        print(self.sld_a1_h.value())
##        self.hor_size_graph.plot(self.l_ind, self.l_x, pen= 'r',symbol='o', symbolPen='r', symbolBrush='r', width=0.3)
##        self.ver_size_graph.plot(self.l_ind, self.l_y, pen= 'g',symbol='o', symbolPen='g', symbolBrush='g', width=0.1)
            
        

    def updateLabel(self, value):
        self.sld_val.setText(str(float(value/1000)))

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
##    fpath = str(QtWidgets.QFileDialog.getOpenFileName(None, 'Open file'))
##    image = cv2.imread(fpath, cv2.IMREAD_GRAYSCALE)
    
##    img_crop = self.img[y:y+h, x:x+w]
##    img_blur = cv2.GuassianBlurr(img_crop, (5,5), 0)
##    (minVal, maxVal_disp, minLoc, maxLoc) = cv2.minMaxLoc(img_blur)
##    norm_image = cv2.normalize(img_blur, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
##            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(norm_image)
##    y_data = np.linspace(-int(roi_pixel_v/2), int(roi_pixel_v/2), roi_pixel_v)
##    x_data = np.linspace(-int(roi_pixel_h/2), int(roi_pixel_h/2), roi_pixel_h)
##    y_func = norm_image[(maxLoc[1]- int(roi_pixel_v/2)) : (maxLoc[1]+ int(roi_pixel_v/2)), maxLoc[0]]
##    x_func = norm_image[maxLoc[1], (maxLoc[0]-int(roi_pixel_h/2)): (maxLoc[0]+int(roi_pixel_h/2)) ]
##    y_ind = np.where(y_func < 0.01)
##    x_ind = np.where(x_func < 0.01)
##    new_y_data = np.delete(y_data, y_ind)
##    new_x_data = np.delete(x_data, x_ind)
##    new_y_func = np.delete(y_func, y_ind)
##    new_x_func = np.delete(x_func, x_ind)
##    bound_h = ([0.1,0.028,-0.1, 0.05,0.1,-1], [0.5, 0.036, 0.01, 0.3, 0.125, 0.001]) 
##    bounds_v =([0.2,-0.1, 0.1, 0.05,0.25,-0.5], [0.2575,-0.01, 0.18, 0.5, 0.289, 0.9293])
##    p0_h = [1,0.039,0.1, 1, 0.15, 1]
##    p0_v = [1, 0.1,0.25, 1,0.32, 1]
##
##    popty, pcovy = curve_fit(func, new_y_data, new_y_func, p0 = p0_v, bounds=bounds_v, check_finite=True, method= 'trf' )
##    poptx, pcovx = curve_fit(func, new_x_data, new_x_func, p0 = p0_h, bounds=bounds_h, check_finite=True, method= 'trf' ) 
    
    
    window = InterFerro()
    window.show()
    sys.exit(app.exec_())

