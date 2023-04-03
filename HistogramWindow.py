from PyQt5.QtWidgets import QMainWindow
from PostProcessing import GetData
from PyQt5.QtWidgets import QVBoxLayout, QWidget
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime


class HistogramWindow(QMainWindow):
    def __init__(self, filename, conversion_factor):
        super().__init__()
        self.setWindowTitle('Histogram')
        self.setGeometry(100,100,800,600)
        self.data = GetData(filename, True) * (conversion_factor**3) ##TODO: might have to rearrange import here
        print(self.data)
        self.create_histogram()
    
    def create_histogram(self):

        # Get current date and time
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

        #Create a MatPlotLib Plot
        fig = plt.figure()
        ax=fig.add_subplot(111)
        ax.hist(self.data, bins=4)
        ax.set_title(dt_string)
        ax.set_xlabel('Volume (ml)')
        ax.set_ylabel('Frequency')

        # xmin = np.floor(self.data.min() / 100) * 100
        # xmax = np.ceil(self.data.max() / 100) * 100
        ax.set_xlim(0, 1)

        #Adding it to a QWidget as Layout
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget = QWidget()
        widget.setLayout(layout)

        self.resize(1000,800)
        self.setCentralWidget(widget)
