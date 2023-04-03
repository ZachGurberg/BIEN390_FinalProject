import cv2
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from datetime import datetime
from PostProcessing import GetData


class VideoRecorder(QWidget):
    def __init__(self):
        super().__init__()

        # initialize video capture
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) ##TODO
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # initialize video writer
        self.is_recording = False
        self.writer = None

        # initialize video display
        self.canvas = QLabel()
        self.canvas.setFixedSize(self.width, self.height)

        # set layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # start video capture
        self.timer = QTimer(self)
        self.timer.setInterval(1000 // self.fps)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.canvas.setPixmap(QPixmap.fromImage(QImage(frame.data, self.width, self.height, QImage.Format_BGR888)))
            if self.is_recording:
                self.writer.write(frame)

    def start_recording(self):
        self.is_recording = True
        self.filename = f"video_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.MOV"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter(self.filename, fourcc, self.fps, (self.width, self.height))

    def stop_recording(self):
        self.is_recording = False
        self.writer.release()
        QMessageBox.information(self, 'Video Saved', f"Video saved as {self.filename}.")
        self.cap.release()
        self.parent().close()
        self.parent().parent().trigger_histogram(self.filename)
        self.parent().parent().close()
        self.close()

        