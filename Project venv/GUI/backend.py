import sys
from PyQt5 import QtWidgets, uic
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsView

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('testwin.ui', self)

        # Access the buttons and graphics view from the UI
        self.get_data_button = self.findChild(QtWidgets.QPushButton, 'pushButton')
        self.plot_data_button = self.findChild(QtWidgets.QPushButton, 'pushButton_2')
        self.graphics_view = self.findChild(QGraphicsView, 'graphicsView')

        # Set up the pyqtgraph plot widget
        self.plot_widget = pg.PlotWidget()
        self.graphics_view.setCentralWidget(self.plot_widget)

        # Connect the buttons to their respective functions
        self.get_data_button.clicked.connect(self.get_data)
        self.plot_data_button.clicked.connect(self.plot_data)

        # Data storage
        self.data_x = []
        self.data_y = []

    def get_data(self):
        # Simulate getting data
        import numpy as np
        self.data_x = np.linspace(0, 10, 100)
        self.data_y = np.sin(self.data_x)

    def plot_data(self):
        if self.data_x and self.data_y:
            self.plot_widget.plot(self.data_x, self.data_y, pen='b')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
