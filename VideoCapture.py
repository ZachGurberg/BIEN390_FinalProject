import cv2
import numpy as np
import random

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap

class VideoRecorder(QWidget):
    def __init__(self):
        super().__init__()

        #initialize camera
        self.camera = cv2.VideoCapture(0)
        self.size = (640, 480) #resolution TODO
        self.recording = False

        #Create GUI elements
        self.video_display = QLabel()
        self.startButton = QPushButton('Start Recording')
        self.stopButton = QPushButton('Stop Recording')
        self.stopButton.setEnabled(False)

        #Setup layout
        layout = QVBoxLayout()
        layout.addWidget(self.video_display)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.startButton)
        button_layout.addWidget(self.stopButton)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        #Connect signals to slots
        self.startButton.clicked.connect(self.start_recording)
        self.stopButton.clicked.connect(self.stop_recording)

    def start_recording(self):
        filename = "Sample#" + str(random.randint(1,10000)) + ".avi"
        self.video_writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MPG'), 10, self.size)

        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)

        self.recording = True
        while self.recording:
            ret, frame = self.camera.read()

            if ret:
                self.video_writer.write(frame)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.video_display.setPixmap(pixmap)
            if not self.recording:
                break

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        self.camera.release()
        self.video_writer.release()
        self.video_display.clear()
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
    
    def stop_recording(self):
        self.recording = False



# def captureVideo():
#     filename = "Sample#" + str(random.randint(1,10000))+".avi" 

#     #camera parameters
#     camera = cv2.VideoCapture(0)
#     size = (640,480) #TODO might need to make larger and adjust dependencies in postProcessing/calibration

#     #capturing and saving video
#     #edge
#     if (camera.isOpened() == False): 
#         print("Error reading video file")

#     result = cv2.videoWriter(filename, cv2.VideoWriter_fourcc(*'MPG'), 10, size)

#     while(True):
#         ret, frame = camera.read()
    
#         if ret == True: 
    
#             # Write the frame into the
#             # file 'filename.avi'
#             result.write(frame)
    
#             # Display the frame
#             # saved in the file
#             cv2.imshow('Frame', frame)
    
#             # Press S on keyboard 
#             # to stop the process
#             if cv2.waitKey(1) & 0xFF == ord('s'):
#                 break
    
#         # Break the loop
#         else:
#             break

#     camera.release()
#     result.release()
#     return filename