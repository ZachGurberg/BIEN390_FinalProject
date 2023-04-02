import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QAction, QMenu, QApplication, QMainWindow, QMenuBar, QAction, QPushButton, QVBoxLayout, QWidget
from HistogramWindow import HistogramWindow
from PostProcessing import GetData
from Calibration import Calibration
from VideoCapture2 import VideoRecorder

KNOWN_HEIGHT = 0.5
KNOWN_WIDTH = 5.5

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Welcome!')
        self.conversion = None

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
         # create video recorder widget
        if self.conversion != None:
            self.video_recorder = VideoRecorder()
            self.video_recorder.setFixedSize(660,530)

            # create buttons
            start_recording_button = QPushButton('Start Recording')
            stop_recording_button = QPushButton('Stop Recording')

            # add buttons to layout
            layout = QVBoxLayout()
            layout.addWidget(self.video_recorder)
            layout.addWidget(start_recording_button)
            layout.addWidget(stop_recording_button)

            # create widget for layout
            widget = QWidget()
            widget.setLayout(layout)

            # add layout widget to main window
            self.setCentralWidget(widget)

            # connect button signals to video recorder functions
            start_recording_button.clicked.connect(self.video_recorder.start_recording)
            stop_recording_button.clicked.connect(self.video_recorder.stop_recording)
        else:
            showMessage('Must Calibrate First!', 1000)

        #The stop recording function calls the creation of a histogram. the data passed to the histogram is based
        # on the filename of the recorded video. The video passes through the postProcessing steps before the histogram
        # is created and displayed to the user. The test.avi filename is the filename used for now, but it can be changed quickly

    def trigger_calibration(self):
        #Temporary placeholder to test function of histogram. The function should operate in a similar manner to the 
        #video recorder. But the bounding boxes should be computed live. Once the bounding box with the correct ratio
        #is found, the video should stop and the conversion from pixels to mm should be stored as a self.conversion field
        # the user should then receive a message saying calibration confirmed and we can proceed to the measure button.
        self.conversion = Calibration(KNOWN_HEIGHT,KNOWN_WIDTH)

    def trigger_histogram(self, filename):
        #TODO remove this for function
        filename = "test.avi"
        self.histogram = HistogramWindow(filename, self.conversion)
        self.histogram.show()
        ## Putting a little note here, I'm not sure if self.histogram.show() is working
            
def showMessage(message, time):
    # create an image to display the message on
    img = np.zeros((512, 512, 3), np.uint8)
    # add the text to the image
    cv2.putText(img, message, (100, 256), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # display the image for time
    cv2.imshow('Message', img)
    cv2.waitKey(time)
    # close the window
    cv2.destroyAllWindows()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())