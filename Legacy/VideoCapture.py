import cv2
import numpy as np
import random

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer

class VideoRecorder(QWidget):
    def __init__(self):
        super().__init__()

        #initialize camera
        self.camera = cv2.VideoCapture(0)
        self.size = (640, 480) #resolution TODO
        self.recording = False
        self.start_pressed = False
        self.stop_pressed = False

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

        #Call Display Preview
        self.showEvent()
        # #Create timer for updating the video display
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.showEvent)
        # self.timer.start(1)

    def start_recording(self):
        print("start recording")
        self.start_pressed = True

        filename = "Test#" + str(random.randint(1,10000))
        self.video_writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M', 'J','P','G'), 10, self.size)

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
            else:
                break

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            
        self.stop_recording()
        
    def stop_recording(self):
        print("stop recording")
        self.camera.release()
        self.video_writer.release()
        self.video_display.clear()   
        self.recording = False
        self.start_pressed = False
        self.stop_pressed = True   

    def showEvent(self):
        print("Show Event")
        cv2.namedWindow("Video Display")

        while not self.start_pressed:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(image)
                self.video_display.setPixmap(pixmap)
            else: print("Camera is not conncted")


        
            

    # def start_recording(self):
    #     filename = "Sample#" + str(random.randint(1,10000))
    #     # self.video_writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MPG'), 10, self.size)
    #     self.video_writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc('M','J','P','G'), 10, self.size)


    #     self.startButton.setEnabled(False)
    #     self.stopButton.setEnabled(True)

    #     cv2.namedWindow("Video Display")

        
    #     while True:
    #         ret, frame = self.camera.read()

    #         if ret:
    #             if self.start_pressed:
    #                 self.video_writer.write(frame)
    #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #             image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    #             pixmap = QPixmap.fromImage(image)
    #             self.video_display.setPixmap(pixmap)
    #         else:
    #             break

    #         key = cv2.waitKey(1)
    #         if key == ord('q'):
    #             break

    #     self.camera.release()
    #     self.video_writer.release()
    #     self.video_display.clear()
    #     self.stopButton.setEnabled(False)
    #     self.startButton.setEnabled(True)
    
    # def stop_recording(self):
    #     self.start_pressed = False
    #     self.video_display.clear()
    #     self.stopButton.setEnabled(False)
    #     self.startButton.setEnabled(True)


###Legacy Code for Reference
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