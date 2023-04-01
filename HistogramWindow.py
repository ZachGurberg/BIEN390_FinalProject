from PyQt5.QtWidgets import QMainWindow
from PostProcessing import GetData
from PyQt5.QtWidgets import QVBoxLayout, QWidget
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class HistogramWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Histogram')
        self.setGeometry(100,100,800,600)
        self.data = GetData(False) ##TODO: might have to rearrange import here
        self.create_histogram()
    
    def create_histogram(self):

        #Create a MatPlotLib Plot
        fig = plt.figure()
        ax=fig.add_subplot(111)
        ax.hist(self.data, bins=4)

        #Adding it to a QWidget as Layout
        canvas = FigureCanvas(fig)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
