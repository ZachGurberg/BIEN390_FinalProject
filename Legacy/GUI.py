import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy, QMenu, QAction, QPushButton, QVBoxLayout, QWidget, QBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QValueAxis
from PyQt5.QtGui import QPainter
from PostProcessing import GetData


class HistogramWindow(QMainWindow):
    # def __init__(self, data):
    #     super().__init__()
    #     self.setWindowTitle('Histogram')
    #     self.setGeometry(100, 100, 680, 500)
    #     self.data = data
    #     self.create_histogram()

    # def create_histogram(self):
    #     # Calculate histogram data using NumPy
    #     hist, bin_edges = np.histogram(self.data, bins=4)

    #     # Create QBarSet for each bin in the histogram
    #     barsets = []
    #     for i, val in enumerate(hist):
    #         barset = QBarSet(f'{bin_edges[i]:.2f} - {bin_edges[i+1]:.2f}')
    #         barset.append(val)
    #         barsets.append(barset)

    #     # Create QBarSeries and add QBarSets to it
    #     series = QBarSeries()
    #     series.setBarWidth(0.9)
    #     for barset in barsets:
    #         series.append(barset)

    #     # Create QChart and add QBarSeries to it
    #     chart = QChart()
    #     chart.addSeries(series)
    #     chart.setTitle('Histogram')
    #     chart.setAnimationOptions(QChart.SeriesAnimations)

    #     # Set axis labels
    #     axis_x = QValueAxis()
    #     axis_x.setTitleText('Volume')
    #     axis_x.setRange(min(self.data), max(self.data))
    #     chart.addAxis(axis_x, Qt.AlignBottom)
    #     series.attachAxis(axis_x)
    #     axis_y = QValueAxis()
    #     axis_y.setTitleText('Frequency')
    #     axis_y.setRange(0, max(hist))
    #     axis_y.setTickCount(max(hist)+1)
    #     chart.addAxis(axis_y, Qt.AlignLeft)
    #     series.attachAxis(axis_y)

    #     # Create QChartView to display chart
    #     chart_view = QChartView(chart, self)
    #     chart_view.setRenderHint(QPainter.Antialiasing)
    #     chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #     self.setCentralWidget(chart_view)
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('Histogram')
        self.setGeometry(100, 100, 800, 600)
        self.data = data
        self.create_histogram()

    def create_histogram(self):
        # Calculate histogram data using NumPy
        hist, bin_edges = np.histogram(self.data, bins=4)

        # Create a Matplotlib Figure instance
        fig = plt.figure()

        # Create a Matplotlib Axes instance
        ax = fig.add_subplot(111)

        # Plot the histogram using Matplotlib
        ax.hist(self.data, bins=4)

        # Create a FigureCanvas instance to display the Figure in PyQt5
        canvas = FigureCanvas(fig)

        # Create a QVBoxLayout instance to organize the canvas in the window
        layout = QVBoxLayout()
        layout.addWidget(canvas)

        # Create a QWidget instance to hold the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the window to the QWidget instance
        self.setCentralWidget(widget)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome!')

        # Create menu bar and two menu items
        menu_bar = self.menuBar()
        calibration_menu = QMenu('Calibration', self)
        measurement_menu = QMenu('Measurement', self)
        menu_bar.addMenu(calibration_menu)
        menu_bar.addMenu(measurement_menu)

        # Create actions for each menu item
        calibration_action = QAction('Calibrate', self)
        calibration_action.triggered.connect(self.show_calibration_video)
        calibration_menu.addAction(calibration_action)

        measurement_action = QAction('Measure', self)
        measurement_action.triggered.connect(self.show_histogram)
        measurement_menu.addAction(measurement_action)

        calibrate_button = QPushButton('Calibrate')
        calibrate_button.setStyleSheet('background-color: red')
        calibrate_button.clicked.connect(self.show_calibration_video)

        histogram_button = QPushButton('Measure')
        histogram_button.setStyleSheet('background-color: green')
        histogram_button.clicked.connect(self.show_histogram)

        layout = QVBoxLayout()
        layout.addWidget(calibrate_button)
        layout.addWidget(histogram_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_calibration_video(self):
        # Use OpenCV to read and display video
        cap = cv2.VideoCapture('test.avi')
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Calibration Video', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def show_histogram(self):
        # Display histogram created in the original script
        self.histogram_window = HistogramWindow(data)
        self.histogram_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Get data from external script
    data = GetData(False)
        
    print(data)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())