import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QAction, QMenu, QApplication, QMainWindow, QMenuBar, QAction, QPushButton, QVBoxLayout, QWidget
from HistogramWindow import HistogramWindow
from PostProcessing import GetData
from Calibration import Calibration

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome!')

        #creating menu bar and two menu items
        menu_bar = self.menuBar()
        calibration_menu = QMenu('Calibration', self)
        measurement_menu = QMenu('Measurement', self)
        menu_bar.addMenu(calibration_menu)
        menu_bar.addMenu(measurement_menu)

        #creating buttons
        calibrate_button = QPushButton('Calibrate')
        calibrate_button.setStyleSheet('background-color: red')
        measurement_button = QPushButton('Measure')
        measurement_button.setStyleSheet('background-color: green')

        #Adding actions for the menu items and buttons
        calibration_action = QAction('Calibrate',self)
        calibration_action.triggered.connect(self.trigger_calibration)
        calibration_menu.addAction(calibration_action)
        calibrate_button.clicked.connect(self.trigger_calibration)

        measurement_action = QAction('Measure', self)
        measurement_action.triggered.connect(self.trigger_measurement)
        measurement_menu.addAction(measurement_action)
        measurement_button.clicked.connect(self.trigger_measurement)

        #Adding to buttons to layout
        layout = QVBoxLayout()
        layout.addWidget(calibrate_button)
        layout.addWidget(measurement_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def trigger_measurement(self):
        self.histogram = HistogramWindow()
        self.histogram.show()

    def trigger_calibration(self):
        self.histogram = HistogramWindow()
        self.histogram.show()


    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())